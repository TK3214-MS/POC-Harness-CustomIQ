"""Synthetic Manufacturing dataset generator (Industry Pack plugin module).

Loaded dynamically by iq_platform.orchestration.industry_pack_loader because
"industry-packs" contains a hyphen and is not a valid Python package name.

All data is synthetic. Names are drawn from invented place/company/part name
pools; no real companies, people, or locations are used. See instruction
section 23 and SECURITY.md.
"""
from __future__ import annotations

import random
from dataclasses import asdict, dataclass, field

_FICTIONAL_PLACES = [
    "Lindmoor", "Aurelport", "Kestrel Bay", "Draymoor", "Verdant Hollow",
    "Northfell", "Emberfield", "Stonebrook Junction", "Marrow Vale", "Windrift",
]

_SUPPLIER_NAME_STEMS = [
    "Northfield", "Riverside", "Kestrel", "Ashgrove", "Ironwood", "Cobalt Peak",
    "Silverline", "Amberfield", "Graystone", "Windrift",
]
_SUPPLIER_SUFFIXES = ["Components Co.", "Precision Works", "Fabrication Ltd.", "Metal Forms Inc.", "Tooling Group"]

_PART_STEMS = [
    "Bracket", "Housing", "Sensor Module", "Gasket", "Bearing Assembly",
    "Wiring Harness", "Valve Body", "Actuator", "Coupling", "Bushing",
]

_ISSUE_SUMMARIES = [
    "Dimensional deviation detected during incoming inspection",
    "Intermittent sensor reading failure under load",
    "Surface finish outside specification",
    "Fastener torque inconsistency observed on assembly line",
    "Material hardness below specification",
    "Seal leakage detected during pressure test",
]

_SEVERITIES = ["low", "medium", "high", "critical"]
_ISSUE_STATUSES = ["open", "investigating", "engineering_review", "resolved"]
_CHANGE_STATUSES = ["proposed", "in_progress", "approved", "implemented"]


@dataclass
class Factory:
    factory_id: str
    name: str
    location: str


@dataclass
class ProductionLine:
    line_id: str
    factory_id: str
    name: str


@dataclass
class Supplier:
    supplier_id: str
    name: str
    region: str
    reliability_score: float


@dataclass
class Part:
    part_id: str
    name: str
    supplier_id: str
    used_in_line_ids: list[str] = field(default_factory=list)


@dataclass
class QualityIssue:
    issue_id: str
    part_id: str
    factory_id: str
    summary: str
    severity: str
    status: str
    defect_rate_percent: float
    detected_at: str


@dataclass
class EngineeringChange:
    change_id: str
    issue_id: str
    description: str
    status: str
    created_at: str


# "scale" controls dataset size. "realistic" targets thousands of records for
# higher-cardinality entity types (Part, QualityIssue, EngineeringChange).
# Lower-cardinality entities such as Factory do not need thousands of rows.
_SCALE_COUNTS = {
    "demo": {
        "factories": 3,
        "production_lines_per_factory": 2,
        "suppliers": 5,
        "parts": 20,
        "quality_issues": 15,
        "engineering_changes": 8,
    },
    "realistic": {
        "factories": 12,
        "production_lines_per_factory": 4,
        "suppliers": 150,
        "parts": 900,
        "quality_issues": 2500,
        "engineering_changes": 900,
    },
    "enterprise": {
        "factories": 40,
        "production_lines_per_factory": 8,
        "suppliers": 1000,
        "parts": 5000,
        "quality_issues": 12000,
        "engineering_changes": 5000,
    },
}


def generate_dataset(seed: int = 42, scale: str = "demo") -> dict:
    """Generate a fully synthetic Manufacturing dataset.

    Deterministic for a given seed, so repeated runs/tests are reproducible
    without committing generated data to git (see .gitignore).
    """
    if scale not in _SCALE_COUNTS:
        raise ValueError(f"Unknown scale '{scale}', expected one of {list(_SCALE_COUNTS)}")
    counts = _SCALE_COUNTS[scale]
    rng = random.Random(seed)

    factories = []
    for i in range(counts["factories"]):
        place = rng.choice(_FICTIONAL_PLACES)
        factories.append(Factory(factory_id=f"FAC-{i + 1:03d}", name=f"{place} Plant {i + 1}", location=place))

    production_lines: list[ProductionLine] = []
    for factory in factories:
        for j in range(counts["production_lines_per_factory"]):
            production_lines.append(
                ProductionLine(
                    line_id=f"LINE-{factory.factory_id}-{j + 1}",
                    factory_id=factory.factory_id,
                    name=f"{factory.name} Line {j + 1}",
                )
            )

    suppliers = [
        Supplier(
            supplier_id=f"SUP-{i + 1:04d}",
            name=f"{rng.choice(_SUPPLIER_NAME_STEMS)} {rng.choice(_SUPPLIER_SUFFIXES)} #{i + 1}",
            region=rng.choice(_FICTIONAL_PLACES),
            reliability_score=round(rng.uniform(0.7, 0.99), 2),
        )
        for i in range(counts["suppliers"])
    ]

    parts = []
    for i in range(counts["parts"]):
        supplier = rng.choice(suppliers)
        used_lines = rng.sample(production_lines, k=min(len(production_lines), rng.randint(1, 3)))
        parts.append(
            Part(
                part_id=f"PART-{i + 1:05d}",
                name=f"{rng.choice(_PART_STEMS)} {i + 1}",
                supplier_id=supplier.supplier_id,
                used_in_line_ids=[line.line_id for line in used_lines],
            )
        )

    quality_issues = []
    for i in range(counts["quality_issues"]):
        part = rng.choice(parts)
        candidate_lines = [line for line in production_lines if line.line_id in part.used_in_line_ids]
        used_line = candidate_lines[0] if candidate_lines else rng.choice(production_lines)
        quality_issues.append(
            QualityIssue(
                issue_id=f"QI-{i + 1:05d}",
                part_id=part.part_id,
                factory_id=used_line.factory_id,
                summary=rng.choice(_ISSUE_SUMMARIES),
                severity=rng.choice(_SEVERITIES),
                status=rng.choice(_ISSUE_STATUSES),
                defect_rate_percent=round(rng.uniform(0.1, 12.0), 2),
                detected_at=f"2026-{rng.randint(1, 8):02d}-{rng.randint(1, 28):02d}",
            )
        )

    engineering_changes = []
    change_count = min(len(quality_issues), counts["engineering_changes"])
    issues_with_changes = rng.sample(quality_issues, k=change_count)
    for i, issue in enumerate(issues_with_changes):
        engineering_changes.append(
            EngineeringChange(
                change_id=f"EC-{i + 1:05d}",
                issue_id=issue.issue_id,
                description=f"Engineering change addressing: {issue.summary.lower()}",
                status=rng.choice(_CHANGE_STATUSES),
                created_at=issue.detected_at,
            )
        )

    return {
        "factories": [asdict(f) for f in factories],
        "production_lines": [asdict(pl) for pl in production_lines],
        "suppliers": [asdict(s) for s in suppliers],
        "parts": [asdict(p) for p in parts],
        "quality_issues": [asdict(qi) for qi in quality_issues],
        "engineering_changes": [asdict(ec) for ec in engineering_changes],
    }
