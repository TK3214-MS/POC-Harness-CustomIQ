import csv
import json
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
PACKS_DIR = REPO_ROOT / "industry-packs"
PACK_IDS = (
    "manufacturing",
    "financial-services",
    "retail",
    "healthcare",
    "public-sector",
)


def _read_table(pack_id: str, table_name: str) -> list[dict[str, str]]:
    path = PACKS_DIR / pack_id / "sample-data" / "fabric" / f"{table_name}.csv"
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


@pytest.mark.parametrize("pack_id", PACK_IDS)
def test_demo_fabric_data_covers_every_ontology_entity(pack_id: str):
    ontology_path = PACKS_DIR / pack_id / "ontology" / "entities.yaml"
    ontology = yaml.safe_load(ontology_path.read_text(encoding="utf-8"))

    for entity in ontology["entity_types"]:
        rows = _read_table(pack_id, entity["dataset_key"])
        assert rows, f"{pack_id}/{entity['dataset_key']} must contain demo rows"
        assert set(entity["fields"]) == set(rows[0])
        identifiers = [row[entity["identifier_field"]] for row in rows]
        assert all(identifiers)
        assert len(identifiers) == len(set(identifiers))


def test_demo_fabric_relationship_keys_resolve():
    joins = {
        "manufacturing": (
            ("production_lines", "factory_id", "factories", "factory_id"),
            ("parts", "supplier_id", "suppliers", "supplier_id"),
            ("quality_issues", "part_id", "parts", "part_id"),
            ("quality_issues", "factory_id", "factories", "factory_id"),
            ("engineering_changes", "issue_id", "quality_issues", "issue_id"),
        ),
        "financial-services": (
            ("accounts", "customer_id", "customers", "customer_id"),
            ("transactions", "account_id", "accounts", "account_id"),
            ("fraud_cases", "transaction_id", "transactions", "transaction_id"),
            ("fraud_cases", "account_id", "accounts", "account_id"),
        ),
        "retail": (
            ("inventory_records", "store_id", "stores", "store_id"),
            ("inventory_records", "product_id", "products", "product_id"),
            ("orders", "store_id", "stores", "store_id"),
            ("orders", "product_id", "products", "product_id"),
            ("demand_signals", "store_id", "stores", "store_id"),
            ("demand_signals", "product_id", "products", "product_id"),
        ),
        "healthcare": (
            ("encounters", "patient_id", "patients", "patient_id"),
            ("encounters", "provider_id", "providers", "provider_id"),
            ("clinical_events", "encounter_id", "encounters", "encounter_id"),
        ),
        "public-sector": (
            ("cases", "citizen_id", "citizens", "citizen_id"),
            ("cases", "agency_id", "agencies", "agency_id"),
            ("applications", "case_id", "cases", "case_id"),
        ),
    }

    for pack_id, pack_joins in joins.items():
        for source_table, source_key, target_table, target_key in pack_joins:
            source_values = {row[source_key] for row in _read_table(pack_id, source_table)}
            target_values = {row[target_key] for row in _read_table(pack_id, target_table)}
            assert source_values <= target_values, (
                f"{pack_id}: {source_table}.{source_key} contains unresolved values "
                f"for {target_table}.{target_key}: {source_values - target_values}"
            )


@pytest.mark.parametrize("pack_id", PACK_IDS)
def test_demo_foundry_corpus_contains_all_knowledge_documents(pack_id: str):
    corpus_path = PACKS_DIR / pack_id / "sample-data" / "foundry" / "demo" / "knowledge.jsonl"
    records = [json.loads(line) for line in corpus_path.read_text(encoding="utf-8").splitlines()]
    knowledge_files = sorted((PACKS_DIR / pack_id / "knowledge").glob("*.md"))

    assert len(records) == len(knowledge_files)
    assert len(records) >= 8
    assert {record["source_file"] for record in records} == {path.name for path in knowledge_files}
    assert len({record["id"] for record in records}) == len(records)
    for record in records:
        assert record["title"]
        assert "synthetic" in record["content"].lower() or "合成" in record["content"]