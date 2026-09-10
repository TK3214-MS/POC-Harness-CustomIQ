"""Public Sector scenario runner (Industry Pack plugin module).

Loaded dynamically via manifest.scenario_module_path. Implements the 'Public
Sector Case Investigation' standard scenario (instruction §9.5).
"""
from __future__ import annotations

from typing import Any


def run_scenario(context: Any, entity_id: str | None = None) -> dict:
    dataset = context.dataset
    case_id = entity_id or dataset["cases"][0]["case_id"]
    case = next(c for c in dataset["cases"] if c["case_id"] == case_id)

    work_context = context.work_context_adapter.query("search_messages", {"keywords": ["case", "application"]})
    relationships_raw = context.semantic_adapter.query(
        "get_relationships", {"entity_type": "Case", "entity_id": case_id}
    )
    knowledge_results = context.knowledge_adapter.query(
        "search_knowledge", {"query": "case review application handling referral"}
    )

    case_history = context.invoke_tool("get_case_history", {"case_id": case_id})
    related_agencies = context.invoke_tool("get_related_agencies", {"case_id": case_id})
    recommendations = context.invoke_tool("recommend_review_steps", {"case_id": case_id})

    agency = related_agencies["data"].get("handling_agency") or {}
    applications = case_history["data"].get("applications", [])

    confirmed_facts = [
        f"Case {case_id} ({case['case_type']}) was opened on {case['opened_at']} with status '{case['status']}'.",
        f"Case is handled by {agency.get('name', case['agency_id'])}.",
        f"{len(applications)} application(s) are on record for this case.",
    ]

    uncertainty_and_conflicts = []
    if any(a["status"] == "pending_more_info" for a in applications):
        uncertainty_and_conflicts.append("At least one application is pending more information from the citizen.")
    if not work_context.get("results"):
        uncertainty_and_conflicts.append(
            "No related work context (messages/meetings) was found in the simulated fixtures for this case."
        )

    mcp_tool_results = [
        {
            "tool_name": "get_case_history",
            "status": case_history["status"],
            "summary": f"{len(applications)} application(s) found for case {case_id}.",
        },
        {
            "tool_name": "get_related_agencies",
            "status": related_agencies["status"],
            "summary": f"Handled by {agency.get('name', 'unknown agency')}.",
        },
        {
            "tool_name": "recommend_review_steps",
            "status": recommendations["status"],
            "summary": "; ".join(recommendations["data"].get("recommendations", [])),
        },
    ]

    return {
        "executive_summary": (
            f"Investigated case {case_id} ({case['case_type']}, status: {case['status']}) handled by "
            f"{agency.get('name', case['agency_id'])}."
        ),
        "confirmed_facts": confirmed_facts,
        "documents_and_citations": knowledge_results.get("results", []),
        "entities_and_relationships": relationships_raw.get("relationships", []),
        "mcp_tool_results": mcp_tool_results,
        "uncertainty_and_conflicts": uncertainty_and_conflicts,
        "recommended_next_actions": recommendations["data"].get("recommendations", []),
        "human_in_the_loop_requirements": [
            "A case officer must review this case; a case supervisor must approve any decision.",
            "This accelerator never automatically approves, denies, or closes a case, and never ranks citizens by risk.",
        ],
    }
