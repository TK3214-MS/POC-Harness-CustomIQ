"""Mock Fabric IQ Adapter - reads an Industry Pack's ontology + generated dataset
and answers entity/relationship queries. See instruction §5.4.

Relationship traversal and semantic measures are industry-specific, so they are
NOT hardcoded here - this adapter delegates to a pack-supplied
`relationships_module` (dynamically loaded from manifest.semantic_relationships_path,
see docs/decisions/0011-generic-orchestrator-and-semantic-adapter.md) exposing
`get_relationships(dataset, entity_type, entity_id) -> list[dict]` and
`get_metrics(dataset) -> dict`.
"""
from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from types import ModuleType
from typing import Any

import yaml

from iq_platform.contracts.adapter import (
    Adapter,
    AdapterCapabilities,
    AdapterDiagnostics,
    AdapterHealth,
)
from iq_platform.contracts.capability import AdapterMode

_SUPPORTED_OPERATIONS = ["list_entity_types", "search_entities", "get_entity", "get_relationships", "get_metrics"]


class MockSemanticAdapter(Adapter):
    def __init__(self, ontology_path: str | Path, dataset: dict[str, Any], relationships_module: ModuleType):
        self._ontology_path = Path(ontology_path)
        self._dataset = dataset
        self._relationships_module = relationships_module
        self._ontology: dict[str, Any] = {}
        if self._ontology_path.exists():
            with self._ontology_path.open("r", encoding="utf-8") as handle:
                self._ontology = yaml.safe_load(handle) or {}

    def health_check(self) -> AdapterHealth:
        healthy = bool(self._ontology.get("entity_types"))
        return AdapterHealth(
            healthy=healthy,
            mode=self.mode,
            message=(
                "Mock Fabric IQ ontology loaded" if healthy else f"Ontology not found/empty at {self._ontology_path}"
            ),
            checked_at=datetime.now(UTC),
        )

    def capabilities(self) -> AdapterCapabilities:
        return AdapterCapabilities(
            adapter_name="mock_semantic_adapter", supported_operations=_SUPPORTED_OPERATIONS, mode=self.mode
        )

    @property
    def mode(self) -> AdapterMode:
        return AdapterMode.MOCK

    def query(self, operation: str, parameters: dict[str, Any]) -> dict[str, Any]:
        if operation == "list_entity_types":
            return {"entity_types": self._ontology.get("entity_types", [])}
        if operation == "search_entities":
            return self._search_entities(parameters)
        if operation == "get_entity":
            return self._get_entity(parameters)
        if operation == "get_relationships":
            relationships = self._relationships_module.get_relationships(
                self._dataset, parameters.get("entity_type"), parameters.get("entity_id")
            )
            return {"relationships": relationships}
        if operation == "get_metrics":
            return {"semantic_measures": self._relationships_module.get_metrics(self._dataset)}
        return {"error": f"Unsupported operation '{operation}'"}

    def _entity_type_map(self) -> dict[str, tuple[str, str]]:
        """Derive {entity_type_name: (dataset_key, id_field)} from the ontology's
        declared entity_types (each entry names its own dataset_key), so
        search_entities/get_entity work generically for any Industry Pack."""
        mapping: dict[str, tuple[str, str]] = {}
        for entity_type in self._ontology.get("entity_types", []):
            name = entity_type.get("name")
            id_field = entity_type.get("identifier_field")
            dataset_key = entity_type.get("dataset_key")
            if name and id_field and dataset_key:
                mapping[name] = (dataset_key, id_field)
        return mapping

    def _search_entities(self, parameters: dict[str, Any]) -> dict[str, Any]:
        entity_type = parameters.get("entity_type")
        dataset_key, _ = self._entity_type_map().get(entity_type, (None, None))
        if dataset_key is None:
            return {"error": f"Unknown entity_type '{entity_type}'", "entities": []}
        return {"entities": self._dataset.get(dataset_key, [])[:50]}

    def _get_entity(self, parameters: dict[str, Any]) -> dict[str, Any]:
        entity_type = parameters.get("entity_type")
        entity_id = parameters.get("entity_id")
        dataset_key, id_field = self._entity_type_map().get(entity_type, (None, None))
        if dataset_key is None:
            return {"error": f"Unknown entity_type '{entity_type}'"}
        entity = next((row for row in self._dataset.get(dataset_key, []) if row[id_field] == entity_id), None)
        return {"entity": entity}

    def validate_configuration(self) -> AdapterDiagnostics:
        missing = [] if self._ontology_path.exists() else [f"ontology file: {self._ontology_path}"]
        return AdapterDiagnostics(
            adapter_name="mock_semantic_adapter",
            mode=self.mode,
            configuration_valid=not missing,
            missing_configuration=missing,
        )

    def get_diagnostics(self) -> AdapterDiagnostics:
        return self.validate_configuration()
