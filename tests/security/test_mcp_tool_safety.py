"""Security tests: MCP tool invocation safety (instruction §24 - unauthorized
tool invocation, input validation, tool allowlist).
"""
from __future__ import annotations

from mcp_backend.registry import ToolRegistry

from iq_platform.contracts.capability import AdapterMode


def _echo_tool(dataset: dict, params: dict) -> dict:
    return {"echo": params["message"]}


def _make_registry(allowed_tools=None) -> ToolRegistry:
    return ToolRegistry(
        dataset={},
        tool_functions={"echo": _echo_tool},
        descriptions={"echo": "Echoes a message back."},
        adapter_mode=AdapterMode.LIVE,
        source_label="test",
        allowed_tools=allowed_tools,
    )


def test_unknown_tool_name_is_rejected_with_structured_error():
    registry = _make_registry()
    response = registry.invoke("does_not_exist", {})
    assert response.status == "error"
    assert "Unknown tool" in response.errors[0]


def test_missing_required_parameter_is_rejected_not_crashed():
    registry = _make_registry()
    response = registry.invoke("echo", {})  # missing "message"
    assert response.status == "error"
    assert "Missing required parameter" in response.errors[0]


def test_tool_not_in_allowlist_is_rejected():
    registry = _make_registry(allowed_tools={"some_other_tool"})
    response = registry.invoke("echo", {"message": "hi"})
    assert response.status == "error"
    assert "not in the allowlist" in response.errors[0]


def test_tool_in_allowlist_is_permitted():
    registry = _make_registry(allowed_tools={"echo"})
    response = registry.invoke("echo", {"message": "hi"})
    assert response.status == "ok"
    assert response.data == {"echo": "hi"}


def test_list_tools_respects_allowlist():
    registry = _make_registry(allowed_tools={"some_other_tool"})
    assert registry.list_tools() == []
