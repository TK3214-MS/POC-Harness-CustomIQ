"""Synthetic Healthcare dataset generator (Industry Pack plugin module).

Loaded dynamically by iq_platform.orchestration.industry_pack_loader - NOT
imported as a dotted Python package. See
docs/decisions/0010-industry-pack-plugin-loading.md.

All data is COMPLETELY SYNTHETIC. No real patients, providers, or clinical
events are used or represented. Reasons/event descriptions are deliberately
generic and administrative (not diagnostic) - see instruction section 9.4 and
23, and SECURITY.md.
"""
from __future__ import annotations

import random
from dataclasses import asdict, dataclass

_AGE_BANDS = ["18-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80+"]
_PROVIDER_ROLES = [
    "Attending Physician (synthetic)", "Nurse Practitioner (synthetic)",
    "Care Coordinator (synthetic)", "Specialist Consultant (synthetic)",
]
_ENCOUNTER_REASONS = [
    "Routine follow-up visit (synthetic)", "Annual wellness check (synthetic)",
    "Follow-up on prior visit (synthetic)", "General consultation (synthetic)",
]
_EVENT_TYPES = ["vital_signs_recorded", "lab_test_ordered", "care_note_added", "medication_review_noted"]


@dataclass
class SyntheticPatient:
    patient_id: str
    age_band: str
    note: str = "Fully synthetic patient; not a real person."


@dataclass
class Provider:
    provider_id: str
    role: str


@dataclass
class Encounter:
    encounter_id: str
    patient_id: str
    provider_id: str
    encounter_date: str
    reason: str


@dataclass
class ClinicalEvent:
    event_id: str
    encounter_id: str
    event_type: str
    description: str
    recorded_at: str


_SCALE_COUNTS = {
    "demo": {"patients": 5, "providers": 4, "encounters": 15, "clinical_events": 30},
    "realistic": {"patients": 300, "providers": 60, "encounters": 1500, "clinical_events": 4000},
    "enterprise": {"patients": 5000, "providers": 500, "encounters": 20000, "clinical_events": 60000},
}


def generate_dataset(seed: int = 42, scale: str = "demo") -> dict:
    """Generate a fully synthetic Healthcare dataset. Deterministic for a given
    seed. Contains no real patient data, diagnoses, or medication names."""
    if scale not in _SCALE_COUNTS:
        raise ValueError(f"Unknown scale '{scale}', expected one of {list(_SCALE_COUNTS)}")
    counts = _SCALE_COUNTS[scale]
    rng = random.Random(seed)

    patients = [
        SyntheticPatient(patient_id=f"PT-{i + 1:05d}", age_band=rng.choice(_AGE_BANDS))
        for i in range(counts["patients"])
    ]
    providers = [
        Provider(provider_id=f"PROV-{i + 1:04d}", role=rng.choice(_PROVIDER_ROLES))
        for i in range(counts["providers"])
    ]

    encounters = []
    for i in range(counts["encounters"]):
        patient = rng.choice(patients)
        provider = rng.choice(providers)
        encounters.append(
            Encounter(
                encounter_id=f"ENC-{i + 1:05d}",
                patient_id=patient.patient_id,
                provider_id=provider.provider_id,
                encounter_date=f"2026-{rng.randint(1, 8):02d}-{rng.randint(1, 28):02d}",
                reason=rng.choice(_ENCOUNTER_REASONS),
            )
        )

    clinical_events = []
    for i in range(counts["clinical_events"]):
        encounter = rng.choice(encounters)
        clinical_events.append(
            ClinicalEvent(
                event_id=f"EVT-{i + 1:05d}",
                encounter_id=encounter.encounter_id,
                event_type=rng.choice(_EVENT_TYPES),
                description=f"Synthetic {rng.choice(_EVENT_TYPES).replace('_', ' ')} entry.",
                recorded_at=encounter.encounter_date,
            )
        )

    return {
        "patients": [asdict(p) for p in patients],
        "providers": [asdict(p) for p in providers],
        "encounters": [asdict(e) for e in encounters],
        "clinical_events": [asdict(e) for e in clinical_events],
    }
