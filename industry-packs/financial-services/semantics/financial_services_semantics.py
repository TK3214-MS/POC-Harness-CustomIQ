"""Financial Services Fabric IQ relationship/metrics logic (Industry Pack
plugin module). Loaded dynamically via manifest.semantic_relationships_path -
see docs/decisions/0011-generic-orchestrator-and-semantic-adapter.md.
"""
from __future__ import annotations

from typing import Any


def get_relationships(dataset: dict, entity_type: str | None, entity_id: str | None) -> list[dict[str, str]]:
    relationships: list[dict[str, str]] = []

    if entity_type == "FraudCase":
        case = next((fc for fc in dataset.get("fraud_cases", []) if fc["case_id"] == entity_id), None)
        if case:
            relationships.append({"subject": entity_id, "relationship": "flags", "object": case["transaction_id"]})
            relationships.append({"subject": entity_id, "relationship": "relatesTo", "object": case["account_id"]})
            account = next((a for a in dataset.get("accounts", []) if a["account_id"] == case["account_id"]), None)
            if account:
                relationships.append(
                    {"subject": account["customer_id"], "relationship": "owns", "object": account["account_id"]}
                )
    elif entity_type == "Account":
        account = next((a for a in dataset.get("accounts", []) if a["account_id"] == entity_id), None)
        if account:
            relationships.append(
                {"subject": account["customer_id"], "relationship": "owns", "object": entity_id}
            )
    elif entity_type == "Transaction":
        txn = next((t for t in dataset.get("transactions", []) if t["transaction_id"] == entity_id), None)
        if txn:
            relationships.append({"subject": txn["account_id"], "relationship": "has", "object": entity_id})

    return relationships


def get_metrics(dataset: dict) -> dict[str, Any]:
    cases = dataset.get("fraud_cases", [])
    avg_risk_score = round(sum(c["risk_score"] for c in cases) / len(cases), 2) if cases else 0.0
    return {"fraud_case_count": len(cases), "average_risk_score": avg_risk_score}
