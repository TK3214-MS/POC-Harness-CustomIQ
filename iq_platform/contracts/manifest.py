"""Industry Pack manifest.yaml schema."""
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
    sample_data_path: str
    knowledge_path: str
    mcp_tools_path: str
    agent_instructions_path: str
    prohibited_actions: list[str] = Field(default_factory=list)
    human_approval_rules: list[HumanApprovalRule] = Field(default_factory=list)
