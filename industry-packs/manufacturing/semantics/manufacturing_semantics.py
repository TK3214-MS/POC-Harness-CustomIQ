"""Manufacturing Fabric IQ relationship/metrics logic (Industry Pack plugin
module). Loaded dynamically via manifest.semantic_relationships_path - see
docs/decisions/0011-generic-orchestrator-and-semantic-adapter.md.
"""
from __future__ import annotations

from typing import Any


def get_relationships(dataset: dict, entity_type: str | None, entity_id: str | None) -> list[dict[str, str]]:
    relationships: list[dict[str, str]] = []

    if entity_type == "QualityIssue":
        issue = next((qi for qi in dataset.get("quality_issues", []) if qi["issue_id"] == entity_id), None)
        if issue:
            relationships.append({"subject": entity_id, "relationship": "affects", "object": issue["part_id"]})
            relationships.append({"subject": entity_id, "relationship": "observedAt", "object": issue["factory_id"]})
            part = next((p for p in dataset.get("parts", []) if p["part_id"] == issue["part_id"]), None)
            if part:
                relationships.append(
                    {"subject": part["supplier_id"], "relationship": "supplies", "object": part["part_id"]}
                )
            for ec in dataset.get("engineering_changes", []):
                if ec["issue_id"] == entity_id:
                    relationships.append(
                        {"subject": ec["change_id"], "relationship": "addresses", "object": entity_id}
                    )
    elif entity_type == "Part":
        part = next((p for p in dataset.get("parts", []) if p["part_id"] == entity_id), None)
        if part:
            relationships.append({"subject": part["supplier_id"], "relationship": "supplies", "object": entity_id})
            for line_id in part.get("used_in_line_ids", []):
                relationships.append({"subject": entity_id, "relationship": "usedIn", "object": line_id})
    elif entity_type == "Factory":
        for line in dataset.get("production_lines", []):
            if line["factory_id"] == entity_id:
                relationships.append({"subject": entity_id, "relationship": "produces", "object": line["line_id"]})

    return relationships


def get_metrics(dataset: dict) -> dict[str, Any]:
    issues = dataset.get("quality_issues", [])
    avg_defect_rate = round(sum(i["defect_rate_percent"] for i in issues) / len(issues), 2) if issues else 0.0
    return {"quality_issue_count": len(issues), "average_defect_rate_percent": avg_defect_rate}
