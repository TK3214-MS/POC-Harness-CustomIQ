"""Contract tests for iq_platform.contracts.agent_response.AgentResponse.

See docs/decisions/0005-agent-response-contract.md.
"""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from iq_platform.contracts.agent_response import AgentResponse


def _valid_kwargs(**overrides):
    base = {
        "executive_summary": "Investigated a synthetic quality issue across two factories.",
        "confirmed_facts": ["Quality issue QI-1 affects Part P-42."],
        "data_sources_used": ["mock_knowledge_adapter", "mock_semantic_adapter"],
        "documents_and_citations": [],
        "entities_and_relationships": [],
        "mcp_tool_results": [],
        "uncertainty_and_conflicts": ["Root cause not yet confirmed by engineering."],
        "recommended_next_actions": ["Escalate to engineering change review."],
        "human_in_the_loop_requirements": ["Engineer must approve recommended action."],
        "iq_layers_used": ["Foundry IQ (mock)", "Fabric IQ (mock)"],
        "execution_mode": "local_preview",
        "mock_or_simulation_disclosure": "All data in this response is synthetic; adapters ran in mock mode.",
        "responsible_ai_notice": "This is not a substitute for engineering judgment.",
        "trace_or_correlation_id": "trace-123",
    }
    base.update(overrides)
    return base


def test_valid_agent_response_parses():
    response = AgentResponse(**_valid_kwargs())
    assert response.execution_mode == "local_preview"


def test_agent_response_requires_mock_disclosure_field():
    kwargs = _valid_kwargs()
    del kwargs["mock_or_simulation_disclosure"]
    with pytest.raises(ValidationError):
        AgentResponse(**kwargs)


def test_agent_response_requires_responsible_ai_notice_field():
    kwargs = _valid_kwargs()
    del kwargs["responsible_ai_notice"]
    with pytest.raises(ValidationError):
        AgentResponse(**kwargs)


def test_agent_response_rejects_unknown_execution_mode():
    kwargs = _valid_kwargs(execution_mode="production")
    with pytest.raises(ValidationError):
        AgentResponse(**kwargs)
