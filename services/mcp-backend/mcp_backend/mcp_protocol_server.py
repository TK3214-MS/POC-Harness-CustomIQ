"""Real Model Context Protocol (MCP) server for the MCP Backend.

Built on the official `mcp` Python SDK's FastMCP. This is the endpoint used by
Microsoft Copilot Studio's MCP server connection flow.

This is NOT a replacement for the existing REST API in app.py
(/health, /tools, /tools/{name}/invoke) - that API predates this module, does
not speak the actual MCP JSON-RPC wire protocol, and is kept for this repo's
own internal use (CLI, tests). This module wraps the same ToolRegistry so both
surfaces stay behind one source of truth for tool behavior. See
docs/mcp/MCP-Design-and-Contract-Guide.md for the current contract.
"""
from __future__ import annotations

import os
from typing import Any

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

from mcp_backend.registry import ToolRegistry


def _transport_security_settings() -> TransportSecuritySettings:
    """Hosts/origins allowed to reach the MCP endpoint without tripping the
    SDK's built-in DNS-rebinding protection. MCP_BACKEND_ALLOWED_HOSTS
    (comma-separated) should list the real deployment hostname(s) once
    deployed (e.g. the Container App's FQDN). 'testserver' is always included
    because fastapi.testclient.TestClient always uses that fixed hostname
    internally - see tests/integration/test_mcp_protocol_server.py.
    'localhost:*'/'127.0.0.1:*' (any port) are always included for local
    development and scripts/demo/test_mcp_protocol_connectivity.py, which
    binds a real socket on a randomly chosen free port."""
    raw = os.environ.get("MCP_BACKEND_ALLOWED_HOSTS", "")
    hosts = {h.strip() for h in raw.split(",") if h.strip()}
    hosts |= {"localhost", "127.0.0.1", "localhost:*", "127.0.0.1:*", "testserver"}
    hosts_list = sorted(hosts)
    return TransportSecuritySettings(allowed_hosts=hosts_list, allowed_origins=hosts_list)


def build_mcp_server(registry: ToolRegistry, name: str) -> FastMCP:
    """Builds a FastMCP server exposing every tool `registry` currently allows
    (respecting MCP_BACKEND_ALLOWED_TOOLS, see registry.py) as a real MCP tool.

    Per-tool input schemas are a single generic 'params' object (no per-field
    typing) because the underlying tool functions accept an untyped params
    dict - this is an honest limitation, not a hidden one; see
    docs/mcp/MCP-Design-and-Contract-Guide.md.
    """
    server = FastMCP(name, transport_security=_transport_security_settings())
    # Mounted at "/mcp" by the caller (see app.py) - avoid a doubled "/mcp/mcp" path.
    server.settings.streamable_http_path = "/"

    for tool in registry.list_tools():
        _register_tool(server, registry, tool["tool_name"], tool["description"])

    return server


def _register_tool(server: FastMCP, registry: ToolRegistry, tool_name: str, description: str) -> None:
    def _handler(params: dict[str, Any] | None = None) -> dict:
        response = registry.invoke(tool_name, params or {})
        return response.model_dump(mode="json")

    _handler.__name__ = tool_name
    server.add_tool(_handler, name=tool_name, description=description)
