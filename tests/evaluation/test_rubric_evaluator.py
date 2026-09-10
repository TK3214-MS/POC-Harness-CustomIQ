"""Tests for the rubric evaluation engine (Phase 6). Runs each Industry Pack's
real default scenario through GenericLocalOrchestrator and its real
evaluations/rubric.yaml through evaluate_response() - no fabricated fixtures.
"""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from iq_platform.evaluation.rubric_evaluator import evaluate_response
from iq_platform.orchestration.generic_orchestrator import GenericLocalOrchestrator

REPO_ROOT = Path(__file__).resolve().parents[2]
INDUSTRY_PACKS_DIR = REPO_ROOT / "industry-packs"

ALL_PACK_IDS = ["manufacturing", "financial-services", "retail", "healthcare", "public-sector"]


@pytest.mark.parametrize("pack_id", ALL_PACK_IDS)
def test_default_scenario_passes_its_own_rubric(pack_id: str):
    pack_dir = INDUSTRY_PACKS_DIR / pack_id
    orchestrator = GenericLocalOrchestrator(pack_dir, scale="demo", seed=42)
    response = orchestrator.run_scenario()

    rubric = yaml.safe_load((pack_dir / "evaluations" / "rubric.yaml").read_text(encoding="utf-8"))
    results = evaluate_response(response, rubric)

    assert results, f"{pack_id}: rubric produced no results"
    failures = [r for r in results if r["status"] == "fail"]
    assert not failures, f"{pack_id}: rubric failures: {failures}"
    # Every criterion in the pack's rubric must be either checked automatically
    # or explicitly flagged as needing manual review - never silently ignored.
    assert all(r["status"] in ("pass", "not_automatically_checked") for r in results)


def test_unknown_criterion_id_is_reported_as_not_automatically_checked():
    pack_dir = INDUSTRY_PACKS_DIR / "manufacturing"
    orchestrator = GenericLocalOrchestrator(pack_dir, scale="demo", seed=42)
    response = orchestrator.run_scenario()

    rubric = {"criteria": [{"id": "some_future_criterion", "description": "not implemented yet"}]}
    results = evaluate_response(response, rubric)
    assert results == [
        {
            "id": "some_future_criterion",
            "description": "not implemented yet",
            "status": "not_automatically_checked",
            "detail": "No automated check implemented for this criterion id - requires manual review.",
        }
    ]
