"""Financial Services-specific MCP tools (Industry Pack plugin module).

Loaded dynamically by services/mcp-backend/mcp_backend/factory.py.

Every function here is read-only / advisory. Nothing in this module freezes an
account, denies a transaction, or makes a legal/credit determination - see
industry-packs/financial-services/manifest.yaml prohibited_actions.
"""
from __future__ import annotations

from collections.abc import Callable


def _find(dataset: dict, entity_key: str, id_field: str, id_value: str) -> dict | None:
    return next((row for row in dataset.get(entity_key, []) if row[id_field] == id_value), None)


def search_transactions(dataset: dict, params: dict) -> dict:
    txns = dataset.get("transactions", [])
    account_id = params.get("account_id")
    transaction_type = params.get("transaction_type")
    min_amount = params.get("min_amount")
    results = [
        t
        for t in txns
        if (account_id is None or t["account_id"] == account_id)
        and (transaction_type is None or t["transaction_type"] == transaction_type)
        and (min_amount is None or t["amount"] >= min_amount)
    ]
    return {"transactions": results[:50], "total_matches": len(results)}


def get_account_relationships(dataset: dict, params: dict) -> dict:
    account_id = params["account_id"]
    account = _find(dataset, "accounts", "account_id", account_id)
    if account is None:
        return {"error": f"Account {account_id} not found"}
    customer = _find(dataset, "customers", "customer_id", account["customer_id"])
    transactions = [t for t in dataset.get("transactions", []) if t["account_id"] == account_id]
    fraud_cases = [fc for fc in dataset.get("fraud_cases", []) if fc["account_id"] == account_id]
    return {
        "account": account,
        "customer": customer,
        "transaction_count": len(transactions),
        "fraud_cases": fraud_cases,
    }


def get_risk_events(dataset: dict, params: dict) -> dict:
    """Return FraudCase records, which represent risk events in this pack."""
    account_id = params["account_id"]
    events = [fc for fc in dataset.get("fraud_cases", []) if fc["account_id"] == account_id]
    return {"risk_events": events}


def analyze_fraud_signals(dataset: dict, params: dict) -> dict:
    case_id = params["case_id"]
    case = _find(dataset, "fraud_cases", "case_id", case_id)
    if case is None:
        return {"error": f"Fraud case {case_id} not found"}
    transaction = _find(dataset, "transactions", "transaction_id", case["transaction_id"])
    account_transactions = [t for t in dataset.get("transactions", []) if t["account_id"] == case["account_id"]]
    avg_amount = (
        round(sum(t["amount"] for t in account_transactions) / len(account_transactions), 2)
        if account_transactions
        else 0.0
    )
    signals = []
    if transaction and avg_amount and transaction["amount"] >= avg_amount * 3:
        signals.append(
            f"Transaction amount {transaction['amount']} is more than 3x the account's average ({avg_amount})."
        )
    if case["risk_score"] >= 0.7:
        signals.append(f"Risk score {case['risk_score']} is high.")
    if not signals:
        signals.append("No strong fraud signal identified from available data.")
    return {"case_id": case_id, "transaction": transaction, "account_average_amount": avg_amount, "signals": signals}


def recommend_investigation_steps(dataset: dict, params: dict) -> dict:
    case_id = params["case_id"]
    case = _find(dataset, "fraud_cases", "case_id", case_id)
    if case is None:
        return {"error": f"Fraud case {case_id} not found"}
    recommendations = []
    if case["status"] == "open":
        recommendations.append("Case is open - recommend assigning to a fraud analyst for initial review.")
    if case["risk_score"] >= 0.7:
        recommendations.append("Risk score is high - recommend contacting the customer to verify the transaction.")
    recommendations.append("Do not freeze the account or deny future transactions automatically - human review required.")
    return {"case_id": case_id, "recommendations": recommendations, "requires_human_review": True}


TOOL_FUNCTIONS: dict[str, Callable[[dict, dict], dict]] = {
    "search_transactions": search_transactions,
    "get_account_relationships": get_account_relationships,
    "get_risk_events": get_risk_events,
    "analyze_fraud_signals": analyze_fraud_signals,
    "recommend_investigation_steps": recommend_investigation_steps,
}

TOOL_DESCRIPTIONS: dict[str, str] = {
    "search_transactions": "Search transactions by account_id, transaction_type, and/or min_amount.",
    "get_account_relationships": "Get an account's customer, transaction count, and related fraud cases.",
    "get_risk_events": "Get risk events (represented by FraudCase records) for an account.",
    "analyze_fraud_signals": "Generate rule-based fraud signal analysis for a fraud case.",
    "recommend_investigation_steps": "Generate rule-based, human-reviewed recommendations for a fraud case.",
}
