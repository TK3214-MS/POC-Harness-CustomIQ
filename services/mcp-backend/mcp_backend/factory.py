"""Builds an Industry-Pack-aware MCP Backend app instance.

See docs/decisions/0010-industry-pack-plugin-loading.md and
docs/decisions/0011-generic-orchestrator-and-semantic-adapter.md. Contains no
industry-specific logic - works for any pack whose manifest.mcp_tools_path
points to a module exposing TOOL_FUNCTIONS/TOOL_DESCRIPTIONS.
"""
from __future__ import annotations

import os
from pathlib import Path

from iq_platform.contracts.capability import AdapterMode
from iq_platform.contracts.manifest import IndustryPackManifest
from iq_platform.orchestration.industry_pack_loader import load_manifest, load_plugin_module
from mcp_backend.app import create_app
from mcp_backend.mcp_protocol_server import build_mcp_server
from mcp_backend.registry import ToolRegistry


def _allowed_tools_from_env() -> set[str] | None:
    """Optional defense-in-depth allowlist (instruction §24). Set
    MCP_BACKEND_ALLOWED_TOOLS to a comma-separated tool name list to restrict
    which of a pack's tools this deployment exposes. Unset means "allow every
    tool the pack declares"."""
    raw = os.environ.get("MCP_BACKEND_ALLOWED_TOOLS")
    if not raw:
        return None
    return {name.strip() for name in raw.split(",") if name.strip()}


def build_app(dataset: dict, pack_dir: Path, manifest: IndustryPackManifest | None = None):
    manifest = manifest or load_manifest(pack_dir)
    tools_module = load_plugin_module(pack_dir / manifest.mcp_tools_path)
    registry = ToolRegistry(
        dataset=dataset,
        tool_functions=tools_module.TOOL_FUNCTIONS,
        descriptions=tools_module.TOOL_DESCRIPTIONS,
        adapter_mode=AdapterMode.MOCK,
        source_label=f"mcp_backend:{manifest.id}",
        allowed_tools=_allowed_tools_from_env(),
    )
    mcp_server = build_mcp_server(registry, name=f"iiq-mcp-backend-{manifest.id}")
    return create_app(registry, mcp_server=mcp_server)


