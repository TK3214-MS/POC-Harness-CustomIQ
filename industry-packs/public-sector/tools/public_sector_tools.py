"""Public Sector-specific MCP tools (Industry Pack plugin module).

Loaded dynamically by services/mcp-backend/mcp_backend/factory.py. See
docs/decisions/0010-industry-pack-plugin-loading.md.

Every function here is read-only / advisory. Nothing in this module approves,
denies, or closes a case automatically - see
industry-packs/public-sector/manifest.yaml prohibited_actions.
"""
from __future__ import annotations

from collections.abc import Callable


def _find(dataset: dict, entity_key: str, id_field: str, id_value: str) -> dict | None:
    return next((row for row in dataset.get(entity_key, []) if row[id_field] == id_value), None)


def get_case_history(dataset: dict, params: dict) -> dict:
    case_id = params["case_id"]
    case = _find(dataset, "cases", "case_id", case_id)
    if case is None:
        return {"error": f"Case {case_id} not found"}
    citizen = _find(dataset, "citizens", "citizen_id", case["citizen_id"])
    agency = _find(dataset, "agencies", "agency_id", case["agency_id"])
    applications = [a for a in dataset.get("applications", []) if a["case_id"] == case_id]
    return {"case": case, "citizen": citizen, "agency": agency, "applications": applications}


def get_application_status(dataset: dict, params: dict) -> dict:
    application_id = params["application_id"]
    application = _find(dataset, "applications", "application_id", application_id)
    if application is None:
        return {"error": f"Application {application_id} not found"}
    return {"application": application}


def get_related_agencies(dataset: dict, params: dict) -> dict:
    case_id = params["case_id"]
    case = _find(dataset, "cases", "case_id", case_id)
    if case is None:
        return {"error": f"Case {case_id} not found"}
    agency = _find(dataset, "agencies", "agency_id", case["agency_id"])
    return {"handling_agency": agency}


def recommend_review_steps(dataset: dict, params: dict) -> dict:
    case_id = params["case_id"]
    case = _find(dataset, "cases", "case_id", case_id)
    if case is None:
        return {"error": f"Case {case_id} not found"}
    applications = [a for a in dataset.get("applications", []) if a["case_id"] == case_id]
    recommendations = []
    if any(a["status"] == "pending_more_info" for a in applications):
        recommendations.append("At least one application is pending more information - recommend following up with the citizen.")
    if case["status"] == "pending_decision":
        recommendations.append("Case is pending decision - recommend case supervisor review before any decision is finalized.")
    recommendations.append("Do not approve, deny, or close this case automatically - human review required.")
    return {"case_id": case_id, "recommendations": recommendations, "requires_human_review": True}


TOOL_FUNCTIONS: dict[str, Callable[[dict, dict], dict]] = {
    "get_case_history": get_case_history,
    "get_application_status": get_application_status,
    "get_related_agencies": get_related_agencies,
    "recommend_review_steps": recommend_review_steps,
}

TOOL_DESCRIPTIONS: dict[str, str] = {
    "get_case_history": "Get a case's citizen, agency, and applications.",
    "get_application_status": "Get a single application's status.",
    "get_related_agencies": "Get the agency handling a case.",
    "recommend_review_steps": "Generate rule-based, human-reviewed recommendations for a case.",
}
