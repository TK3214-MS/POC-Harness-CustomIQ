"""MCP tool response contract shared by every generic and industry-specific MCP tool.

See docs/decisions/0006-mcp-tool-response-contract.md and instruction section 10.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from iq_platform.contracts.capability import AdapterMode


class MCPToolResponse(BaseModel):
    tool_name: str
    request_id: str
    correlation_id: str
    status: str
    data: dict[str, Any] = Field(default_factory=dict)
    source: str
    provenance: list[str] = Field(default_factory=list)
    executed_at: datetime
    adapter_mode: AdapterMode
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    human_approval_required: bool = False
