"""Manufacturing Local Preview end-to-end test (Phase 2 exit criterion).

Runs the full stack: Industry Pack manifest -> generated dataset -> Simulated
Work IQ + Mock Foundry IQ + Mock Fabric IQ adapters -> MCP Backend (in-process,
via FastAPI TestClient) -> Local Orchestrator -> AgentResponse.

Phase 2 exit criteria (instruction section 26): E2E test passes, sample output
is saved, mock disclosure is shown, reset works. All four are exercised below.
"""
from __future__ import annotations

import json
from pathlib import Path

from iq_platform.contracts.agent_response import AgentResponse, ExecutionMode
from iq_platform.orchestration.generic_orchestrator import GenericLocalOrchestrator

REPO_ROOT = Path(__file__).resolve().parents[2]
MANUFACTURING_PACK_DIR = REPO_ROOT / "industry-packs" / "manufacturing"
SAMPLE_OUTPUT_PATH = (
    REPO_ROOT / "docs" / "architecture" / "sample-outputs" / "manufacturing-quality-issue-investigation.json"
)


def test_manufacturing_quality_issue_investigation_e2e(tmp_path):
    orchestrator = GenericLocalOrchestrator(MANUFACTURING_PACK_DIR, scale="demo", seed=42)
    response = orchestrator.run_scenario()

    # Core response is populated end-to-end from all three IQ layers + MCP Backend.
    assert response.executive_summary
    assert response.confirmed_facts
    assert response.data_sources_used == [
        "simulated_work_context_adapter",
        "mock_knowledge_adapter",
        "mock_semantic_adapter",
        "mcp_backend (mock)",
    ]
    assert response.documents_and_citations, "Foundry IQ mock adapter should return at least one citation"
    assert response.entities_and_relationships, "Fabric IQ mock adapter should return at least one relationship"
    assert response.mcp_tool_results, "MCP Backend should return at least one tool result"
    assert response.recommended_next_actions
    assert response.human_in_the_loop_requirements
    assert response.execution_mode == ExecutionMode.LOCAL_PREVIEW

    # Mock/Simulation disclosure must be present and mention every mocked layer.
    disclosure = response.mock_or_simulation_disclosure.lower()
    assert "synthetic" in disclosure
    assert "simulated" in disclosure
    assert "mock" in disclosure

    assert response.responsible_ai_notice
    assert response.trace_or_correlation_id

    # Sample output is saved (ephemeral here, proving the save path itself works;
    # a real committed sample is checked separately below).
    scratch_output = tmp_path / "sample_output.json"
    scratch_output.write_text(response.model_dump_json(indent=2), encoding="utf-8")
    assert scratch_output.exists()
    saved = json.loads(scratch_output.read_text(encoding="utf-8"))
    assert saved["mock_or_simulation_disclosure"] == response.mock_or_simulation_disclosure


def test_manufacturing_scenario_is_deterministic_for_fixed_seed():
    """Same seed/scale must produce the same investigated issue and facts, so the
    committed sample output and demo prompts stay meaningful across runs."""
    first = GenericLocalOrchestrator(MANUFACTURING_PACK_DIR, scale="demo", seed=42).run_scenario()
    second = GenericLocalOrchestrator(MANUFACTURING_PACK_DIR, scale="demo", seed=42).run_scenario()
    assert first.confirmed_facts == second.confirmed_facts
    assert first.executive_summary == second.executive_summary


def test_committed_sample_output_matches_current_schema():
    """A real sample output is committed under docs/ for documentation purposes
    (Phase 2 exit criterion: 'sample output is saved'). This test ensures it
    stays in sync with the current AgentResponse schema instead of silently
    rotting - regenerate it via `run-demo` if this test fails."""
    assert SAMPLE_OUTPUT_PATH.exists(), (
        "Committed sample output is missing - regenerate it with the run-demo CLI command "
        "(see docs/architecture/sample-outputs/README.md)"
    )
    raw = json.loads(SAMPLE_OUTPUT_PATH.read_text(encoding="utf-8"))
    AgentResponse.model_validate(raw)  # raises if the committed sample no longer matches the schema


def test_reset_clears_generated_demo_output(tmp_path, monkeypatch):
    from demo_cli import cli

    fake_output_dir = tmp_path / "output"
    fake_output_dir.mkdir()
    (fake_output_dir / "last_run.json").write_text("{}", encoding="utf-8")

    monkeypatch.setattr(cli, "OUTPUT_DIR", fake_output_dir)
    exit_code = cli._cmd_reset(None)
    assert exit_code == 0
    assert list(fake_output_dir.glob("*")) == []
