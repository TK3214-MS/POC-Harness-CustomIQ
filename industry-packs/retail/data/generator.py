"""Synthetic Retail dataset generator (Industry Pack plugin module).

Loaded dynamically by iq_platform.orchestration.industry_pack_loader - NOT
imported as a dotted Python package. See
docs/decisions/0010-industry-pack-plugin-loading.md.

All data is synthetic. No real stores, products, or orders are used. See
instruction section 23 and SECURITY.md.
"""
from __future__ import annotations

import random
from dataclasses import asdict, dataclass

_PLACES = [
    "Lindmoor", "Aurelport", "Kestrel Bay", "Draymoor", "Verdant Hollow",
    "Northfell", "Emberfield", "Stonebrook Junction", "Marrow Vale", "Windrift",
]
_PRODUCT_STEMS = [
    "Wireless Headphones", "Running Shoes", "Coffee Maker", "Desk Lamp", "Backpack",
    "Water Bottle", "Yoga Mat", "Bluetooth Speaker", "Rain Jacket", "Cookware Set",
]
_CATEGORIES = ["Electronics", "Apparel", "Home Goods", "Outdoor", "Kitchen"]
_ORDER_STATUSES = ["pending", "shipped", "delivered", "cancelled"]
_SIGNAL_TYPES = ["spike", "decline", "seasonal"]


@dataclass
class Store:
    store_id: str
    name: str
    region: str


@dataclass
class Product:
    product_id: str
    name: str
    category: str


@dataclass
class InventoryRecord:
    inventory_id: str
    store_id: str
    product_id: str
    quantity_on_hand: int
    reorder_point: int


@dataclass
class Order:
    order_id: str
    store_id: str
    product_id: str
    quantity: int
    order_date: str
    status: str


@dataclass
class DemandSignal:
    signal_id: str
    product_id: str
    store_id: str
    signal_type: str
    trend_percent: float
    detected_at: str


_SCALE_COUNTS = {
    "demo": {"stores": 4, "products": 10, "inventory_records": 25, "orders": 25, "demand_signals": 8},
    "realistic": {"stores": 50, "products": 500, "inventory_records": 4000, "orders": 5000, "demand_signals": 1200},
    "enterprise": {"stores": 500, "products": 5000, "inventory_records": 60000, "orders": 80000, "demand_signals": 15000},
}


def generate_dataset(seed: int = 42, scale: str = "demo") -> dict:
    """Generate a fully synthetic Retail dataset. Deterministic for a given seed."""
    if scale not in _SCALE_COUNTS:
        raise ValueError(f"Unknown scale '{scale}', expected one of {list(_SCALE_COUNTS)}")
    counts = _SCALE_COUNTS[scale]
    rng = random.Random(seed)

    stores = [
        Store(store_id=f"STORE-{i + 1:04d}", name=f"{rng.choice(_PLACES)} Store {i + 1}", region=rng.choice(_PLACES))
        for i in range(counts["stores"])
    ]
    products = [
        Product(product_id=f"PROD-{i + 1:05d}", name=f"{rng.choice(_PRODUCT_STEMS)} {i + 1}", category=rng.choice(_CATEGORIES))
        for i in range(counts["products"])
    ]

    inventory_records = []
    for i in range(counts["inventory_records"]):
        store = rng.choice(stores)
        product = rng.choice(products)
        inventory_records.append(
            InventoryRecord(
                inventory_id=f"INV-{i + 1:05d}",
                store_id=store.store_id,
                product_id=product.product_id,
                quantity_on_hand=rng.randint(0, 200),
                reorder_point=rng.randint(10, 60),
            )
        )

    orders = []
    for i in range(counts["orders"]):
        store = rng.choice(stores)
        product = rng.choice(products)
        orders.append(
            Order(
                order_id=f"ORD-{i + 1:05d}",
                store_id=store.store_id,
                product_id=product.product_id,
                quantity=rng.randint(1, 50),
                order_date=f"2026-{rng.randint(1, 8):02d}-{rng.randint(1, 28):02d}",
                status=rng.choice(_ORDER_STATUSES),
            )
        )

    demand_signals = []
    for i in range(counts["demand_signals"]):
        product = rng.choice(products)
        store = rng.choice(stores)
        demand_signals.append(
            DemandSignal(
                signal_id=f"SIG-{i + 1:05d}",
                product_id=product.product_id,
                store_id=store.store_id,
                signal_type=rng.choice(_SIGNAL_TYPES),
                trend_percent=round(rng.uniform(-40, 80), 1),
                detected_at=f"2026-{rng.randint(1, 8):02d}-{rng.randint(1, 28):02d}",
            )
        )

    # Guarantee the default (first) demand signal has a matching low-stock
    # inventory record, so the default scenario is always meaningful.
    if demand_signals and inventory_records:
        primary_signal = demand_signals[0]
        inventory_records[0] = InventoryRecord(
            inventory_id=inventory_records[0].inventory_id,
            store_id=primary_signal.store_id,
            product_id=primary_signal.product_id,
            quantity_on_hand=5,
            reorder_point=50,
        )

    return {
        "stores": [asdict(s) for s in stores],
        "products": [asdict(p) for p in products],
        "inventory_records": [asdict(i) for i in inventory_records],
        "orders": [asdict(o) for o in orders],
        "demand_signals": [asdict(d) for d in demand_signals],
    }
