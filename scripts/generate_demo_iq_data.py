"""Generate a compact, cross-IQ synthetic dataset for customer demos."""
from __future__ import annotations

import csv
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PACKS_DIR = REPO_ROOT / "industry-packs"

DEMO_DATA = {
    "manufacturing": {
        "factories": [
            {"factory_id": "FAC-SYN-01", "name": "Northfield Assembly Plant", "location": "Aurelport"},
            {"factory_id": "FAC-SYN-02", "name": "Riverside Components Plant", "location": "Lindmoor"},
        ],
        "production_lines": [
            {"line_id": "LINE-SYN-01", "factory_id": "FAC-SYN-01", "name": "Valve Assembly Line"},
            {"line_id": "LINE-SYN-02", "factory_id": "FAC-SYN-01", "name": "Connector Assembly Line"},
            {"line_id": "LINE-SYN-03", "factory_id": "FAC-SYN-02", "name": "Coating Line"},
        ],
        "suppliers": [
            {"supplier_id": "SUP-SYN-01", "name": "Northfield Precision Works", "region": "Aurelport", "reliability_score": 0.82},
            {"supplier_id": "SUP-SYN-02", "name": "Silverline Components", "region": "Lindmoor", "reliability_score": 0.94},
        ],
        "parts": [
            {"part_id": "PART-SYN-101", "name": "Valve Housing A", "supplier_id": "SUP-SYN-01", "used_in_line_ids": ["LINE-SYN-01"]},
            {"part_id": "PART-SYN-102", "name": "Connector Pin B", "supplier_id": "SUP-SYN-02", "used_in_line_ids": ["LINE-SYN-02"]},
            {"part_id": "PART-SYN-103", "name": "Protective Coating C", "supplier_id": "SUP-SYN-01", "used_in_line_ids": ["LINE-SYN-03"]},
            {"part_id": "PART-SYN-104", "name": "Packaging Seal D", "supplier_id": "SUP-SYN-02", "used_in_line_ids": ["LINE-SYN-01"]},
        ],
        "quality_issues": [
            {"issue_id": "QI-SYN-001", "part_id": "PART-SYN-101", "factory_id": "FAC-SYN-01", "summary": "Surface crack on valve housing", "severity": "high", "status": "open", "defect_rate_percent": 4.8, "detected_at": "2026-01-12T09:30:00Z"},
            {"issue_id": "QI-SYN-002", "part_id": "PART-SYN-102", "factory_id": "FAC-SYN-01", "summary": "Connector pin misalignment", "severity": "medium", "status": "investigating", "defect_rate_percent": 2.1, "detected_at": "2026-01-13T11:00:00Z"},
            {"issue_id": "QI-SYN-003", "part_id": "PART-SYN-103", "factory_id": "FAC-SYN-02", "summary": "Coating thickness below target", "severity": "high", "status": "contained", "defect_rate_percent": 3.7, "detected_at": "2026-01-15T14:20:00Z"},
            {"issue_id": "QI-SYN-004", "part_id": "PART-SYN-101", "factory_id": "FAC-SYN-02", "summary": "Dimensional variance at final inspection", "severity": "medium", "status": "open", "defect_rate_percent": 1.9, "detected_at": "2026-01-17T08:45:00Z"},
            {"issue_id": "QI-SYN-005", "part_id": "PART-SYN-104", "factory_id": "FAC-SYN-01", "summary": "Packaging seal failure", "severity": "low", "status": "closed", "defect_rate_percent": 0.8, "detected_at": "2026-01-19T16:10:00Z"},
        ],
        "engineering_changes": [
            {"change_id": "EC-SYN-001", "issue_id": "QI-SYN-001", "description": "Review valve housing tolerance and inspection gate", "status": "in_progress", "created_at": "2026-01-14T10:00:00Z"},
            {"change_id": "EC-SYN-002", "issue_id": "QI-SYN-002", "description": "Update connector alignment fixture", "status": "approved", "created_at": "2026-01-15T09:00:00Z"},
            {"change_id": "EC-SYN-003", "issue_id": "QI-SYN-003", "description": "Validate coating process parameters", "status": "proposed", "created_at": "2026-01-16T13:00:00Z"},
        ],
    },
    "financial-services": {
        "customers": [
            {"customer_id": "CUST-SYN-101", "display_name": "Synthetic Customer 101", "segment": "business"},
            {"customer_id": "CUST-SYN-102", "display_name": "Synthetic Customer 102", "segment": "retail"},
            {"customer_id": "CUST-SYN-103", "display_name": "Synthetic Customer 103", "segment": "retail"},
            {"customer_id": "CUST-SYN-104", "display_name": "Synthetic Customer 104", "segment": "private_banking"},
            {"customer_id": "CUST-SYN-105", "display_name": "Synthetic Customer 105", "segment": "business"},
        ],
        "accounts": [
            {"account_id": f"ACC-SYN-{number}", "customer_id": f"CUST-SYN-{number - 100}", "account_type": account_type, "opened_at": opened_at}
            for number, account_type, opened_at in (
                (201, "checking", "2024-03-12"), (202, "savings", "2024-05-08"),
                (203, "credit_card", "2024-08-21"), (204, "checking", "2025-01-10"),
                (205, "savings", "2025-04-18"),
            )
        ],
        "transactions": [
            {"transaction_id": "TX-SYN-1001", "account_id": "ACC-SYN-201", "amount": 2450.00, "currency": "USD", "merchant": "Aurelport Digital Goods", "transaction_type": "purchase", "occurred_at": "2026-02-03T09:45:00Z"},
            {"transaction_id": "TX-SYN-1002", "account_id": "ACC-SYN-202", "amount": 980.50, "currency": "USD", "merchant": "Northgate Travel", "transaction_type": "purchase", "occurred_at": "2026-02-03T12:10:00Z"},
            {"transaction_id": "TX-SYN-1003", "account_id": "ACC-SYN-203", "amount": 3100.00, "currency": "EUR", "merchant": "Silverline Electronics", "transaction_type": "purchase", "occurred_at": "2026-02-04T08:40:00Z"},
            {"transaction_id": "TX-SYN-1004", "account_id": "ACC-SYN-204", "amount": 640.25, "currency": "USD", "merchant": "Marrow Vale Market", "transaction_type": "transfer", "occurred_at": "2026-02-05T14:50:00Z"},
            {"transaction_id": "TX-SYN-1005", "account_id": "ACC-SYN-205", "amount": 1250.75, "currency": "JPY", "merchant": "Cobalt Peak Retail", "transaction_type": "withdrawal", "occurred_at": "2026-02-06T08:20:00Z"},
        ],
        "fraud_cases": [
            {"case_id": "CASE-SYN-001", "transaction_id": "TX-SYN-1001", "account_id": "ACC-SYN-201", "status": "open", "risk_score": 0.97, "opened_at": "2026-02-03T10:15:00Z"},
            {"case_id": "CASE-SYN-002", "transaction_id": "TX-SYN-1002", "account_id": "ACC-SYN-202", "status": "investigating", "risk_score": 0.84, "opened_at": "2026-02-03T12:40:00Z"},
            {"case_id": "CASE-SYN-003", "transaction_id": "TX-SYN-1003", "account_id": "ACC-SYN-203", "status": "escalated", "risk_score": 0.91, "opened_at": "2026-02-04T09:05:00Z"},
            {"case_id": "CASE-SYN-004", "transaction_id": "TX-SYN-1004", "account_id": "ACC-SYN-204", "status": "closed", "risk_score": 0.62, "opened_at": "2026-02-05T15:20:00Z"},
            {"case_id": "CASE-SYN-005", "transaction_id": "TX-SYN-1005", "account_id": "ACC-SYN-205", "status": "open", "risk_score": 0.78, "opened_at": "2026-02-06T08:50:00Z"},
        ],
    },
    "retail": {
        "stores": [
            {"store_id": "STORE-SYN-01", "name": "Aurelport Central", "region": "North"},
            {"store_id": "STORE-SYN-02", "name": "Lindmoor Market", "region": "East"},
            {"store_id": "STORE-SYN-03", "name": "Windrift Square", "region": "West"},
        ],
        "products": [
            {"product_id": "PROD-SYN-501", "name": "Everyday Travel Mug", "category": "home"},
            {"product_id": "PROD-SYN-502", "name": "Compact Desk Lamp", "category": "home"},
            {"product_id": "PROD-SYN-503", "name": "Trail Daypack", "category": "outdoor"},
            {"product_id": "PROD-SYN-504", "name": "Reusable Food Container", "category": "kitchen"},
        ],
        "inventory_records": [
            {"inventory_id": "INV-SYN-401", "store_id": "STORE-SYN-01", "product_id": "PROD-SYN-501", "quantity_on_hand": 12, "reorder_point": 20},
            {"inventory_id": "INV-SYN-402", "store_id": "STORE-SYN-01", "product_id": "PROD-SYN-502", "quantity_on_hand": 44, "reorder_point": 30},
            {"inventory_id": "INV-SYN-403", "store_id": "STORE-SYN-02", "product_id": "PROD-SYN-501", "quantity_on_hand": 8, "reorder_point": 18},
            {"inventory_id": "INV-SYN-404", "store_id": "STORE-SYN-02", "product_id": "PROD-SYN-503", "quantity_on_hand": 6, "reorder_point": 15},
            {"inventory_id": "INV-SYN-405", "store_id": "STORE-SYN-03", "product_id": "PROD-SYN-504", "quantity_on_hand": 27, "reorder_point": 25},
        ],
        "orders": [
            {"order_id": "ORD-SYN-601", "store_id": "STORE-SYN-01", "product_id": "PROD-SYN-501", "quantity": 25, "order_date": "2026-03-12", "status": "draft"},
            {"order_id": "ORD-SYN-602", "store_id": "STORE-SYN-02", "product_id": "PROD-SYN-501", "quantity": 20, "order_date": "2026-03-12", "status": "in_transit"},
            {"order_id": "ORD-SYN-603", "store_id": "STORE-SYN-02", "product_id": "PROD-SYN-503", "quantity": 18, "order_date": "2026-03-11", "status": "approved"},
        ],
        "demand_signals": [
            {"signal_id": "SIGNAL-SYN-001", "product_id": "PROD-SYN-501", "store_id": "STORE-SYN-01", "signal_type": "promotion_spike", "trend_percent": 18.5, "detected_at": "2026-03-10T08:00:00Z"},
            {"signal_id": "SIGNAL-SYN-002", "product_id": "PROD-SYN-502", "store_id": "STORE-SYN-01", "signal_type": "seasonal_decline", "trend_percent": -12.3, "detected_at": "2026-03-09T08:00:00Z"},
            {"signal_id": "SIGNAL-SYN-003", "product_id": "PROD-SYN-503", "store_id": "STORE-SYN-02", "signal_type": "local_spike", "trend_percent": 25.0, "detected_at": "2026-03-08T08:00:00Z"},
        ],
    },
    "healthcare": {
        "patients": [
            {"patient_id": f"PAT-SYN-{number}", "age_band": age_band, "note": "Fully synthetic care coordination record"}
            for number, age_band in ((101, "40-49"), (102, "50-59"), (103, "60-69"), (104, "30-39"), (105, "70-79"))
        ],
        "providers": [
            {"provider_id": "PROV-SYN-01", "role": "care coordinator"},
            {"provider_id": "PROV-SYN-02", "role": "documentation reviewer"},
            {"provider_id": "PROV-SYN-03", "role": "discharge planner"},
        ],
        "encounters": [
            {"encounter_id": "ENC-SYN-001", "patient_id": "PAT-SYN-101", "provider_id": "PROV-SYN-01", "encounter_date": "2026-02-10", "reason": "follow-up review"},
            {"encounter_id": "ENC-SYN-002", "patient_id": "PAT-SYN-102", "provider_id": "PROV-SYN-02", "encounter_date": "2026-02-11", "reason": "documentation completeness"},
            {"encounter_id": "ENC-SYN-003", "patient_id": "PAT-SYN-103", "provider_id": "PROV-SYN-01", "encounter_date": "2026-02-12", "reason": "care coordination"},
            {"encounter_id": "ENC-SYN-004", "patient_id": "PAT-SYN-104", "provider_id": "PROV-SYN-03", "encounter_date": "2026-02-13", "reason": "discharge planning"},
            {"encounter_id": "ENC-SYN-005", "patient_id": "PAT-SYN-105", "provider_id": "PROV-SYN-02", "encounter_date": "2026-02-14", "reason": "case escalation review"},
        ],
        "clinical_events": [
            {"event_id": "EVT-SYN-001", "encounter_id": "ENC-SYN-003", "event_type": "handoff_created", "description": "Primary care handoff prepared; clinic confirmation pending", "recorded_at": "2026-02-12T14:00:00Z"},
            {"event_id": "EVT-SYN-002", "encounter_id": "ENC-SYN-003", "event_type": "documentation_gap", "description": "One unsigned section and one missing laboratory result identified", "recorded_at": "2026-02-13T09:15:00Z"},
            {"event_id": "EVT-SYN-003", "encounter_id": "ENC-SYN-004", "event_type": "discharge_checklist", "description": "Discharge checklist opened for human review", "recorded_at": "2026-02-13T16:30:00Z"},
        ],
    },
    "public-sector": {
        "citizens": [
            {"citizen_id": f"CIT-SYN-{number}", "note": "Fully synthetic service applicant"}
            for number in range(101, 106)
        ],
        "agencies": [
            {"agency_id": "AGENCY-SYN-01", "name": "Aurelport Permit Service"},
            {"agency_id": "AGENCY-SYN-02", "name": "Lindmoor Benefits Office"},
            {"agency_id": "AGENCY-SYN-03", "name": "Windrift Inspection Service"},
        ],
        "cases": [
            {"case_id": "CASE-SYN-301", "citizen_id": "CIT-SYN-101", "agency_id": "AGENCY-SYN-01", "case_type": "permit_review", "status": "open", "opened_at": "2026-03-01T09:00:00Z"},
            {"case_id": "CASE-SYN-302", "citizen_id": "CIT-SYN-102", "agency_id": "AGENCY-SYN-02", "case_type": "benefit_eligibility", "status": "in_review", "opened_at": "2026-03-02T10:30:00Z"},
            {"case_id": "CASE-SYN-303", "citizen_id": "CIT-SYN-103", "agency_id": "AGENCY-SYN-01", "case_type": "records_request", "status": "awaiting_documents", "opened_at": "2026-03-03T13:15:00Z"},
            {"case_id": "CASE-SYN-304", "citizen_id": "CIT-SYN-104", "agency_id": "AGENCY-SYN-03", "case_type": "inspection_followup", "status": "closed", "opened_at": "2026-03-04T15:45:00Z"},
            {"case_id": "CASE-SYN-305", "citizen_id": "CIT-SYN-105", "agency_id": "AGENCY-SYN-02", "case_type": "service_referral", "status": "open", "opened_at": "2026-03-05T08:20:00Z"},
        ],
        "applications": [
            {"application_id": "APP-SYN-401", "case_id": "CASE-SYN-301", "application_type": "permit_application", "status": "pending_more_information", "submitted_at": "2026-03-01T08:30:00Z"},
            {"application_id": "APP-SYN-402", "case_id": "CASE-SYN-302", "application_type": "benefit_application", "status": "in_review", "submitted_at": "2026-03-02T09:45:00Z"},
            {"application_id": "APP-SYN-403", "case_id": "CASE-SYN-303", "application_type": "records_request", "status": "awaiting_documents", "submitted_at": "2026-03-03T12:50:00Z"},
            {"application_id": "APP-SYN-404", "case_id": "CASE-SYN-304", "application_type": "inspection_response", "status": "completed", "submitted_at": "2026-03-04T14:30:00Z"},
            {"application_id": "APP-SYN-405", "case_id": "CASE-SYN-305", "application_type": "service_referral", "status": "draft", "submitted_at": "2026-03-05T08:00:00Z"},
        ],
    },
}


