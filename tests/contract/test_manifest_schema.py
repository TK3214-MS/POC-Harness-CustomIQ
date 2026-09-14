"""Contract tests for iq_platform.contracts.manifest.IndustryPackManifest."""
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
        "sample_data_path": "data/",
        "knowledge_path": "knowledge/",
        "mcp_tools_path": "tools/",
        "agent_instructions_path": "agents/",
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
