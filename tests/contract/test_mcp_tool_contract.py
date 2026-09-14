"""Contract tests for iq_platform.contracts.mcp_tool.MCPToolResponse."""
from __future__ import annotations

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from iq_platform.contracts.capability import AdapterMode
from iq_platform.contracts.mcp_tool import MCPToolResponse


def test_mcp_tool_response_round_trips_through_json():
    response = MCPToolResponse(
        tool_name="search_quality_issues",
        request_id="req-1",
        correlation_id="corr-1",
        status="ok",
        data={"issues": []},
        source="mock:manufacturing",
        provenance=["mock-data-set-v1"],
        executed_at=datetime.now(UTC),
        adapter_mode=AdapterMode.LIVE,
        warnings=[],
        errors=[],
        human_approval_required=False,
    )
    payload = response.model_dump(mode="json")
    restored = MCPToolResponse.model_validate(payload)
    assert restored.tool_name == "search_quality_issues"
    assert restored.adapter_mode == AdapterMode.LIVE


def test_mcp_tool_response_requires_core_fields():
    with pytest.raises(ValidationError):
        MCPToolResponse.model_validate({"tool_name": "x"})


def test_mcp_tool_response_defaults_human_approval_to_false():
    response = MCPToolResponse(
        tool_name="get_case_history",
        request_id="req-2",
        correlation_id="corr-2",
        status="ok",
        source="mock:public-sector",
        executed_at=datetime.now(UTC),
        adapter_mode=AdapterMode.LIVE,
    )
    assert response.human_approval_required is False
    assert response.data == {}
