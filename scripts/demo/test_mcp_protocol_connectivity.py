#!/usr/bin/env python3
"""Real Model Context Protocol (MCP) client connectivity test.

Unlike scripts/demo/test_mcp_connectivity.py (which drives the REST API
in-process via fastapi.testclient.TestClient), this script starts a REAL
uvicorn HTTP server for the MCP Backend and connects to it using the
official `mcp` Python client SDK (mcp.client.streamable_http +
mcp.ClientSession) - performing the exact same initialize -> list_tools ->
call_tool sequence Microsoft Copilot Studio's "Add MCP server" flow performs
when a maker adds this MCP Backend as a Tool. See
docs/decisions/0016-copilot-studio-github-harness-confirmed.md.

Usage:
    PYTHONPATH=".:apps/demo-cli:services/mcp-backend" \\
        python3 scripts/demo/test_mcp_protocol_connectivity.py [industry_pack_id]
"""
from __future__ import annotations

import asyncio
import sys
import threading
import time
from contextlib import closing
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "services" / "mcp-backend"))

import socket

import uvicorn
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from mcp_backend.factory import build_app

from iq_platform.orchestration.industry_pack_loader import load_manifest, load_plugin_module

ALL_PACK_IDS = ["manufacturing", "financial-services", "retail", "healthcare", "public-sector"]
DEFAULT_PACK_ID = "manufacturing"


def _free_port() -> int:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


class _BackgroundServer:
    """Runs a real uvicorn server for the MCP Backend in a background thread,
    so the official MCP client SDK can connect over a genuine HTTP socket
    (streamablehttp_client requires a real URL, not an in-process ASGI
    transport)."""

    def __init__(self, app, port: int):
        self._config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning")
        self._server = uvicorn.Server(self._config)
        self._thread = threading.Thread(target=self._server.run, daemon=True)

    def __enter__(self) -> str:
        self._thread.start()
        while not self._server.started:
            time.sleep(0.05)
        return f"http://127.0.0.1:{self._config.port}/mcp/"

    def __exit__(self, *_exc_info) -> None:
        self._server.should_exit = True
        self._thread.join(timeout=5)


async def _check_pack_async(pack_id: str) -> bool:
    pack_dir = REPO_ROOT / "industry-packs" / pack_id
    manifest = load_manifest(pack_dir)
    generator = load_plugin_module(pack_dir / manifest.sample_data_path)
    dataset = generator.generate_dataset(seed=42, scale="demo")
    app = build_app(dataset, pack_dir, manifest)

    with _BackgroundServer(app, _free_port()) as url:
        async with streamablehttp_client(url) as (read_stream, write_stream, _get_session_id):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                print(f"[{pack_id}] MCP initialize -> OK")

                tools_result = await session.list_tools()
                tool_names = [t.name for t in tools_result.tools]
                if not tool_names:
                    print(f"[{pack_id}] tools/list -> FAIL (no tools returned)")
                    return False
                print(f"[{pack_id}] tools/list -> {len(tool_names)} tool(s) OK ({', '.join(tool_names)})")

                first_tool = tool_names[0]
                call_result = await session.call_tool(first_tool, arguments={})
                ok = call_result.isError is not True
                print(f"[{pack_id}] tools/call({first_tool}) -> {'OK' if ok else 'FAIL'}")
                return ok


def check_pack(pack_id: str) -> bool:
    return asyncio.run(_check_pack_async(pack_id))


def main() -> int:
    pack_ids = sys.argv[1:] or ALL_PACK_IDS
    results = [check_pack(pack_id) for pack_id in pack_ids]
    if all(results):
        print("\nAll real MCP protocol connectivity checks passed.")
        return 0
    print("\nSome real MCP protocol connectivity checks FAILED.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
