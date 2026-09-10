"""Manufacturing scenario runner (Industry Pack plugin module).

Loaded dynamically via manifest.scenario_module_path - see
docs/decisions/0011-generic-orchestrator-and-semantic-adapter.md. Implements the
'Manufacturing Quality Issue Investigation' standard scenario (instruction §9.1).
"""
from __future__ import annotations

from typing import Any


def _issue_part_id(dataset: dict, issue_id: str) -> str:
    issue = next(qi for qi in dataset["quality_issues"] if qi["issue_id"] == issue_id)
    return issue["part_id"]


def run_scenario(context: Any, entity_id: str | None = None) -> dict:
    dataset = context.dataset
    issue_id = entity_id or dataset["quality_issues"][0]["issue_id"]

    work_context = context.work_context_adapter.query("search_messages", {"keywords": ["quality", issue_id]})
    relationships_raw = context.semantic_adapter.query(
        "get_relationships", {"entity_type": "QualityIssue", "entity_id": issue_id}
    )
    knowledge_results = context.knowledge_adapter.query(
        "search_knowledge", {"query": "quality issue engineering change supplier"}
    )

    traceability = context.invoke_tool("get_part_traceability", {"part_id": _issue_part_id(dataset, issue_id)})
    changes = context.invoke_tool("get_engineering_changes", {"issue_id": issue_id})
    recommendations = context.invoke_tool("recommend_quality_actions", {"issue_id": issue_id})

    issue = next(qi for qi in dataset["quality_issues"] if qi["issue_id"] == issue_id)
    part = traceability["data"].get("part") or {}
    supplier = traceability["data"].get("supplier") or {}
    factory = next((f for f in dataset["factories"] if f["factory_id"] == issue["factory_id"]), {})

    confirmed_facts = [
        f"Quality issue {issue_id} was detected on {issue['detected_at']} with severity '{issue['severity']}'.",
        f"Defect rate is {issue['defect_rate_percent']}%.",
        (
            f"Issue affects part {issue['part_id']} supplied by "
            f"{supplier.get('name', 'unknown supplier')} ({supplier.get('supplier_id', 'unknown')})."
        ),
        f"Issue was observed at factory {factory.get('name', issue['factory_id'])}.",
    ]

    uncertainty_and_conflicts = []
    if not changes["data"].get("engineering_changes"):
        uncertainty_and_conflicts.append(
            "No engineering change has been created yet for this issue; root cause is not yet confirmed."
        )
    if not work_context.get("results"):
        uncertainty_and_conflicts.append(
            "No related work context (messages/meetings) was found in the simulated fixtures for this issue."
        )

    mcp_tool_results = [
        {
            "tool_name": "get_part_traceability",
            "status": traceability["status"],
            "summary": (
                f"Part {part.get('name', part.get('part_id', 'unknown'))} supplied by "
                f"{supplier.get('name', 'unknown supplier')}."
            ),
        },
        {
            "tool_name": "get_engineering_changes",
            "status": changes["status"],
            "summary": f"{len(changes['data'].get('engineering_changes', []))} engineering change(s) found.",
        },
        {
            "tool_name": "recommend_quality_actions",
            "status": recommendations["status"],
            "summary": "; ".join(recommendations["data"].get("recommendations", [])),
        },
    ]

    return {
        "executive_summary": (
            f"Investigated quality issue {issue_id} ({issue['summary']}) at "
            f"{factory.get('name', issue['factory_id'])}, affecting part "
            f"{part.get('name', issue['part_id'])} supplied by {supplier.get('name', 'unknown supplier')}."
        ),
        "confirmed_facts": confirmed_facts,
        "documents_and_citations": knowledge_results.get("results", []),
        "entities_and_relationships": relationships_raw.get("relationships", []),
        "mcp_tool_results": mcp_tool_results,
        "uncertainty_and_conflicts": uncertainty_and_conflicts,
        "recommended_next_actions": recommendations["data"].get("recommendations", []),
        "human_in_the_loop_requirements": [
            "A quality engineer must review and approve any recommended action before implementation.",
            "Closing this quality issue requires quality_engineer approval (see manifest.yaml human_approval_rules).",
        ],
    }
