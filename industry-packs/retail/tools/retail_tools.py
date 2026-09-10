"""Retail-specific MCP tools (Industry Pack plugin module).

Loaded dynamically by services/mcp-backend/mcp_backend/factory.py. See
docs/decisions/0010-industry-pack-plugin-loading.md.

Every function here is read-only / advisory. Nothing in this module places a
reorder or changes pricing automatically - see
industry-packs/retail/manifest.yaml prohibited_actions.
"""
from __future__ import annotations

from collections.abc import Callable


def _find(dataset: dict, entity_key: str, id_field: str, id_value: str) -> dict | None:
    return next((row for row in dataset.get(entity_key, []) if row[id_field] == id_value), None)


def get_inventory_status(dataset: dict, params: dict) -> dict:
    store_id = params.get("store_id")
    product_id = params.get("product_id")
    records = [
        r
        for r in dataset.get("inventory_records", [])
        if (store_id is None or r["store_id"] == store_id) and (product_id is None or r["product_id"] == product_id)
    ]
    return {"inventory_records": records[:50], "total_matches": len(records)}


def get_order_history(dataset: dict, params: dict) -> dict:
    store_id = params.get("store_id")
    product_id = params.get("product_id")
    orders = [
        o
        for o in dataset.get("orders", [])
        if (store_id is None or o["store_id"] == store_id) and (product_id is None or o["product_id"] == product_id)
    ]
    return {"orders": orders[:50], "total_matches": len(orders)}


def get_demand_signals(dataset: dict, params: dict) -> dict:
    store_id = params.get("store_id")
    product_id = params.get("product_id")
    signals = [
        s
        for s in dataset.get("demand_signals", [])
        if (store_id is None or s["store_id"] == store_id) and (product_id is None or s["product_id"] == product_id)
    ]
    return {"demand_signals": signals[:50], "total_matches": len(signals)}


def recommend_inventory_actions(dataset: dict, params: dict) -> dict:
    signal_id = params["signal_id"]
    signal = _find(dataset, "demand_signals", "signal_id", signal_id)
    if signal is None:
        return {"error": f"Demand signal {signal_id} not found"}
    inventory = next(
        (
            r
            for r in dataset.get("inventory_records", [])
            if r["store_id"] == signal["store_id"] and r["product_id"] == signal["product_id"]
        ),
        None,
    )
    recommendations = []
    if inventory is None:
        recommendations.append(
            "No inventory record found for this store/product combination - recommend confirming stock levels manually."
        )
    elif inventory["quantity_on_hand"] < inventory["reorder_point"]:
        recommendations.append(
            f"On-hand quantity ({inventory['quantity_on_hand']}) is below the reorder point "
            f"({inventory['reorder_point']}) - recommend a reorder review."
        )
    if signal["signal_type"] == "spike":
        recommendations.append("Demand signal is a spike - recommend prioritizing this product for review.")
    if not recommendations:
        recommendations.append("No immediate action identified from available data; continue monitoring.")
    return {"signal_id": signal_id, "recommendations": recommendations, "requires_human_review": True}


TOOL_FUNCTIONS: dict[str, Callable[[dict, dict], dict]] = {
    "get_inventory_status": get_inventory_status,
    "get_order_history": get_order_history,
    "get_demand_signals": get_demand_signals,
    "recommend_inventory_actions": recommend_inventory_actions,
}

TOOL_DESCRIPTIONS: dict[str, str] = {
    "get_inventory_status": "Get inventory records filtered by store_id and/or product_id.",
    "get_order_history": "Get order history filtered by store_id and/or product_id.",
    "get_demand_signals": "Get demand signals filtered by store_id and/or product_id.",
    "recommend_inventory_actions": "Generate rule-based, human-reviewed recommendations for a demand signal.",
}
