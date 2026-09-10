"""Industry Pack switching end-to-end tests (Phase 3 exit criteria, instruction
§26 Phase 3): each of the 5 packs' representative scenario runs successfully
through GenericLocalOrchestrator, and switching between packs requires no
change to iq_platform/ or services/mcp-backend/ code - only pack_dir changes.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from iq_platform.contracts.agent_response import ExecutionMode
from iq_platform.orchestration.generic_orchestrator import GenericLocalOrchestrator

REPO_ROOT = Path(__file__).resolve().parents[2]
INDUSTRY_PACKS_DIR = REPO_ROOT / "industry-packs"

ALL_PACK_IDS = ["manufacturing", "financial-services", "retail", "healthcare", "public-sector"]


@pytest.mark.parametrize("pack_id", ALL_PACK_IDS)
def test_each_industry_pack_representative_scenario_runs_e2e(pack_id: str):
    orchestrator = GenericLocalOrchestrator(INDUSTRY_PACKS_DIR / pack_id, scale="demo", seed=42)
    response = orchestrator.run_scenario()

    assert response.executive_summary
    assert response.confirmed_facts
    assert response.documents_and_citations, f"{pack_id}: expected at least one citation"
    assert response.entities_and_relationships, f"{pack_id}: expected at least one relationship"
    assert response.mcp_tool_results, f"{pack_id}: expected at least one MCP tool result"
    assert response.recommended_next_actions
    assert response.human_in_the_loop_requirements
    assert response.execution_mode == ExecutionMode.LOCAL_PREVIEW

    disclosure = response.mock_or_simulation_disclosure.lower()
    assert "synthetic" in disclosure and "mock" in disclosure and "simulated" in disclosure

    # responsible_ai_notice is loaded verbatim from the pack's responsible-ai/notice.md
    assert response.responsible_ai_notice
    assert "synthetic" in response.responsible_ai_notice.lower()


def test_switching_between_industry_packs_requires_no_shared_state():
    """Running Manufacturing then Financial Services back-to-back must not leak
    state between packs (e.g. via module-level caches) - each orchestrator
    instance is independent."""
    manufacturing = GenericLocalOrchestrator(INDUSTRY_PACKS_DIR / "manufacturing", scale="demo", seed=42)
    manufacturing_response = manufacturing.run_scenario()

    financial = GenericLocalOrchestrator(INDUSTRY_PACKS_DIR / "financial-services", scale="demo", seed=42)
    financial_response = financial.run_scenario()

    back_to_manufacturing = GenericLocalOrchestrator(INDUSTRY_PACKS_DIR / "manufacturing", scale="demo", seed=42)
    back_to_manufacturing_response = back_to_manufacturing.run_scenario()

    assert manufacturing_response.executive_summary != financial_response.executive_summary
    assert manufacturing_response.confirmed_facts == back_to_manufacturing_response.confirmed_facts
    assert manufacturing_response.data_sources_used == financial_response.data_sources_used
    assert manufacturing_response.iq_layers_used == financial_response.iq_layers_used


@pytest.mark.parametrize("pack_id", ["financial-services", "retail", "healthcare", "public-sector"])
def test_non_manufacturing_pack_prohibited_action_language_not_recommended(pack_id: str):
    """Spot-check that recommended actions never contain obviously prohibited
    verbs for each pack (freeze/deny/diagnose/approve-automatically etc.)."""
    orchestrator = GenericLocalOrchestrator(INDUSTRY_PACKS_DIR / pack_id, scale="demo", seed=42)
    response = orchestrator.run_scenario()
    joined = " ".join(response.recommended_next_actions).lower()
    for banned_phrase in ["automatically freeze", "automatically deny", "automatically diagnose", "automatically approve"]:
        assert banned_phrase not in joined
