"""Mock Foundry IQ Adapter - reads synthetic knowledge documents from an
Industry Pack and returns citation-backed search results. See instruction §5.3.

`application_confidence` is an accelerator-derived value (combining retrieval
score and source count), NOT a native Microsoft confidence score.
"""
from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from iq_platform.contracts.adapter import (
    Adapter,
    AdapterCapabilities,
    AdapterDiagnostics,
    AdapterHealth,
)
from iq_platform.contracts.capability import AdapterMode

_SUPPORTED_OPERATIONS = ["search_knowledge", "get_document", "get_citations", "list_knowledge_bases"]


class MockKnowledgeAdapter(Adapter):
    def __init__(self, knowledge_dir: str | Path):
        self._knowledge_dir = Path(knowledge_dir)
        self._documents: list[dict[str, str]] = []
        if self._knowledge_dir.exists():
            for path in sorted(self._knowledge_dir.glob("*.md")):
                self._documents.append(
                    {
                        "document_id": path.stem,
                        "title": path.stem.replace("_", " ").title(),
                        "source_uri": f"mock://knowledge/{path.name}",
                        "content": path.read_text(encoding="utf-8"),
                    }
                )

    def health_check(self) -> AdapterHealth:
        healthy = len(self._documents) > 0
        return AdapterHealth(
            healthy=healthy,
            mode=self.mode,
            message=(
                f"{len(self._documents)} synthetic knowledge documents loaded"
                if healthy
                else f"No documents found in {self._knowledge_dir}"
            ),
            checked_at=datetime.now(UTC),
        )

    def capabilities(self) -> AdapterCapabilities:
        return AdapterCapabilities(
            adapter_name="mock_knowledge_adapter", supported_operations=_SUPPORTED_OPERATIONS, mode=self.mode
        )

    @property
    def mode(self) -> AdapterMode:
        return AdapterMode.MOCK

    def query(self, operation: str, parameters: dict[str, Any]) -> dict[str, Any]:
        if operation == "list_knowledge_bases":
            return {
                "knowledge_bases": [
                    {"knowledge_base_id": "manufacturing-knowledge", "document_count": len(self._documents)}
                ]
            }
        if operation == "get_document":
            document_id = parameters.get("document_id")
            doc = next((d for d in self._documents if d["document_id"] == document_id), None)
            return {"document": doc}
        if operation in ("search_knowledge", "get_citations"):
            return self._search(parameters.get("query", ""))
        return {"error": f"Unsupported operation '{operation}'", "results": []}

    def _search(self, query: str) -> dict[str, Any]:
        terms = [t.lower() for t in query.split() if t]
        results = []
        for doc in self._documents:
            content_lower = doc["content"].lower()
            hits = sum(content_lower.count(term) for term in terms) if terms else 0
            if terms and hits == 0:
                continue
            retrieval_score = min(1.0, (hits / max(1, len(terms))) / 5.0) if terms else 0.5
            excerpt_lines = doc["content"].strip().splitlines()[:3]
            results.append(
                {
                    "document_id": doc["document_id"],
                    "title": doc["title"],
                    "source_type": "markdown",
                    "source_uri": doc["source_uri"],
                    "content_excerpt": " ".join(line.strip() for line in excerpt_lines),
                    "citation": f"{doc['title']} (synthetic reference document)",
                    "retrieval_score": round(retrieval_score, 2),
                    "acl_tags": ["public-demo-synthetic"],
                    "retrieved_at": datetime.now(UTC).isoformat(),
                    "adapter_mode": self.mode.value,
                }
            )
        results.sort(key=lambda r: r["retrieval_score"], reverse=True)
        return {"results": results, "application_confidence": self._application_confidence(results)}

    def _application_confidence(self, results: list[dict[str, Any]]) -> float:
        """Accelerator-derived confidence, NOT a native Microsoft confidence score.
        Combines average retrieval score and source count (see instruction §5.3)."""
        if not results:
            return 0.0
        avg_score = sum(r["retrieval_score"] for r in results) / len(results)
        source_count_factor = min(1.0, len(results) / 3.0)
        return round((avg_score * 0.7) + (source_count_factor * 0.3), 2)

    def validate_configuration(self) -> AdapterDiagnostics:
        missing = [] if self._knowledge_dir.exists() else [f"knowledge dir: {self._knowledge_dir}"]
        return AdapterDiagnostics(
            adapter_name="mock_knowledge_adapter",
            mode=self.mode,
            configuration_valid=not missing,
            missing_configuration=missing,
        )

    def get_diagnostics(self) -> AdapterDiagnostics:
        return self.validate_configuration()
