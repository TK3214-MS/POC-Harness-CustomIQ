#!/usr/bin/env python3
"""MCP connectivity test (instruction §18/§19). Builds the MCP Backend
in-process for a given Industry Pack and exercises /health, /tools, and one
tool invocation - useful as a fast standalone check outside the full CLI.

Usage:
    PYTHONPATH=".:apps/demo-cli:services/mcp-backend" \\
        python3 scripts/demo/test_mcp_connectivity.py [industry_pack_id]
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "services" / "mcp-backend"))

from fastapi.testclient import TestClient
from mcp_backend.factory import build_app

from iq_platform.orchestration.industry_pack_loader import load_manifest, load_plugin_module

ALL_PACK_IDS = ["manufacturing", "financial-services", "retail", "healthcare", "public-sector"]


def check_pack(pack_id: str) -> bool:
    pack_dir = REPO_ROOT / "industry-packs" / pack_id
    manifest = load_manifest(pack_dir)
    generator = load_plugin_module(pack_dir / manifest.sample_data_path)
    dataset = generator.generate_dataset(seed=42, scale="demo")
    tools_module = load_plugin_module(pack_dir / manifest.mcp_tools_path)

    client = TestClient(build_app(dataset, pack_dir, manifest))

    health = client.get("/health")
    ok = health.status_code == 200 and health.json().get("status") == "ok"
    print(f"[{pack_id}] GET /health -> {health.status_code} {'OK' if ok else 'FAIL'}")

    tools_response = client.get("/tools")
    declared = set(tools_module.TOOL_DESCRIPTIONS.keys())
    listed = {t["tool_name"] for t in tools_response.json()} if tools_response.status_code == 200 else set()
    tools_ok = tools_response.status_code == 200 and listed == declared
    print(f"[{pack_id}] GET /tools -> {tools_response.status_code} {len(listed)} tool(s) {'OK' if tools_ok else 'FAIL'}")

    first_tool = next(iter(declared)) if declared else None
    invoke_ok = False
    if first_tool:
        invoke_response = client.post(f"/tools/{first_tool}/invoke", json={"params": {}})
        invoke_ok = invoke_response.status_code == 200 and "status" in invoke_response.json()
        print(f"[{pack_id}] POST /tools/{first_tool}/invoke -> {invoke_response.status_code} {'OK' if invoke_ok else 'FAIL'}")

    return ok and tools_ok and invoke_ok


def main() -> int:
    targets = sys.argv[1:] or ALL_PACK_IDS
    results = {pack_id: check_pack(pack_id) for pack_id in targets}
    print()
    all_ok = all(results.values())
    print("All MCP connectivity checks passed." if all_ok else f"Failures: {[k for k, v in results.items() if not v]}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
