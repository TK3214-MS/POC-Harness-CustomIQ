"""Healthcare scenario runner (Industry Pack plugin module).

Loaded dynamically via manifest.scenario_module_path. Implements the
'Healthcare Case History Search' standard scenario (instruction §9.4). This
scenario NEVER diagnoses, decides treatment, or recommends medication.
"""
from __future__ import annotations

from typing import Any


def run_scenario(context: Any, entity_id: str | None = None) -> dict:
    dataset = context.dataset
    patient_id = entity_id or dataset["patients"][0]["patient_id"]
    patient = next(p for p in dataset["patients"] if p["patient_id"] == patient_id)

    work_context = context.work_context_adapter.query("search_messages", {"keywords": ["case_history"]})
    relationships_raw = context.semantic_adapter.query(
        "get_relationships", {"entity_type": "SyntheticPatient", "entity_id": patient_id}
    )
    knowledge_results = context.knowledge_adapter.query(
        "search_knowledge", {"query": "case history documentation completeness escalation"}
    )

    encounters = context.invoke_tool("get_encounters", {"patient_id": patient_id})
    timeline = context.invoke_tool("get_treatment_timeline", {"patient_id": patient_id})
    gaps = context.invoke_tool("identify_missing_case_information", {"patient_id": patient_id})

    encounter_count = len(encounters["data"].get("encounters", []))
    event_count = len(timeline["data"].get("timeline", []))

    confirmed_facts = [
        f"Synthetic patient {patient_id} (age band {patient['age_band']}) has {encounter_count} encounter(s) on record.",
        f"{event_count} clinical event(s) are recorded across those encounters.",
    ]

    uncertainty_and_conflicts = list(gaps["data"].get("gaps", []))
    if not work_context.get("results"):
        uncertainty_and_conflicts.append(
            "No related work context (messages/meetings) was found in the simulated fixtures for this patient."
        )

    mcp_tool_results = [
        {
            "tool_name": "get_encounters",
            "status": encounters["status"],
            "summary": f"{encounter_count} encounter(s) found.",
        },
        {
            "tool_name": "get_treatment_timeline",
            "status": timeline["status"],
            "summary": f"{event_count} clinical event(s) in chronological order.",
        },
        {
            "tool_name": "identify_missing_case_information",
            "status": gaps["status"],
            "summary": "; ".join(gaps["data"].get("gaps", [])),
        },
    ]

    return {
        "executive_summary": (
            f"Reviewed the synthetic case history for patient {patient_id}: {encounter_count} encounter(s) and "
            f"{event_count} clinical event(s) on record. This is a documentation review only, not a diagnosis."
        ),
        "confirmed_facts": confirmed_facts,
        "documents_and_citations": knowledge_results.get("results", []),
        "entities_and_relationships": relationships_raw.get("relationships", []),
        "mcp_tool_results": mcp_tool_results,
        "uncertainty_and_conflicts": uncertainty_and_conflicts,
        "recommended_next_actions": [
            "Recommend a clinician review the full timeline and documentation gaps identified above.",
        ],
        "human_in_the_loop_requirements": [
            "A qualified clinician must review this case history; this is not medical advice.",
            "This accelerator never diagnoses, decides treatment, or recommends medication.",
        ],
    }
