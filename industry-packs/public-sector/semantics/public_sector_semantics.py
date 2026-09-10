"""Public Sector Fabric IQ relationship/metrics logic (Industry Pack plugin
module). Loaded dynamically via manifest.semantic_relationships_path - see
docs/decisions/0011-generic-orchestrator-and-semantic-adapter.md.
"""
from __future__ import annotations

from typing import Any


def get_relationships(dataset: dict, entity_type: str | None, entity_id: str | None) -> list[dict[str, str]]:
    relationships: list[dict[str, str]] = []

    if entity_type == "Case":
        case = next((c for c in dataset.get("cases", []) if c["case_id"] == entity_id), None)
        if case:
            relationships.append({"subject": entity_id, "relationship": "involves", "object": case["citizen_id"]})
            relationships.append({"subject": entity_id, "relationship": "handledBy", "object": case["agency_id"]})
            for application in dataset.get("applications", []):
                if application["case_id"] == entity_id:
                    relationships.append(
                        {"subject": application["application_id"], "relationship": "partOf", "object": entity_id}
                    )
    elif entity_type == "SyntheticCitizen":
        for case in dataset.get("cases", []):
            if case["citizen_id"] == entity_id:
                relationships.append({"subject": case["case_id"], "relationship": "involves", "object": entity_id})

    return relationships


def get_metrics(dataset: dict) -> dict[str, Any]:
    cases = dataset.get("cases", [])
    pending_decision_count = sum(1 for c in cases if c["status"] == "pending_decision")
    return {"case_count": len(cases), "pending_decision_count": pending_decision_count}
