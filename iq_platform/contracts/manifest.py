"""Industry Pack manifest.yaml schema.

See docs/decisions/0004-industry-pack-manifest-schema.md and instruction section 8.
"""
from __future__ import annotations

from pydantic import BaseModel, Field


class HumanApprovalRule(BaseModel):
    """One entry of manifest.yaml's human_approval_rules list."""

    action: str
    reason: str
    required_approver_role: str | None = None


class IndustryPackManifest(BaseModel):
    id: str
    display_name: str
    version: str
    description: str
    default_scenario: str
    ontology_path: str
    semantic_model_path: str
    sample_data_path: str
    knowledge_path: str
    work_context_path: str
    mcp_tools_path: str
    # Pack-specific Fabric IQ mock relationship/metrics logic - see ADR-0011.
    # Keeps iq_platform.adapters.semantic.mock_adapter fully industry-agnostic.
    semantic_relationships_path: str
    # Pack-specific scenario runner (executive summary, tool call sequence,
    # human-in-the-loop text) - see ADR-0011. Keeps the Orchestrator generic.
    scenario_module_path: str
    agent_instructions_path: str
    demo_prompts_path: str
    expected_results_path: str
    evaluation_path: str
    terminology_path: str
    responsible_ai_path: str
    prohibited_actions: list[str] = Field(default_factory=list)
    human_approval_rules: list[HumanApprovalRule] = Field(default_factory=list)
