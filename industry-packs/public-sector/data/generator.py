"""Synthetic Public Sector dataset generator (Industry Pack plugin module).

Loaded dynamically by iq_platform.orchestration.industry_pack_loader - NOT
imported as a dotted Python package. See
docs/decisions/0010-industry-pack-plugin-loading.md.

All data is COMPLETELY SYNTHETIC. No real citizens or agencies are used or
represented. Agency names are deliberately labeled "(synthetic)". See
instruction section 9.5 and 23, and SECURITY.md.
"""
from __future__ import annotations

import random
from dataclasses import asdict, dataclass

_AGENCY_NAMES = [
    "Department of Synthetic Records (synthetic)",
    "Bureau of Synthetic Permits (synthetic)",
    "Office of Synthetic Licensing (synthetic)",
]
_CASE_TYPES = ["permit_review", "benefit_application", "license_renewal", "zoning_variance"]
_CASE_STATUSES = ["open", "under_review", "pending_decision", "closed"]
_APPLICATION_TYPES = ["initial_application", "renewal_application", "appeal"]
_APPLICATION_STATUSES = ["submitted", "in_review", "approved", "denied", "pending_more_info"]


@dataclass
class SyntheticCitizen:
    citizen_id: str
    note: str = "Fully synthetic citizen; not a real person."


@dataclass
class Agency:
    agency_id: str
    name: str


@dataclass
class Case:
    case_id: str
    citizen_id: str
    agency_id: str
    case_type: str
    status: str
    opened_at: str


@dataclass
class Application:
    application_id: str
    case_id: str
    application_type: str
    status: str
    submitted_at: str


_SCALE_COUNTS = {
    "demo": {"citizens": 8, "agencies": 3, "cases": 10, "applications": 12},
    "realistic": {"citizens": 500, "agencies": 15, "cases": 1200, "applications": 1500},
    "enterprise": {"citizens": 10000, "agencies": 50, "cases": 15000, "applications": 22000},
}


def generate_dataset(seed: int = 42, scale: str = "demo") -> dict:
    """Generate a fully synthetic Public Sector dataset. Deterministic for a
    given seed. Contains no real citizen or agency data."""
    if scale not in _SCALE_COUNTS:
        raise ValueError(f"Unknown scale '{scale}', expected one of {list(_SCALE_COUNTS)}")
    counts = _SCALE_COUNTS[scale]
    rng = random.Random(seed)

    citizens = [SyntheticCitizen(citizen_id=f"CIT-{i + 1:05d}") for i in range(counts["citizens"])]
    agencies = [
        Agency(agency_id=f"AGY-{i + 1:03d}", name=f"{_AGENCY_NAMES[i % len(_AGENCY_NAMES)]} #{i + 1}")
        for i in range(counts["agencies"])
    ]

    cases = []
    for i in range(counts["cases"]):
        citizen = rng.choice(citizens)
        agency = rng.choice(agencies)
        cases.append(
            Case(
                case_id=f"CASE-{i + 1:05d}",
                citizen_id=citizen.citizen_id,
                agency_id=agency.agency_id,
                case_type=rng.choice(_CASE_TYPES),
                status=rng.choice(_CASE_STATUSES),
                opened_at=f"2026-{rng.randint(1, 8):02d}-{rng.randint(1, 28):02d}",
            )
        )

    applications = []
    for i in range(counts["applications"]):
        case = rng.choice(cases)
        applications.append(
            Application(
                application_id=f"APP-{i + 1:05d}",
                case_id=case.case_id,
                application_type=rng.choice(_APPLICATION_TYPES),
                status=rng.choice(_APPLICATION_STATUSES),
                submitted_at=case.opened_at,
            )
        )

    return {
        "citizens": [asdict(c) for c in citizens],
        "agencies": [asdict(a) for a in agencies],
        "cases": [asdict(c) for c in cases],
        "applications": [asdict(a) for a in applications],
    }