def _write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        for row in rows:
            writer.writerow({
                key: json.dumps(value, ensure_ascii=True) if isinstance(value, (list, dict)) else value
                for key, value in row.items()
            })


def _write_foundry_corpus(pack_id: str) -> int:
    output_path = PACKS_DIR / pack_id / "sample-data" / "foundry" / "demo" / "knowledge.jsonl"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    knowledge_paths = sorted((PACKS_DIR / pack_id / "knowledge").glob("*.md"))
    with output_path.open("w", encoding="utf-8") as handle:
        for path in knowledge_paths:
            record = {
                "id": f"{pack_id}-{path.stem}",
                "industry": pack_id,
                "title": path.read_text(encoding="utf-8").splitlines()[0].removeprefix("# "),
                "source_file": path.name,
                "content": path.read_text(encoding="utf-8"),
            }
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    return len(knowledge_paths)


def main() -> None:
    for pack_id, tables in DEMO_DATA.items():
        output_dir = PACKS_DIR / pack_id / "sample-data" / "fabric"
        for table_name, rows in tables.items():
            _write_csv(output_dir / f"{table_name}.csv", rows)
        knowledge_count = _write_foundry_corpus(pack_id)
        row_count = sum(len(rows) for rows in tables.values())
        print(f"{pack_id}: {row_count} Fabric rows, {knowledge_count} Foundry documents")


if __name__ == "__main__":
    main()