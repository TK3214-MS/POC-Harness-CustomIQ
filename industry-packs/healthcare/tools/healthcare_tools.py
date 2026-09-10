"""Healthcare-specific MCP tools (Industry Pack plugin module).

Loaded dynamically by services/mcp-backend/mcp_backend/factory.py. See
docs/decisions/0010-industry-pack-plugin-loading.md.

These tools NEVER diagnose, decide treatment, or recommend medication - they
only retrieve and summarize synthetic case history data. See
industry-packs/healthcare/manifest.yaml prohibited_actions.
"""
from __future__ import annotations

from collections.abc import Callable


def get_synthetic_case_history(dataset: dict, params: dict) -> dict:
    patient_id = params["patient_id"]
    patient = next((p for p in dataset.get("patients", []) if p["patient_id"] == patient_id), None)
    if patient is None:
        return {"error": f"Patient {patient_id} not found"}
    encounters = [e for e in dataset.get("encounters", []) if e["patient_id"] == patient_id]
    encounter_ids = {e["encounter_id"] for e in encounters}
    events = [ev for ev in dataset.get("clinical_events", []) if ev["encounter_id"] in encounter_ids]
    return {"patient": patient, "encounters": encounters, "clinical_events": events}


def get_encounters(dataset: dict, params: dict) -> dict:
    patient_id = params["patient_id"]
    encounters = [e for e in dataset.get("encounters", []) if e["patient_id"] == patient_id]
    return {"encounters": encounters}


def get_treatment_timeline(dataset: dict, params: dict) -> dict:
    """Despite the name (matching instruction §11), this returns a chronological
    list of recorded ClinicalEvents only - it does not decide or recommend any
    treatment."""
    patient_id = params["patient_id"]
    encounters = [e for e in dataset.get("encounters", []) if e["patient_id"] == patient_id]
    encounter_ids = {e["encounter_id"] for e in encounters}
    events = sorted(
        (ev for ev in dataset.get("clinical_events", []) if ev["encounter_id"] in encounter_ids),
        key=lambda ev: ev["recorded_at"],
    )
    return {"timeline": events}


def identify_missing_case_information(dataset: dict, params: dict) -> dict:
    patient_id = params["patient_id"]
    encounters = [e for e in dataset.get("encounters", []) if e["patient_id"] == patient_id]
    encounter_ids = {e["encounter_id"] for e in encounters}
    events = [ev for ev in dataset.get("clinical_events", []) if ev["encounter_id"] in encounter_ids]
    event_types = {ev["event_type"] for ev in events}

    gaps = []
    if not encounters:
        gaps.append("No encounters on record for this patient.")
    if len(encounters) > 1 and "lab_test_ordered" not in event_types:
        gaps.append("No lab_test_ordered event found across multiple encounters - recommend confirming with the care team.")
    if "care_note_added" not in event_types:
        gaps.append("No care_note_added event found - recommend confirming documentation is complete.")
    if not gaps:
        gaps.append("No documentation gaps identified from available data.")
    return {"patient_id": patient_id, "gaps": gaps, "requires_human_review": True}


TOOL_FUNCTIONS: dict[str, Callable[[dict, dict], dict]] = {
    "get_synthetic_case_history": get_synthetic_case_history,
    "get_encounters": get_encounters,
    "get_treatment_timeline": get_treatment_timeline,
    "identify_missing_case_information": identify_missing_case_information,
}

TOOL_DESCRIPTIONS: dict[str, str] = {
    "get_synthetic_case_history": "Get a synthetic patient's encounters and clinical events.",
    "get_encounters": "Get a synthetic patient's encounters.",
    "get_treatment_timeline": "Get a chronological timeline of recorded clinical events (not a treatment decision).",
    "identify_missing_case_information": "Identify documentation gaps in a synthetic patient's case history.",
}
