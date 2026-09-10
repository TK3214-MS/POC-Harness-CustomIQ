"""Agent final-response contract shared by every industry pack and execution mode.

See docs/decisions/0005-agent-response-contract.md and instruction section 13.
"""
from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field

from iq_platform.contracts.capability import AdapterMode


class ExecutionMode(str, Enum):
    FULL_SAAS = "full_saas"
    HYBRID = "hybrid"
    LOCAL_PREVIEW = "local_preview"


class DocumentCitation(BaseModel):
    document_id: str
    title: str
    source_type: str
    source_uri: str | None = None
    citation: str
    retrieval_score: float | None = None
    adapter_mode: AdapterMode


class EntityRelationship(BaseModel):
    subject: str
    relationship: str
    object: str
    source: str | None = None


class MCPToolResultSummary(BaseModel):
    tool_name: str
    status: str
    summary: str
    adapter_mode: AdapterMode


class AgentResponse(BaseModel):
    """The 14-item response schema every agent must return, regardless of industry
    pack or execution mode. ``mock_or_simulation_disclosure`` and
    ``responsible_ai_notice`` are required fields on purpose - there is no way to
    construct a valid AgentResponse that omits them."""

    executive_summary: str
    confirmed_facts: list[str]
    data_sources_used: list[str]
    documents_and_citations: list[DocumentCitation] = Field(default_factory=list)
    entities_and_relationships: list[EntityRelationship] = Field(default_factory=list)
    mcp_tool_results: list[MCPToolResultSummary] = Field(default_factory=list)
    uncertainty_and_conflicts: list[str] = Field(default_factory=list)
    recommended_next_actions: list[str]
    human_in_the_loop_requirements: list[str]
    iq_layers_used: list[str]
    execution_mode: ExecutionMode
    mock_or_simulation_disclosure: str
    responsible_ai_notice: str
    trace_or_correlation_id: str
