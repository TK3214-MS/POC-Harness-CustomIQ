"""FastAPI MCP Backend app factory.

See docs/decisions/0006-mcp-tool-response-contract.md and instruction §5.5/§10.
Every tool response - including errors - conforms to MCPToolResponse; the HTTP
status code is always 200 so clients always get the structured contract instead
of a generic HTTP error body.
"""
from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from iq_platform.contracts.mcp_tool import MCPToolResponse
from mcp_backend.registry import ToolRegistry


class ToolInvokeRequest(BaseModel):
    params: dict = {}
    correlation_id: str | None = None


def create_app(registry: ToolRegistry) -> FastAPI:
    app = FastAPI(title="Industry IQ Platform Accelerator - MCP Backend", version="0.1.0")

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok"}

    @app.get("/tools")
    def list_tools() -> list[dict[str, str]]:
        return registry.list_tools()

    @app.post("/tools/{tool_name}/invoke", response_model=MCPToolResponse)
    def invoke_tool(tool_name: str, request: ToolInvokeRequest) -> MCPToolResponse:
        return registry.invoke(tool_name, request.params, request.correlation_id)

    return app
