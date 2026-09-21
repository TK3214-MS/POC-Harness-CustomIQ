# MCP Backend Documentation Index

This folder contains documentation for the MCP Backend in `services/mcp-backend/`. The MCP Backend is an integration layer that exposes customer business systems as standardized tools and is implemented with FastAPI and the official MCP SDK.

## Documentation

- [MCP Design and Contract Guide](MCP-Design-and-Contract-Guide.md) - Describes the `MCPToolResponse` contract, `ToolRegistry` design, per-Industry Pack tool declarations, and the behavior of the `/health`, `/tools`, and `/tools/{tool_name}/invoke` endpoints.
- [MCP Security Guide](MCP-Security-Guide.md) - Describes the `MCP_BACKEND_ALLOWED_TOOLS` allowlist, non-root container execution, internal-only ingress by default, and the list of unimplemented security controls.

## Related Documentation

- [Production Environment Setup Guide](../Production-Environment-Setup.md) - Instructions for connecting Industry Pack tools to Copilot Studio
- [Troubleshooting](../troubleshooting/README.md) - Diagnosing `tools/list`, tool execution, and connection failures
