"""Contract tests for iq_platform.contracts.manifest.IndustryPackManifest.

See docs/decisions/0004-industry-pack-manifest-schema.md.
"""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from iq_platform.contracts.manifest import HumanApprovalRule, IndustryPackManifest


def _valid_manifest_kwargs(**overrides):
    base = {
        "id": "manufacturing",
        "display_name": "Manufacturing",
        "version": "0.1.0",
        "description": "Manufacturing Quality Issue Investigation industry pack.",
        "default_scenario": "manufacturing-quality-issue-investigation",
        "ontology_path": "ontology/",
        "semantic_model_path": "semantic-model/",
        "sample_data_path": "data/",
        "knowledge_path": "knowledge/",
        "work_context_path": "work-context/",
        "mcp_tools_path": "tools/",
        "semantic_relationships_path": "semantics/pack_semantics.py",
        "scenario_module_path": "agents/scenario.py",
        "agent_instructions_path": "agents/",
        "demo_prompts_path": "prompts/",
        "expected_results_path": "expected-results/",
        "evaluation_path": "evaluations/",
        "terminology_path": "terminology/",
        "responsible_ai_path": "responsible-ai/",
    }
    base.update(overrides)
    return base


def test_minimal_valid_manifest_parses():
    manifest = IndustryPackManifest(**_valid_manifest_kwargs())
    assert manifest.id == "manufacturing"
    assert manifest.prohibited_actions == []
    assert manifest.human_approval_rules == []


def test_manifest_missing_required_field_raises():
    kwargs = _valid_manifest_kwargs()
    del kwargs["ontology_path"]
    with pytest.raises(ValidationError):
        IndustryPackManifest(**kwargs)


def test_manifest_with_prohibited_actions_and_approval_rules():
    kwargs = _valid_manifest_kwargs(
        prohibited_actions=["automatic account freeze", "automatic credit scoring"],
        human_approval_rules=[
            {
                "action": "freeze_account",
                "reason": "high impact, irreversible",
                "required_approver_role": "compliance_officer",
            }
        ],
    )
    manifest = IndustryPackManifest(**kwargs)
    assert manifest.prohibited_actions == ["automatic account freeze", "automatic credit scoring"]
    assert isinstance(manifest.human_approval_rules[0], HumanApprovalRule)
    assert manifest.human_approval_rules[0].required_approver_role == "compliance_officer"
