"""Generic MCP tool registry and response wrapper shared by every tool."""
from __future__ import annotations

import uuid
from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any

from iq_platform.contracts.capability import AdapterMode
from iq_platform.contracts.mcp_tool import MCPToolResponse


class ToolRegistry:
    """Holds tool_name -> callable(dataset, params) -> dict mappings for one
    Industry Pack's MCP tools, plus a fixed dataset and adapter_mode."""

    def __init__(
        self,
        dataset: dict,
        tool_functions: dict[str, Callable[[dict, dict], dict]],
        descriptions: dict[str, str],
        adapter_mode: AdapterMode,
        source_label: str,
        allowed_tools: set[str] | None = None,
    ):
        self._dataset = dataset
        self._tool_functions = tool_functions
        self._descriptions = descriptions
        self._adapter_mode = adapter_mode
        self._source_label = source_label
        # Defense-in-depth allowlist (instruction §24). None means "allow every
        # tool this pack declares" - the pack's own TOOL_FUNCTIONS dict is
        # already a closed set, so this is only useful to further restrict it
        # (e.g. disabling a specific tool in a given deployment).
        self._allowed_tools = allowed_tools

    def list_tools(self) -> list[dict[str, str]]:
        return [
            {"tool_name": name, "description": desc}
            for name, desc in self._descriptions.items()
            if self._is_allowed(name)
        ]

    def _is_allowed(self, tool_name: str) -> bool:
        return self._allowed_tools is None or tool_name in self._allowed_tools

    def invoke(self, tool_name: str, params: dict[str, Any], correlation_id: str | None = None) -> MCPToolResponse:
        request_id = str(uuid.uuid4())
        correlation_id = correlation_id or request_id
        func = self._tool_functions.get(tool_name)

        if not self._is_allowed(tool_name):
            return MCPToolResponse(
                tool_name=tool_name,
                request_id=request_id,
                correlation_id=correlation_id,
                status="error",
                source=self._source_label,
                executed_at=datetime.now(UTC),
                adapter_mode=self._adapter_mode,
                errors=[f"Tool '{tool_name}' is not in the allowlist for this deployment"],
            )

        if func is None:
            return MCPToolResponse(
                tool_name=tool_name,
                request_id=request_id,
                correlation_id=correlation_id,
                status="error",
                source=self._source_label,
                executed_at=datetime.now(UTC),
                adapter_mode=self._adapter_mode,
                errors=[f"Unknown tool '{tool_name}'"],
            )

        try:
            data = func(self._dataset, params)
        except KeyError as exc:
            return MCPToolResponse(
                tool_name=tool_name,
                request_id=request_id,
                correlation_id=correlation_id,
                status="error",
                source=self._source_label,
                executed_at=datetime.now(UTC),
                adapter_mode=self._adapter_mode,
                errors=[f"Missing required parameter: {exc}"],
            )

        is_error = isinstance(data, dict) and "error" in data
        human_approval_required = bool(data.get("requires_human_review")) if isinstance(data, dict) else False
        return MCPToolResponse(
            tool_name=tool_name,
            request_id=request_id,
            correlation_id=correlation_id,
            status="error" if is_error else "ok",
            data=data if isinstance(data, dict) else {"result": data},
            source=self._source_label,
            provenance=[self._source_label],
            executed_at=datetime.now(UTC),
            adapter_mode=self._adapter_mode,
            warnings=[str(data.get("error"))] if is_error else [],
            human_approval_required=human_approval_required,
        )
