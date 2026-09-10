"""Shared Pydantic contracts used across the platform, MCP backend, and industry packs.

See docs/decisions/0003-adapter-contract-and-mode-enum.md,
docs/decisions/0004-industry-pack-manifest-schema.md,
docs/decisions/0005-agent-response-contract.md,
docs/decisions/0006-mcp-tool-response-contract.md, and
docs/decisions/0007-capability-registry-authority.md.
"""
from iq_platform.contracts.adapter import (
    Adapter,
    AdapterCapabilities,
    AdapterDiagnostics,
    AdapterHealth,
)
from iq_platform.contracts.agent_response import (
    AgentResponse,
    DocumentCitation,
    EntityRelationship,
    ExecutionMode,
    MCPToolResultSummary,
)
from iq_platform.contracts.capability import (
    AdapterMode,
    Capability,
    CapabilityRegistry,
    CapabilityStatus,
)
from iq_platform.contracts.manifest import HumanApprovalRule, IndustryPackManifest
from iq_platform.contracts.mcp_tool import MCPToolResponse

__all__ = [
    "Adapter",
    "AdapterCapabilities",
    "AdapterDiagnostics",
    "AdapterHealth",
    "AdapterMode",
    "AgentResponse",
    "Capability",
    "CapabilityRegistry",
    "CapabilityStatus",
    "DocumentCitation",
    "EntityRelationship",
    "ExecutionMode",
    "HumanApprovalRule",
    "IndustryPackManifest",
    "MCPToolResponse",
    "MCPToolResultSummary",
]
