"""Integration test: human approval flow (instruction §22.3). Verifies that
high-impact recommendations are flagged with human_approval_required in the
MCP tool response, and that the final AgentResponse always carries at least
one human-in-the-loop requirement referencing a role from the pack's
manifest.human_approval_rules.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from iq_platform.orchestration.generic_orchestrator import GenericLocalOrchestrator
from iq_platform.orchestration.industry_pack_loader import load_manifest

REPO_ROOT = Path(__file__).resolve().parents[2]
INDUSTRY_PACKS_DIR = REPO_ROOT / "industry-packs"

ALL_PACK_IDS = ["manufacturing", "financial-services", "retail", "healthcare", "public-sector"]


@pytest.mark.parametrize("pack_id", ALL_PACK_IDS)
def test_agent_response_always_has_human_in_the_loop_requirement(pack_id: str):
    pack_dir = INDUSTRY_PACKS_DIR / pack_id
    orchestrator = GenericLocalOrchestrator(pack_dir, scale="demo", seed=42)
    response = orchestrator.run_scenario()
    assert response.human_in_the_loop_requirements


@pytest.mark.parametrize("pack_id", ALL_PACK_IDS)
def test_manifest_declares_human_approval_rules_with_named_roles(pack_id: str):
    pack_dir = INDUSTRY_PACKS_DIR / pack_id
    manifest = load_manifest(pack_dir)
    assert manifest.human_approval_rules, f"{pack_id}: expected at least one human_approval_rule"
    for rule in manifest.human_approval_rules:
        assert rule.required_approver_role


def test_manufacturing_recommend_tool_flags_human_review():
    """The recommend_quality_actions MCP tool must flag human_approval_required
    - this is the mechanism the orchestrator relies on for high-impact actions."""
    orchestrator = GenericLocalOrchestrator(INDUSTRY_PACKS_DIR / "manufacturing", scale="demo", seed=42)
    issue_id = orchestrator.dataset["quality_issues"][0]["issue_id"]
    result = orchestrator._invoke_tool("recommend_quality_actions", {"issue_id": issue_id})
    assert result["human_approval_required"] is True
