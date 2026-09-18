# MCP Security Guide

[![日本語](https://img.shields.io/badge/%E3%81%82-%E6%97%A5%E6%9C%AC%E8%AA%9E-5B6670?style=for-the-badge)](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/docs/mcp/MCP-Security-Guide.md) [![English](https://img.shields.io/badge/A-English-087F8C?style=for-the-badge)](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/docs/mcp/MCP-Security-Guide.en.md)

Authentication itself, which determines who can make requests, must be configured in the Azure environment that exposes the MCP Backend and in the Copilot Studio connection settings. This page describes MCP Backend security controls other than authentication.

## 1. Implemented Controls

### 1.1 `MCP_BACKEND_ALLOWED_TOOLS` Allowlist (Defense in Depth)

`services/mcp-backend/mcp_backend/factory.py::_allowed_tools_from_env()` reads the `MCP_BACKEND_ALLOWED_TOOLS` environment variable, a comma-separated list of tool names, and passes it to `ToolRegistry` as an allowlist.

```bash
# From .env.example
# Optional defense-in-depth allowlist of comma-separated tool names.
# When unset, allow all tools declared by the selected Industry Pack.
MCP_BACKEND_ALLOWED_TOOLS=
```

When unset or set to an empty string, all tools declared by the selected Industry Pack's `manifest.yaml`, through the `TOOL_FUNCTIONS` in the module referenced by `mcp_tools_path`, are allowed. This allowlist can only further restrict the set of tool names. It cannot allow a tool that the Pack does not declare because, after checking the allowlist, `ToolRegistry.invoke()` separately verifies that the tool name exists in the `tool_functions` dictionary. This behavior is verified by `test_tool_not_in_allowlist_is_rejected`, `test_tool_in_allowlist_is_permitted`, and `test_list_tools_respects_allowlist` in the [MCP tool safety test](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/tests/security/test_mcp_tool_safety.py).

### 1.2 Non-Root Container Execution

`deployment/containers/mcp-backend/Dockerfile` runs the application as a non-root user.

```dockerfile
RUN groupadd --gid 1000 iiq && useradd --uid 1000 --gid iiq --shell /usr/sbin/nologin --create-home iiq
...
USER iiq
```

### 1.3 Internal-Only Ingress by Default

`deployment/bicep/resources.bicep` configures Azure Container Apps ingress as internal-only by default (`external: false`).

```bicep
// Environment, and one Container App. Ingress is internal-only by default -
// flip to external only with explicit approval (see instruction section 24).
...
ingress: {
  external: false
```

Changing this setting to public access (`external: true`) is permitted only with explicit approval.

### 1.4 Host/Origin Allowlist for the MCP Protocol Endpoint (`/mcp`)

`services/mcp-backend/mcp_backend/mcp_protocol_server.py` enables the DNS rebinding protection provided by the official `mcp` SDK through `TransportSecuritySettings`. Add the actual deployment host name, such as the Container App FQDN, to the comma-separated `MCP_BACKEND_ALLOWED_HOSTS` environment variable. Even when this variable is unset, `localhost`/`127.0.0.1` on any port and `testserver`, the fixed host name used for tests, are always allowed. Requests with a Host header that is not allowed are rejected with `421 Misdirected Request`. See section 5 of the [MCP Design and Contract Guide](MCP-Design-and-Contract-Guide.md) for details.

## 2. Unimplemented Security Controls (Explicit Gaps)

The following controls are **not currently implemented**. They must be evaluated and implemented before a production deployment.

- **API authentication**: Authentication for inbound requests to the MCP Backend is not implemented. Configure an Azure authentication layer or the Copilot Studio connection authentication method before exposing the backend.
- **Dependency vulnerability scanning**: At the time this documentation was written, automated vulnerability scanning for Python packages used by `services/mcp-backend/` and Industry Pack code, such as `pip-audit` or an equivalent to Dependabot, had not been confirmed in this repository. If it is added to a CI workflow under `.github/workflows/`, update this page with the implementation details.
- **Prompt injection test suite**: A dedicated test suite that validates resistance to prompt injection against MCP tools and agent instructions has not yet been implemented.

Do not describe these controls as implemented in other documentation. When a control is implemented, update this guide and add a link to the corresponding test file.
