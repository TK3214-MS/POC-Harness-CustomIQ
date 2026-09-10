"""Generic Local Orchestrator - Local Preview Mode's stand-in for the GitHub
Copilot harness / Copilot Studio. Works for ANY Industry Pack that follows the
plugin contract (data generator, MCP tools, semantic relationships, scenario
runner). Contains no industry-specific logic itself - see
docs/decisions/0010-industry-pack-plugin-loading.md and
docs/decisions/0011-generic-orchestrator-and-semantic-adapter.md.

See docs/decisions/0005-agent-response-contract.md and instruction §14.3.
"""
from __future__ import annotations

import uuid
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient

from iq_platform.adapters.knowledge.mock_adapter import MockKnowledgeAdapter
from iq_platform.adapters.semantic.mock_adapter import MockSemanticAdapter
from iq_platform.adapters.work_context.simulated_adapter import SimulatedWorkContextAdapter
from iq_platform.contracts.agent_response import (
    AgentResponse,
    DocumentCitation,
    EntityRelationship,
    ExecutionMode,
    MCPToolResultSummary,
)
from iq_platform.contracts.capability import AdapterMode
from iq_platform.contracts.manifest import IndustryPackManifest
from iq_platform.observability.logging_config import get_logger
from iq_platform.orchestration.industry_pack_loader import load_manifest, load_plugin_module

logger = get_logger(__name__)

MOCK_DISCLOSURE = (
    "Local Preview Mode: all data in this response is synthetic. Work IQ ran in "
    "simulated mode; Foundry IQ and Fabric IQ ran in mock mode; the MCP Backend "
    "served mock data. Nothing here reflects a real Microsoft SaaS environment. "
    "See docs/decisions/product-verification.md."
)

DATA_SOURCES_USED = [
    "simulated_work_context_adapter",
    "mock_knowledge_adapter",
    "mock_semantic_adapter",
    "mcp_backend (mock)",
]
IQ_LAYERS_USED = ["Work IQ (simulated)", "Foundry IQ (mock)", "Fabric IQ (mock)", "MCP Backend (mock)"]


@dataclass
class OrchestrationContext:
    """Passed to a pack's scenario_module_path plugin's run_scenario(), so it can
    freely call whichever adapters/tools its own scenario needs."""

    dataset: dict[str, Any]
    work_context_adapter: SimulatedWorkContextAdapter
    knowledge_adapter: MockKnowledgeAdapter
    semantic_adapter: MockSemanticAdapter
    invoke_tool: Callable[[str, dict[str, Any]], dict[str, Any]]


class GenericLocalOrchestrator:
    """Works for any Industry Pack; contains no industry-specific logic."""

    def __init__(self, pack_dir: str | Path, scale: str = "demo", seed: int = 42):
        self.pack_dir = Path(pack_dir)
        self.manifest: IndustryPackManifest = load_manifest(self.pack_dir)

        generator_module = load_plugin_module(self.pack_dir / self.manifest.sample_data_path)
        self.dataset = generator_module.generate_dataset(seed=seed, scale=scale)

        relationships_module = load_plugin_module(self.pack_dir / self.manifest.semantic_relationships_path)
        self._scenario_module = load_plugin_module(self.pack_dir / self.manifest.scenario_module_path)

        self.work_context_adapter = SimulatedWorkContextAdapter(self.pack_dir / self.manifest.work_context_path)
        self.knowledge_adapter = MockKnowledgeAdapter(self.pack_dir / self.manifest.knowledge_path)
        self.semantic_adapter = MockSemanticAdapter(
            self.pack_dir / self.manifest.ontology_path, self.dataset, relationships_module
        )

        # Local import: keeps the MCP Backend an optional dependency for callers
        # that only need the Adapters (e.g. a future 'health' check).
        from mcp_backend.factory import build_app

        app = build_app(self.dataset, self.pack_dir, self.manifest)
        self._mcp_client = TestClient(app)

        responsible_ai_path = self.pack_dir / self.manifest.responsible_ai_path
        self._responsible_ai_notice = (
            responsible_ai_path.read_text(encoding="utf-8").strip()
            if responsible_ai_path.exists()
            else "No Responsible AI notice found for this Industry Pack."
        )

    def _invoke_tool(self, tool_name: str, params: dict) -> dict:
        response = self._mcp_client.post(f"/tools/{tool_name}/invoke", json={"params": params})
        response.raise_for_status()
        return response.json()

    def run_scenario(self, entity_id: str | None = None) -> AgentResponse:
        trace_id = str(uuid.uuid4())
        logger.info(f"Starting {self.manifest.default_scenario}", extra={"correlation_id": trace_id})

        context = OrchestrationContext(
            dataset=self.dataset,
            work_context_adapter=self.work_context_adapter,
            knowledge_adapter=self.knowledge_adapter,
            semantic_adapter=self.semantic_adapter,
            invoke_tool=self._invoke_tool,
        )
        result = self._scenario_module.run_scenario(context, entity_id)

        documents_and_citations = [
            DocumentCitation(
                document_id=r["document_id"],
                title=r["title"],
                source_type=r["source_type"],
                source_uri=r.get("source_uri"),
                citation=r["citation"],
                retrieval_score=r.get("retrieval_score"),
                adapter_mode=AdapterMode.MOCK,
            )
            for r in result.get("documents_and_citations", [])
        ]
        entities_and_relationships = [
            EntityRelationship(
                subject=rel["subject"],
                relationship=rel["relationship"],
                object=rel["object"],
                source="mock_semantic_adapter",
            )
            for rel in result.get("entities_and_relationships", [])
        ]
        mcp_tool_results = [
            MCPToolResultSummary(
                tool_name=r["tool_name"], status=r["status"], summary=r["summary"], adapter_mode=AdapterMode.MOCK
            )
            for r in result.get("mcp_tool_results", [])
        ]

        response = AgentResponse(
            executive_summary=result["executive_summary"],
            confirmed_facts=result.get("confirmed_facts", []),
            data_sources_used=DATA_SOURCES_USED,
            documents_and_citations=documents_and_citations,
            entities_and_relationships=entities_and_relationships,
            mcp_tool_results=mcp_tool_results,
            uncertainty_and_conflicts=result.get("uncertainty_and_conflicts", []),
            recommended_next_actions=result.get("recommended_next_actions", []),
            human_in_the_loop_requirements=result.get("human_in_the_loop_requirements", []),
            iq_layers_used=IQ_LAYERS_USED,
            execution_mode=ExecutionMode.LOCAL_PREVIEW,
            mock_or_simulation_disclosure=MOCK_DISCLOSURE,
            responsible_ai_notice=self._responsible_ai_notice,
            trace_or_correlation_id=trace_id,
        )
        logger.info(f"Completed {self.manifest.default_scenario}", extra={"correlation_id": trace_id})
        return response
