"""Integration tests: MCP client (FastAPI TestClient) <-> MCP Backend, tested
directly (not via the Orchestrator). See instruction §22.3.
"""
from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from mcp_backend.factory import build_app

from iq_platform.orchestration.industry_pack_loader import load_manifest, load_plugin_module

REPO_ROOT = Path(__file__).resolve().parents[2]
INDUSTRY_PACKS_DIR = REPO_ROOT / "industry-packs"

ALL_PACK_IDS = ["manufacturing", "financial-services", "retail", "healthcare", "public-sector"]


def _client_for(pack_id: str) -> TestClient:
    pack_dir = INDUSTRY_PACKS_DIR / pack_id
    manifest = load_manifest(pack_dir)
    generator = load_plugin_module(pack_dir / manifest.sample_data_path)
    dataset = generator.generate_dataset(seed=42, scale="demo")
    return TestClient(build_app(dataset, pack_dir, manifest))


@pytest.mark.parametrize("pack_id", ALL_PACK_IDS)
def test_health_endpoint(pack_id: str):
    client = _client_for(pack_id)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.parametrize("pack_id", ALL_PACK_IDS)
def test_tools_endpoint_lists_declared_tools(pack_id: str):
    pack_dir = INDUSTRY_PACKS_DIR / pack_id
    manifest = load_manifest(pack_dir)
    tools_module = load_plugin_module(pack_dir / manifest.mcp_tools_path)

    client = _client_for(pack_id)
    response = client.get("/tools")
    assert response.status_code == 200
    listed_names = {tool["tool_name"] for tool in response.json()}
    assert listed_names == set(tools_module.TOOL_DESCRIPTIONS.keys())


@pytest.mark.parametrize("pack_id", ALL_PACK_IDS)
def test_invoke_unknown_tool_returns_structured_error_not_http_error(pack_id: str):
    client = _client_for(pack_id)
    response = client.post("/tools/does_not_exist/invoke", json={"params": {}})
    # Contract: every tool response - including errors - is a 200 with a
    # structured MCPToolResponse body, never a bare HTTP error (§10).
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "error"
    assert "Unknown tool" in body["errors"][0]
