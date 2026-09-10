"""Integration test: correlation ID propagation through logging (instruction
§5.6 Observability). Verifies GenericLocalOrchestrator's log lines carry the
same correlation_id as the AgentResponse it returns.
"""
from __future__ import annotations

import logging
from pathlib import Path

from iq_platform.orchestration.generic_orchestrator import GenericLocalOrchestrator

REPO_ROOT = Path(__file__).resolve().parents[2]
MANUFACTURING_PACK_DIR = REPO_ROOT / "industry-packs" / "manufacturing"


def test_orchestrator_logs_carry_the_response_correlation_id(caplog):
    orchestrator = GenericLocalOrchestrator(MANUFACTURING_PACK_DIR, scale="demo", seed=42)
    with caplog.at_level(logging.INFO, logger="iq_platform.orchestration.generic_orchestrator"):
        response = orchestrator.run_scenario()

    trace_id = response.trace_or_correlation_id
    matching_records = [r for r in caplog.records if getattr(r, "correlation_id", None) == trace_id]
    assert matching_records, "Expected at least one log record tagged with the response's correlation_id"
    assert any("Starting" in r.message for r in matching_records)
    assert any("Completed" in r.message for r in matching_records)
