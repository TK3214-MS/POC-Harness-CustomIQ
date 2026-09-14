"""Manufacturing-specific MCP tools (Industry Pack plugin module).

Loaded dynamically by services/mcp-backend/mcp_backend/factory.py - not imported
as a dotted package (industry-packs/ is not a valid Python package name).

Every function here is read-only / advisory. Nothing in this module closes a
quality issue or approves an engineering change automatically - see
industry-packs/manufacturing/manifest.yaml human_approval_rules.
"""
from __future__ import annotations

from collections.abc import Callable


def _find(dataset: dict, entity_key: str, id_field: str, id_value: str) -> dict | None:
    return next((row for row in dataset.get(entity_key, []) if row[id_field] == id_value), None)


def search_quality_issues(dataset: dict, params: dict) -> dict:
    issues = dataset.get("quality_issues", [])
    part_id = params.get("part_id")
    factory_id = params.get("factory_id")
    status = params.get("status")
    results = [
        issue
        for issue in issues
        if (part_id is None or issue["part_id"] == part_id)
        and (factory_id is None or issue["factory_id"] == factory_id)
        and (status is None or issue["status"] == status)
    ]
    return {"quality_issues": results[:50], "total_matches": len(results)}


def get_part_traceability(dataset: dict, params: dict) -> dict:
    part_id = params["part_id"]
    part = _find(dataset, "parts", "part_id", part_id)
    if part is None:
        return {"error": f"Part {part_id} not found"}
    supplier = _find(dataset, "suppliers", "supplier_id", part["supplier_id"])
    lines = [line for line in dataset.get("production_lines", []) if line["line_id"] in part["used_in_line_ids"]]
    return {"part": part, "supplier": supplier, "used_in_lines": lines}


def get_supplier_history(dataset: dict, params: dict) -> dict:
    supplier_id = params["supplier_id"]
    supplier = _find(dataset, "suppliers", "supplier_id", supplier_id)
    if supplier is None:
        return {"error": f"Supplier {supplier_id} not found"}
    parts = [p for p in dataset.get("parts", []) if p["supplier_id"] == supplier_id]
    part_ids = {p["part_id"] for p in parts}
    related_issues = [qi for qi in dataset.get("quality_issues", []) if qi["part_id"] in part_ids]
    return {"supplier": supplier, "parts_supplied": parts, "related_quality_issues": related_issues}


def get_factory_context(dataset: dict, params: dict) -> dict:
    factory_id = params["factory_id"]
    factory = _find(dataset, "factories", "factory_id", factory_id)
    if factory is None:
        return {"error": f"Factory {factory_id} not found"}
    lines = [line for line in dataset.get("production_lines", []) if line["factory_id"] == factory_id]
    issues = [qi for qi in dataset.get("quality_issues", []) if qi["factory_id"] == factory_id]
    return {"factory": factory, "production_lines": lines, "quality_issues_observed": issues}


def get_engineering_changes(dataset: dict, params: dict) -> dict:
    issue_id = params["issue_id"]
    changes = [ec for ec in dataset.get("engineering_changes", []) if ec["issue_id"] == issue_id]
    return {"engineering_changes": changes}


def recommend_quality_actions(dataset: dict, params: dict) -> dict:
    """Rule-based, read-only recommendation - not an automated decision. A human
    quality engineer must review before any action is taken."""
    issue_id = params["issue_id"]
    issue = _find(dataset, "quality_issues", "issue_id", issue_id)
    if issue is None:
        return {"error": f"Quality issue {issue_id} not found"}
    changes = [ec for ec in dataset.get("engineering_changes", []) if ec["issue_id"] == issue_id]
    recommendations = []
    if issue["defect_rate_percent"] >= 5.0:
        recommendations.append("Defect rate is high - recommend a supplier audit for the responsible part.")
    if not changes:
        recommendations.append("No engineering change exists yet - recommend opening one for engineering review.")
    else:
        latest = changes[-1]
        if latest["status"] in ("proposed", "in_progress"):
            recommendations.append(
                f"Engineering change {latest['change_id']} is still '{latest['status']}' - recommend following up with engineering."
            )
    if issue["severity"] in ("high", "critical"):
        recommendations.append("Severity is high/critical - recommend escalating to the factory quality lead.")
    if not recommendations:
        recommendations.append("No immediate action identified from available data; continue monitoring.")
    return {"issue_id": issue_id, "recommendations": recommendations, "requires_human_review": True}


TOOL_FUNCTIONS: dict[str, Callable[[dict, dict], dict]] = {
    "search_quality_issues": search_quality_issues,
    "get_part_traceability": get_part_traceability,
    "get_supplier_history": get_supplier_history,
    "get_factory_context": get_factory_context,
    "get_engineering_changes": get_engineering_changes,
    "recommend_quality_actions": recommend_quality_actions,
}

TOOL_DESCRIPTIONS: dict[str, str] = {
    "search_quality_issues": "Search quality issues by part_id, factory_id, and/or status.",
    "get_part_traceability": "Get a part's supplier and the production lines it is used in.",
    "get_supplier_history": "Get a supplier's parts and related quality issues.",
    "get_factory_context": "Get a factory's production lines and observed quality issues.",
    "get_engineering_changes": "Get engineering changes addressing a quality issue.",
    "recommend_quality_actions": "Generate rule-based, human-reviewed recommendations for a quality issue.",
}
