"""Financial Services scenario runner (Industry Pack plugin module).

Loaded dynamically via manifest.scenario_module_path. Implements the 'Financial
Fraud Investigation' standard scenario (instruction §9.2).
"""
from __future__ import annotations

from typing import Any


def run_scenario(context: Any, entity_id: str | None = None) -> dict:
    dataset = context.dataset
    case_id = entity_id or dataset["fraud_cases"][0]["case_id"]
    case = next(fc for fc in dataset["fraud_cases"] if fc["case_id"] == case_id)

    work_context = context.work_context_adapter.query("search_messages", {"keywords": ["fraud", case_id]})
    relationships_raw = context.semantic_adapter.query(
        "get_relationships", {"entity_type": "FraudCase", "entity_id": case_id}
    )
    knowledge_results = context.knowledge_adapter.query(
        "search_knowledge", {"query": "fraud investigation transaction monitoring compliance"}
    )

    account_rel = context.invoke_tool("get_account_relationships", {"account_id": case["account_id"]})
    signals = context.invoke_tool("analyze_fraud_signals", {"case_id": case_id})
    recommendations = context.invoke_tool("recommend_investigation_steps", {"case_id": case_id})

    customer = account_rel["data"].get("customer") or {}
    transaction = signals["data"].get("transaction") or {}

    confirmed_facts = [
        f"Fraud case {case_id} was opened on {case['opened_at']} with risk score {case['risk_score']}.",
        f"Case status is '{case['status']}'.",
        (
            f"Flagged transaction {case['transaction_id']} was for "
            f"{transaction.get('amount', 'an unknown amount')} {transaction.get('currency', '')}."
        ),
        f"Account {case['account_id']} belongs to customer {customer.get('display_name', 'unknown customer')}.",
    ]

    uncertainty_and_conflicts = []
    if case["status"] in ("open", "investigating"):
        uncertainty_and_conflicts.append("Case is not yet resolved; fraud has not been confirmed.")
    if not work_context.get("results"):
        uncertainty_and_conflicts.append(
            "No related work context (messages/meetings) was found in the simulated fixtures for this case."
        )

    mcp_tool_results = [
        {
            "tool_name": "get_account_relationships",
            "status": account_rel["status"],
            "summary": (
                f"Account held by {customer.get('display_name', 'unknown customer')}, "
                f"{account_rel['data'].get('transaction_count', 0)} transaction(s) on record."
            ),
        },
        {
            "tool_name": "analyze_fraud_signals",
            "status": signals["status"],
            "summary": "; ".join(signals["data"].get("signals", [])),
        },
        {
            "tool_name": "recommend_investigation_steps",
            "status": recommendations["status"],
            "summary": "; ".join(recommendations["data"].get("recommendations", [])),
        },
    ]

    return {
        "executive_summary": (
            f"Investigated fraud case {case_id} (status: {case['status']}, risk score {case['risk_score']}) "
            f"on account {case['account_id']} held by {customer.get('display_name', 'unknown customer')}."
        ),
        "confirmed_facts": confirmed_facts,
        "documents_and_citations": knowledge_results.get("results", []),
        "entities_and_relationships": relationships_raw.get("relationships", []),
        "mcp_tool_results": mcp_tool_results,
        "uncertainty_and_conflicts": uncertainty_and_conflicts,
        "recommended_next_actions": recommendations["data"].get("recommendations", []),
        "human_in_the_loop_requirements": [
            "A fraud analyst must review and confirm this case before any account action is taken.",
            "This accelerator never automatically freezes accounts, denies transactions, or makes credit/legal determinations.",
        ],
    }
