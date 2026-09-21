# MCP Design and Contract Guide

## 1. MCPToolResponse Contract

Every MCP tool returns the shared response type `iq_platform.contracts.mcp_tool.MCPToolResponse`, a Pydantic model. Its fields are as follows.

| Field | Type | Description |
| --- | --- | --- |
| `tool_name` | `str` | Name of the invoked tool. |
| `request_id` | `str` | ID unique to this request. A UUID is generated automatically when omitted. |
| `correlation_id` | `str` | Correlation ID propagated from the caller. Defaults to the same value as `request_id` when omitted. |
| `status` | `str` | `"ok"` or `"error"`. |
| `data` | `dict[str, Any]` | Tool execution result payload. |
| `source` | `str` | Response source label, for example `mcp_backend:manufacturing`. |
| `provenance` | `list[str]` | Data provenance information. |
| `executed_at` | `datetime` | Execution time in UTC. |
| `adapter_mode` | `AdapterMode` | `live` or `unavailable`. Indicates the execution state of the production MCP Backend. |
| `warnings` | `list[str]` | List of warning messages. |
| `errors` | `list[str]` | List of error messages. |
| `human_approval_required` | `bool` | Whether human approval is required to perform this action. |

Destructive or high-impact operations are represented by returning `human_approval_required=True` without performing the operation, in accordance with instruction section 10.

## 2. ToolRegistry Design

`services/mcp_backend/mcp_backend/registry.py::ToolRegistry` ([implementation](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/services/mcp-backend/mcp_backend/registry.py)) stores the tools exposed by one Industry Pack and provides shared invocation processing.

- The constructor accepts `dataset` (synthetic dataset), `tool_functions` (a `tool_name -> Callable[[dataset, params], dict]` dictionary), `descriptions`, `adapter_mode`, `source_label`, and an optional `allowed_tools` allowlist. See the [MCP Security Guide](MCP-Security-Guide.md).
- `list_tools()` returns the list of tools filtered by the allowlist.
- `invoke(tool_name, params, correlation_id=None)` performs the following checks in order and returns an `MCPToolResponse` **without raising an exception in any branch**.
  1. Tool name not included in the allowlist: `status="error"`, `errors=["Tool '...' is not in the allowlist for this deployment"]`.
  2. Unknown tool name: `status="error"`, `errors=["Unknown tool '...'"]`.
  3. A `KeyError` raised while calling the tool function, indicating a missing required parameter, is caught: `status="error"`, `errors=["Missing required parameter: ..."]`.
  4. If the `dict` returned by the tool function contains an `"error"` key: `status="error"`.
  5. Otherwise: `status="ok"`.

This design prevents unknown or invalid tool calls from crashing the service or exposing raw exceptions. It is verified by the [MCP tool safety test](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/tests/security/test_mcp_tool_safety.py) and the [MCP Backend integration test](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/tests/integration/test_mcp_backend_integration.py).

## 3. Declaring Tools for Each Industry Pack

The `mcp_tools_path` in each Industry Pack's `manifest.yaml` identifies the tool implementation module. The `industry_pack_loader` dynamically loads this module at runtime, and the module exposes `TOOL_FUNCTIONS` and `TOOL_DESCRIPTIONS`.

- `TOOL_FUNCTIONS: dict[str, Callable[[dict, dict], dict]]`
- `TOOL_DESCRIPTIONS: dict[str, str]`

`services/mcp-backend/mcp_backend/factory.py::build_app()` reads these values and constructs the `ToolRegistry`, so the code in `services/mcp-backend/` contains no industry-specific logic.

## 4. HTTP Endpoints (REST API for Internal Use by This Backend)

`services/mcp-backend/mcp_backend/app.py::create_app()` constructs a FastAPI application that exposes the following three endpoints.

- `GET /health` - A basic health check that returns `{"status": "ok"}`.
- `GET /tools` - Returns the tool list currently filtered by the allowlist as an array of `tool_name`/`description` dictionaries.
- `POST /tools/{tool_name}/invoke` - Accepts `{"params": {...}, "correlation_id": "..."}` and returns the `MCPToolResponse` produced by `ToolRegistry.invoke()` as the `response_model`.

As an important design decision, **tool invocation responses always use HTTP 200**. Even on error, the response is a structured `MCPToolResponse` body with `status="error"`, rather than a raw HTTP error (4xx/5xx). This allows callers to parse every response using the same contract. This behavior is verified by `test_invoke_unknown_tool_returns_structured_error_not_http_error` in the [integration test](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/tests/integration/test_mcp_backend_integration.py).

**Note**: The REST API in this section does not conform to the actual Model Context Protocol wire format, which uses a JSON-RPC 2.0-based `initialize`/`tools/list`/`tools/call` handshake. It is a custom API used only internally by this repository's CLI and tests. It will not be removed, but external MCP clients such as Copilot Studio cannot connect to this REST API. External clients connect to the endpoint described in section 5.

## 5. Protocol-Compliant MCP Server (`/mcp` for External MCP Clients)

The GitHub Copilot harness in Microsoft Copilot Studio can connect to an MCP server through the "Add MCP server" flow. This backend exposes a protocol-compliant server implemented with the official MCP Python SDK at `/mcp` and delegates to the same `ToolRegistry`.

- **Rationale for the implementation language**: The implementation preserves the existing Python 3.11+ architecture and uses the official MCP Python SDK.
- **Tool input schemas**: Each tool function accepts an untyped `params: dict`, so the exposed JSON Schema is also a permissive schema equivalent to `{"type": "object", "additionalProperties": true}`. Individual fields are not typed. This is an explicit limitation. Defining strict schemas for each tool in the future will require extensions to each Industry Pack's `tools/*.py` implementation.
- **Host allowlist**: The `mcp` SDK validates Host and Origin headers to protect against DNS rebinding. Add the actual deployment host names to the comma-separated `MCP_BACKEND_ALLOWED_HOSTS` environment variable. `localhost`/`127.0.0.1` on any port and `testserver`, the fixed host name used by `fastapi.testclient.TestClient`, are always allowed. See the [MCP Security Guide](MCP-Security-Guide.md) for details.
- **Validation**:
  - [MCP protocol integration test](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/tests/integration/test_mcp_protocol_server.py) - Sends raw JSON-RPC requests (`initialize` -> `notifications/initialized` -> `tools/list` -> `tools/call`) through `fastapi.testclient.TestClient`. This has been validated in-process for all five industries and runs quickly.
  - **Not performed**: Connection testing against this `/mcp` endpoint from an actual Microsoft Copilot Studio environment has not been performed because no such environment is available. The validation above demonstrates that an MCP client based on the official SDK can complete the handshake correctly; it does not guarantee the behavior of Copilot Studio's own implementation.
