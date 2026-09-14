"""Integration test: the real Model Context Protocol (MCP) server mounted at
/mcp (mcp_backend/mcp_protocol_server.py), exercised via raw JSON-RPC requests
through fastapi.testclient.TestClient - the same wire protocol Microsoft
Copilot Studio's MCP server connection flow uses. This complements
scripts/demo/test_mcp_protocol_connectivity.py, which exercises
the same server through the official `mcp` client SDK over a real HTTP
socket - this test stays in-process for speed.
"""
from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from mcp_backend.factory import build_app

from iq_platform.orchestration.industry_pack_loader import load_manifest

REPO_ROOT = Path(__file__).resolve().parents[2]
ALL_PACK_IDS = ["manufacturing", "financial-services", "retail", "healthcare", "public-sector"]

_JSON_RPC_HEADERS = {"Accept": "application/json, text/event-stream", "Content-Type": "application/json"}


def _parse_sse_json(response_text: str) -> dict:
    """The streamable HTTP transport returns 'event: message\\ndata: {...}\\n\\n'
    (SSE framing) even for a single JSON-RPC response; extract the JSON payload."""
    import json

    for line in response_text.splitlines():
        if line.startswith("data:"):
            return json.loads(line[len("data:") :].strip())
    raise AssertionError(f"No SSE 'data:' line found in response: {response_text!r}")


@pytest.mark.parametrize("pack_id", ALL_PACK_IDS)
def test_mcp_initialize_list_and_call_tool(pack_id: str):
    pack_dir = REPO_ROOT / "industry-packs" / pack_id
    manifest = load_manifest(pack_dir)
    dataset = {}  # tool functions under test only need to run far enough to be listed/invoked
    app = build_app(dataset, pack_dir, manifest=manifest)

    with TestClient(app) as client:
        init_resp = client.post(
            "/mcp/",
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-11-25",
                    "capabilities": {},
                    "clientInfo": {"name": "test-client", "version": "0.1"},
                },
            },
            headers=_JSON_RPC_HEADERS,
        )
        assert init_resp.status_code == 200
        session_id = init_resp.headers["mcp-session-id"]
        init_body = _parse_sse_json(init_resp.text)
        assert init_body["result"]["serverInfo"]["name"] == f"iiq-mcp-backend-{manifest.id}"

        notif_resp = client.post(
            "/mcp/",
            json={"jsonrpc": "2.0", "method": "notifications/initialized"},
            headers={**_JSON_RPC_HEADERS, "mcp-session-id": session_id},
        )
        assert notif_resp.status_code == 202

        list_resp = client.post(
            "/mcp/",
            json={"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
            headers={**_JSON_RPC_HEADERS, "mcp-session-id": session_id},
        )
        assert list_resp.status_code == 200
        tools = _parse_sse_json(list_resp.text)["result"]["tools"]
        tool_names = {t["name"] for t in tools}
        assert tool_names, f"{pack_id}: expected at least one MCP tool, got none"

        first_tool = next(iter(tool_names))
        call_resp = client.post(
            "/mcp/",
            json={
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {"name": first_tool, "arguments": {}},
            },
            headers={**_JSON_RPC_HEADERS, "mcp-session-id": session_id},
        )
        assert call_resp.status_code == 200
        call_body = _parse_sse_json(call_resp.text)
        assert "result" in call_body, f"{pack_id}/{first_tool}: expected a tool result, got {call_body}"
