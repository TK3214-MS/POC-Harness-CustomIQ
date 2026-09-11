"""Export deterministic enterprise-scale Industry Pack datasets to CSV.

The generated files are synthetic and intended for optional Fabric Lakehouse
loading. The generators remain the source of truth so the export is repeatable.
"""
from __future__ import annotations

import csv
import importlib.util
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PACKS = ("manufacturing", "financial-services", "retail", "healthcare", "public-sector")


def load_generator(pack_id: str):
    path = REPO_ROOT / "industry-packs" / pack_id / "data" / "generator.py"
    spec = importlib.util.spec_from_file_location(f"{pack_id}_enterprise_generator", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load generator: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def export_pack(pack_id: str) -> dict[str, int]:
    dataset = load_generator(pack_id).generate_dataset(seed=20260911, scale="enterprise")
    output_dir = REPO_ROOT / "industry-packs" / pack_id / "sample-data" / "fabric" / "enterprise"
    output_dir.mkdir(parents=True, exist_ok=True)
    knowledge_dir = REPO_ROOT / "industry-packs" / pack_id / "sample-data" / "foundry" / "enterprise"
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    counts: dict[str, int] = {}
    knowledge_path = knowledge_dir / "records.jsonl"
    with knowledge_path.open("w", encoding="utf-8") as handle:
        for entity_name, rows in dataset.items():
            for index, row in enumerate(rows, start=1):
                record = {
                    "id": f"{pack_id}-{entity_name}-{index:07d}",
                    "industry": pack_id,
                    "entity_type": entity_name,
                    "content": json.dumps(row, ensure_ascii=True, sort_keys=True),
                }
                handle.write(json.dumps(record, ensure_ascii=True) + "\n")
    for entity_name, rows in dataset.items():
        if not rows:
            continue
        output_path = output_dir / f"{entity_name}.csv"
        fieldnames = list(rows[0])
        with output_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                normalized = {
                    key: json.dumps(value, ensure_ascii=True) if isinstance(value, (list, dict)) else value
                    for key, value in row.items()
                }
                writer.writerow(normalized)
        counts[entity_name] = len(rows)
    return counts


def main() -> None:
    for pack_id in PACKS:
        counts = export_pack(pack_id)
        total = sum(counts.values())
        print(f"{pack_id}: {total} rows across {len(counts)} tables")


if __name__ == "__main__":
    main()
