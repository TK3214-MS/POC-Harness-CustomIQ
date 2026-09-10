"""Retail Fabric IQ relationship/metrics logic (Industry Pack plugin module).
Loaded dynamically via manifest.semantic_relationships_path - see
docs/decisions/0011-generic-orchestrator-and-semantic-adapter.md.
"""
from __future__ import annotations

from typing import Any


def get_relationships(dataset: dict, entity_type: str | None, entity_id: str | None) -> list[dict[str, str]]:
    relationships: list[dict[str, str]] = []

    if entity_type == "DemandSignal":
        signal = next((s for s in dataset.get("demand_signals", []) if s["signal_id"] == entity_id), None)
        if signal:
            relationships.append(
                {"subject": entity_id, "relationship": "relatesTo", "object": signal["product_id"]}
            )
            relationships.append(
                {"subject": entity_id, "relationship": "observedAt", "object": signal["store_id"]}
            )
    elif entity_type == "Product":
        for record in dataset.get("inventory_records", []):
            if record["product_id"] == entity_id:
                relationships.append(
                    {"subject": record["store_id"], "relationship": "stocks", "object": entity_id}
                )
    elif entity_type == "Store":
        for order in dataset.get("orders", []):
            if order["store_id"] == entity_id:
                relationships.append(
                    {"subject": entity_id, "relationship": "ordered", "object": order["order_id"]}
                )

    return relationships


def get_metrics(dataset: dict) -> dict[str, Any]:
    records = dataset.get("inventory_records", [])
    low_stock_count = sum(1 for r in records if r["quantity_on_hand"] < r["reorder_point"])
    return {"demand_signal_count": len(dataset.get("demand_signals", [])), "low_stock_inventory_count": low_stock_count}
