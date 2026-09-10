"""Retail scenario runner (Industry Pack plugin module).

Loaded dynamically via manifest.scenario_module_path. Implements the 'Retail
Demand and Inventory Analysis' standard scenario (instruction §9.3).
"""
from __future__ import annotations

from typing import Any


def run_scenario(context: Any, entity_id: str | None = None) -> dict:
    dataset = context.dataset
    signal_id = entity_id or dataset["demand_signals"][0]["signal_id"]
    signal = next(s for s in dataset["demand_signals"] if s["signal_id"] == signal_id)

    work_context = context.work_context_adapter.query("search_messages", {"keywords": ["inventory", "demand"]})
    relationships_raw = context.semantic_adapter.query(
        "get_relationships", {"entity_type": "DemandSignal", "entity_id": signal_id}
    )
    knowledge_results = context.knowledge_adapter.query(
        "search_knowledge", {"query": "inventory replenishment demand signal reorder"}
    )

    inventory = context.invoke_tool("get_inventory_status", {"store_id": signal["store_id"], "product_id": signal["product_id"]})
    orders = context.invoke_tool("get_order_history", {"store_id": signal["store_id"], "product_id": signal["product_id"]})
    recommendations = context.invoke_tool("recommend_inventory_actions", {"signal_id": signal_id})

    product = next((p for p in dataset["products"] if p["product_id"] == signal["product_id"]), {})
    store = next((s for s in dataset["stores"] if s["store_id"] == signal["store_id"]), {})
    inventory_records = inventory["data"].get("inventory_records", [])
    inventory_record = inventory_records[0] if inventory_records else {}

    confirmed_facts = [
        f"Demand signal {signal_id} ({signal['signal_type']}, trend {signal['trend_percent']}%) was detected on {signal['detected_at']}.",
        f"Signal relates to product {product.get('name', signal['product_id'])} at store {store.get('name', signal['store_id'])}.",
    ]
    if inventory_record:
        confirmed_facts.append(
            f"On-hand quantity is {inventory_record['quantity_on_hand']} against a reorder point of "
            f"{inventory_record['reorder_point']}."
        )

    uncertainty_and_conflicts = []
    if not inventory_records:
        uncertainty_and_conflicts.append("No inventory record found for this store/product combination.")
    if not orders["data"].get("orders"):
        uncertainty_and_conflicts.append("No order history found for this store/product combination.")
    if not work_context.get("results"):
        uncertainty_and_conflicts.append(
            "No related work context (messages/meetings) was found in the simulated fixtures for this signal."
        )

    mcp_tool_results = [
        {
            "tool_name": "get_inventory_status",
            "status": inventory["status"],
            "summary": f"{inventory['data'].get('total_matches', 0)} inventory record(s) found.",
        },
        {
            "tool_name": "get_order_history",
            "status": orders["status"],
            "summary": f"{orders['data'].get('total_matches', 0)} order(s) found.",
        },
        {
            "tool_name": "recommend_inventory_actions",
            "status": recommendations["status"],
            "summary": "; ".join(recommendations["data"].get("recommendations", [])),
        },
    ]

    return {
        "executive_summary": (
            f"Investigated demand signal {signal_id} ({signal['signal_type']}) for "
            f"{product.get('name', signal['product_id'])} at {store.get('name', signal['store_id'])}."
        ),
        "confirmed_facts": confirmed_facts,
        "documents_and_citations": knowledge_results.get("results", []),
        "entities_and_relationships": relationships_raw.get("relationships", []),
        "mcp_tool_results": mcp_tool_results,
        "uncertainty_and_conflicts": uncertainty_and_conflicts,
        "recommended_next_actions": recommendations["data"].get("recommendations", []),
        "human_in_the_loop_requirements": [
            "An inventory manager must approve any reorder before it is placed.",
            "This accelerator never automatically places a reorder or changes pricing.",
        ],
    }
