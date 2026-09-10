"""Healthcare Fabric IQ relationship/metrics logic (Industry Pack plugin
module). Loaded dynamically via manifest.semantic_relationships_path - see
docs/decisions/0011-generic-orchestrator-and-semantic-adapter.md.
"""
from __future__ import annotations

from typing import Any


def get_relationships(dataset: dict, entity_type: str | None, entity_id: str | None) -> list[dict[str, str]]:
    relationships: list[dict[str, str]] = []

    if entity_type == "SyntheticPatient":
        for encounter in dataset.get("encounters", []):
            if encounter["patient_id"] == entity_id:
                relationships.append(
                    {"subject": encounter["encounter_id"], "relationship": "involves", "object": entity_id}
                )
    elif entity_type == "Encounter":
        encounter = next((e for e in dataset.get("encounters", []) if e["encounter_id"] == entity_id), None)
        if encounter:
            relationships.append(
                {"subject": entity_id, "relationship": "attendedBy", "object": encounter["provider_id"]}
            )
            for event in dataset.get("clinical_events", []):
                if event["encounter_id"] == entity_id:
                    relationships.append(
                        {"subject": event["event_id"], "relationship": "occursDuring", "object": entity_id}
                    )

    return relationships


def get_metrics(dataset: dict) -> dict[str, Any]:
    encounters = dataset.get("encounters", [])
    events = dataset.get("clinical_events", [])
    avg_events_per_encounter = round(len(events) / len(encounters), 2) if encounters else 0.0
    return {"encounter_count": len(encounters), "average_events_per_encounter": avg_events_per_encounter}
