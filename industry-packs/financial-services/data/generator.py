"""Synthetic Financial Services dataset generator (Industry Pack plugin module).

Loaded dynamically by iq_platform.orchestration.industry_pack_loader - NOT
imported as a dotted Python package. See
docs/decisions/0010-industry-pack-plugin-loading.md.

All data is synthetic. No real customers, accounts, or transactions are used.
See instruction section 23 and SECURITY.md.
"""
from __future__ import annotations

import random
from dataclasses import asdict, dataclass

_SEGMENTS = ["retail", "business", "private_banking"]
_ACCOUNT_TYPES = ["checking", "savings", "credit_card"]
_TRANSACTION_TYPES = ["purchase", "withdrawal", "transfer", "deposit"]
_CURRENCIES = ["USD", "EUR", "JPY"]
_MERCHANT_STEMS = ["Northgate", "Silverline", "Aurelport", "Windrift", "Marrow Vale", "Cobalt Peak", "Draymoor"]
_MERCHANT_SUFFIXES = ["Retail", "Market", "Digital Goods", "Travel", "Electronics", "Grocery"]
_FRAUD_CASE_STATUSES = ["open", "investigating", "confirmed_fraud", "closed_no_fraud"]


@dataclass
class Customer:
    customer_id: str
    display_name: str
    segment: str


@dataclass
class Account:
    account_id: str
    customer_id: str
    account_type: str
    opened_at: str


@dataclass
class Transaction:
    transaction_id: str
    account_id: str
    amount: float
    currency: str
    merchant: str
    transaction_type: str
    occurred_at: str


@dataclass
class FraudCase:
    case_id: str
    transaction_id: str
    account_id: str
    status: str
    risk_score: float
    opened_at: str


_SCALE_COUNTS = {
    "demo": {"customers": 8, "accounts": 10, "transactions": 80, "fraud_cases": 6},
    "realistic": {"customers": 400, "accounts": 550, "transactions": 6000, "fraud_cases": 250},
}


def generate_dataset(seed: int = 42, scale: str = "demo") -> dict:
    """Generate a fully synthetic Financial Services dataset. Deterministic for a
    given seed. Customer names are deliberately non-humanlike placeholders
    ("Synthetic Customer NNNNN") to avoid any resemblance to real individuals."""
    if scale not in _SCALE_COUNTS:
        raise ValueError(f"Unknown scale '{scale}', expected one of {list(_SCALE_COUNTS)}")
    counts = _SCALE_COUNTS[scale]
    rng = random.Random(seed)

    customers = [
        Customer(
            customer_id=f"CUST-{i + 1:05d}",
            display_name=f"Synthetic Customer {i + 1:05d}",
            segment=rng.choice(_SEGMENTS),
        )
        for i in range(counts["customers"])
    ]

    accounts = []
    for i in range(counts["accounts"]):
        customer = rng.choice(customers)
        accounts.append(
            Account(
                account_id=f"ACC-{i + 1:05d}",
                customer_id=customer.customer_id,
                account_type=rng.choice(_ACCOUNT_TYPES),
                opened_at=f"2024-{rng.randint(1, 12):02d}-{rng.randint(1, 28):02d}",
            )
        )

    transactions = []
    for i in range(counts["transactions"]):
        account = rng.choice(accounts)
        transactions.append(
            Transaction(
                transaction_id=f"TXN-{i + 1:06d}",
                account_id=account.account_id,
                amount=round(rng.uniform(5, 500), 2),
                currency=rng.choice(_CURRENCIES),
                merchant=f"{rng.choice(_MERCHANT_STEMS)} {rng.choice(_MERCHANT_SUFFIXES)} #{i + 1}",
                transaction_type=rng.choice(_TRANSACTION_TYPES),
                occurred_at=f"2026-{rng.randint(1, 8):02d}-{rng.randint(1, 28):02d}",
            )
        )

    fraud_cases = []
    flagged_transactions = rng.sample(transactions, k=min(len(transactions), counts["fraud_cases"]))
    for i, txn in enumerate(flagged_transactions):
        # Spike the amount on flagged transactions so the fraud scenario has a
        # meaningful signal to find (still synthetic/random, not real events).
        txn.amount = round(rng.uniform(800, 5000), 2)
        fraud_cases.append(
            FraudCase(
                case_id=f"FC-{i + 1:05d}",
                transaction_id=txn.transaction_id,
                account_id=txn.account_id,
                status=rng.choice(_FRAUD_CASE_STATUSES),
                risk_score=round(rng.uniform(0.4, 0.98), 2),
                opened_at=txn.occurred_at,
            )
        )

    return {
        "customers": [asdict(c) for c in customers],
        "accounts": [asdict(a) for a in accounts],
        "transactions": [asdict(t) for t in transactions],
        "fraud_cases": [asdict(fc) for fc in fraud_cases],
    }
