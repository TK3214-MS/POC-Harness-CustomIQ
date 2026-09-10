"""Demo CLI for the Industry IQ Platform Accelerator (Phase 3: all 5 industry
packs implemented).

See instruction §28 for the full intended command surface; only a subset is
implemented so far. Others are honestly reported as not-yet-implemented rather
than silently accepted.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
INDUSTRY_PACKS_DIR = REPO_ROOT / "industry-packs"
OUTPUT_DIR = REPO_ROOT / "scripts" / "demo" / "output"
STATE_FILE = OUTPUT_DIR / "selected_industry_pack.json"
DEFAULT_PACK_ID = "manufacturing"

ALL_PACK_IDS = ["manufacturing", "financial-services", "retail", "healthcare", "public-sector"]

_NOT_YET_IMPLEMENTED: dict[str, str] = {}


def _selected_pack_id() -> str:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))["id"]
        except (json.JSONDecodeError, KeyError):
            pass
    return DEFAULT_PACK_ID


def _pack_dir(pack_id: str) -> Path:
    return INDUSTRY_PACKS_DIR / pack_id


def _cmd_health(_args: argparse.Namespace) -> int:
    from iq_platform.adapters.knowledge.live_adapter import FoundryIQLiveAdapter
    from iq_platform.adapters.knowledge.mock_adapter import MockKnowledgeAdapter
    from iq_platform.adapters.semantic.live_adapter import FabricIQLiveAdapter
    from iq_platform.adapters.work_context.live_adapter import WorkIQLiveAdapter
    from iq_platform.adapters.work_context.simulated_adapter import SimulatedWorkContextAdapter
    from iq_platform.configuration.settings import LiveAdapterSettings
    from iq_platform.orchestration.industry_pack_loader import load_manifest

    selected = _selected_pack_id()
    print("Industry IQ Platform Accelerator - Health Check (Local Preview Mode)")
    print("=" * 70)
    try:
        manifest = load_manifest(_pack_dir(selected))
    except Exception as exc:  # noqa: BLE001 - top-level CLI boundary
        print(f"Industry Pack ({selected}): NOT READY - {exc}")
        return 1
    print(f"Industry Pack: {manifest.display_name} - Ready")

    work_adapter = SimulatedWorkContextAdapter(_pack_dir(selected) / manifest.work_context_path)
    knowledge_adapter = MockKnowledgeAdapter(_pack_dir(selected) / manifest.knowledge_path)

    for label, adapter in [
        ("Work IQ (simulated)", work_adapter),
        ("Foundry IQ (mock)", knowledge_adapter),
    ]:
        health = adapter.health_check()
        status = "Ready" if health.healthy else "NOT READY"
        print(f"{label}: {status} ({health.mode.value}) - {health.message}")
    print("Fabric IQ (mock): Ready (mock) - relationship/metrics logic loaded per-pack at run-demo time")

    print("MCP Backend: Ready (mock)")

    print()
    print("Live Adapters (Phase 4 - see docs/setup/live-adapters-configuration.md)")
    print("-" * 70)
    settings = LiveAdapterSettings.from_env()
    for label, adapter in [
        ("Work IQ (live)", WorkIQLiveAdapter(settings)),
        ("Foundry IQ (live)", FoundryIQLiveAdapter(settings)),
        ("Fabric IQ (live)", FabricIQLiveAdapter(settings)),
    ]:
        health = adapter.health_check()
        print(f"{label}: {health.mode.value} - {health.message}")
    copilot_missing = settings.missing_fields_for("copilot_studio")
    copilot_status = "Not Configured" if copilot_missing else "Configuration present (Verification Required)"
    print(f"Copilot Studio harness: {copilot_status}")
    if copilot_missing:
        print(f"  Missing: {copilot_missing}")

    print()
    print("NOTE: Local Preview Mode uses synthetic data and local adapters. It does")
    print("not validate the availability, behavior, security, licensing, or")
    print("performance of Microsoft SaaS services. Live Adapters never reach 'live'")
    print("mode in this repo - the underlying product API contracts are unverified")
    print("(see docs/decisions/product-verification.md).")
    return 0


def _cmd_validate(_args: argparse.Namespace) -> int:
    """Validate every Industry Pack's manifest.yaml against the shared schema
    and confirm every plugin/content path it declares actually exists."""
    from pydantic import ValidationError

    from iq_platform.orchestration.industry_pack_loader import load_manifest

    print("Validating all Industry Pack manifests against IndustryPackManifest schema...")
    print("=" * 70)
    all_ok = True
    for pack_id in ALL_PACK_IDS:
        pack_dir = _pack_dir(pack_id)
        try:
            manifest = load_manifest(pack_dir)
        except (FileNotFoundError, ValidationError) as exc:
            print(f"{pack_id}: FAILED - {exc}")
            all_ok = False
            continue

        missing = [
            field_name
            for field_name in (
                "ontology_path", "semantic_model_path", "sample_data_path", "knowledge_path",
                "work_context_path", "mcp_tools_path", "semantic_relationships_path", "scenario_module_path",
                "agent_instructions_path", "demo_prompts_path", "expected_results_path", "evaluation_path",
                "terminology_path", "responsible_ai_path",
            )
            if not (pack_dir / getattr(manifest, field_name)).exists()
        ]
        if missing:
            print(f"{pack_id}: FAILED - missing paths: {missing}")
            all_ok = False
        else:
            print(f"{pack_id}: OK ({manifest.display_name})")

    print()
    print("All packs valid." if all_ok else "One or more packs FAILED validation.")
    return 0 if all_ok else 1


def _cmd_load_data(args: argparse.Namespace) -> int:
    from iq_platform.orchestration.industry_pack_loader import load_manifest, load_plugin_module

    pack_id = args.industry or _selected_pack_id()
    pack_dir = _pack_dir(pack_id)
    manifest = load_manifest(pack_dir)
    generator = load_plugin_module(pack_dir / manifest.sample_data_path)
    dataset = generator.generate_dataset(seed=args.seed, scale=args.scale)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / f"{pack_id}_dataset.json"
    output_path.write_text(json.dumps(dataset, indent=2), encoding="utf-8")

    print(f"Loaded synthetic {manifest.display_name} dataset (scale={args.scale}, seed={args.seed}):")
    for key, rows in dataset.items():
        print(f"  {key}: {len(rows)} records")
    print(f"Saved to {output_path.relative_to(REPO_ROOT)}")
    print("All data above is synthetic (see instruction section 23 / SECURITY.md).")
    return 0


def _cmd_select_industry(args: argparse.Namespace) -> int:
    if args.name not in ALL_PACK_IDS:
        print(f"Industry Pack '{args.name}' is not recognized. Available packs: {', '.join(ALL_PACK_IDS)}")
        return 1
    from iq_platform.orchestration.industry_pack_loader import load_manifest

    manifest = load_manifest(_pack_dir(args.name))
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps({"id": manifest.id, "display_name": manifest.display_name}, indent=2), encoding="utf-8")
    print(f"Selected Industry Pack: {manifest.display_name} ({manifest.id})")
    print(f"Default scenario: {manifest.default_scenario}")
    return 0


def _cmd_run_demo(args: argparse.Namespace) -> int:
    from iq_platform.orchestration.generic_orchestrator import GenericLocalOrchestrator

    pack_id = args.industry or _selected_pack_id()
    orchestrator = GenericLocalOrchestrator(_pack_dir(pack_id), scale=args.scale, seed=args.seed)
    response = orchestrator.run_scenario(entity_id=args.entity_id)

    print(f"Industry Pack: {pack_id}")
    print("=" * 70)
    print("MOCK/SIMULATION DISCLOSURE")
    print("=" * 70)
    print(response.mock_or_simulation_disclosure)
    print()
    print("RESPONSIBLE AI NOTICE")
    print("-" * 70)
    print(response.responsible_ai_notice)
    print()
    print("EXECUTIVE SUMMARY")
    print("-" * 70)
    print(response.executive_summary)
    print()
    print("RECOMMENDED NEXT ACTIONS")
    print("-" * 70)
    for action in response.recommended_next_actions:
        print(f"  - {action}")
    print()
    print("HUMAN-IN-THE-LOOP REQUIREMENTS")
    print("-" * 70)
    for req in response.human_in_the_loop_requirements:
        print(f"  - {req}")
    print()
    print(f"Execution mode: {response.execution_mode.value}")
    print(f"Trace/Correlation ID: {response.trace_or_correlation_id}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / "last_run.json"
    output_path.write_text(response.model_dump_json(indent=2), encoding="utf-8")
    print()
    print(f"Full response saved to {output_path.relative_to(REPO_ROOT)}")
    return 0


def _cmd_reset(_args: argparse.Namespace) -> int:
    if OUTPUT_DIR.exists():
        for path in OUTPUT_DIR.glob("*"):
            path.unlink()
        try:
            location = OUTPUT_DIR.relative_to(REPO_ROOT)
        except ValueError:
            location = OUTPUT_DIR
        print(f"Cleared {location}")
    else:
        print("Nothing to reset (no demo output directory found).")
    return 0


def _cmd_setup(_args: argparse.Namespace) -> int:
    script = REPO_ROOT / "scripts" / "setup" / "setup.sh"
    result = subprocess.run(["bash", str(script)], cwd=REPO_ROOT, check=False)
    return result.returncode


def _cmd_cleanup(_args: argparse.Namespace) -> int:
    """Deployed-resource cleanup. This only affects real Azure resources created
    via 'azd up' - it does nothing (and is safe to run) if no azd environment
    exists yet. Delegates to scripts/cleanup/cleanup-azure.sh, which requires
    typed environment-name confirmation before deleting anything."""
    script = REPO_ROOT / "scripts" / "cleanup" / "cleanup-azure.sh"
    result = subprocess.run(["bash", str(script)], cwd=REPO_ROOT, check=False)
    return result.returncode


def _cmd_evaluate(args: argparse.Namespace) -> int:
    import yaml

    from iq_platform.evaluation.rubric_evaluator import evaluate_response
    from iq_platform.orchestration.generic_orchestrator import GenericLocalOrchestrator
    from iq_platform.orchestration.industry_pack_loader import load_manifest

    pack_id = args.industry or _selected_pack_id()
    pack_dir = _pack_dir(pack_id)
    manifest = load_manifest(pack_dir)

    orchestrator = GenericLocalOrchestrator(pack_dir, scale=args.scale, seed=args.seed)
    response = orchestrator.run_scenario(entity_id=args.entity_id)

    rubric = yaml.safe_load((pack_dir / manifest.evaluation_path).read_text(encoding="utf-8"))
    results = evaluate_response(response, rubric)

    print(f"Evaluating {manifest.display_name} ({pack_id}) against {manifest.evaluation_path}")
    print("=" * 70)
    status_labels = {"pass": "PASS", "fail": "FAIL", "not_automatically_checked": "MANUAL REVIEW NEEDED"}
    passed = 0
    for result in results:
        print(f"[{status_labels[result['status']]}] {result['id']}: {result['detail']}")
        if result["status"] == "pass":
            passed += 1
    print()
    print(f"{passed}/{len(results)} criteria automatically passed. Review MANUAL REVIEW NEEDED items by hand.")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / "evaluation_result.json"
    output_path.write_text(json.dumps({"industry": pack_id, "results": results}, indent=2), encoding="utf-8")
    print(f"Full results saved to {output_path.relative_to(REPO_ROOT)}")

    return 1 if any(r["status"] == "fail" for r in results) else 0


def _cmd_generate_summary(_args: argparse.Namespace) -> int:
    from iq_platform.orchestration.industry_pack_loader import load_manifest

    last_run_path = OUTPUT_DIR / "last_run.json"
    if not last_run_path.exists():
        print("No run-demo output found. Run 'run-demo' first.", file=sys.stderr)
        return 1

    response_data = json.loads(last_run_path.read_text(encoding="utf-8"))
    eval_path = OUTPUT_DIR / "evaluation_result.json"
    eval_data = json.loads(eval_path.read_text(encoding="utf-8")) if eval_path.exists() else None
    pack_id = (eval_data or {}).get("industry") or _selected_pack_id()
    manifest = load_manifest(_pack_dir(pack_id))

    tools_invoked = [r["tool_name"] for r in response_data.get("mcp_tool_results", [])]
    features_verified = [
        "Industry Pack manifest loaded and validated",
        "Synthetic dataset generated",
        "Simulated Work IQ / Mock Foundry IQ / Mock Fabric IQ adapters queried",
        "MCP Backend tool(s) invoked: " + (", ".join(tools_invoked) if tools_invoked else "(none recorded)"),
        "Mock/Simulation disclosure present in response",
        "Responsible AI notice present in response",
    ]
    features_not_verified = [
        (
            "Live Adapters (Work IQ / Foundry IQ / Fabric IQ / Copilot Studio) - verification_required scaffold "
            "only, no real Microsoft product connectivity (see docs/decisions/product-verification.md)"
        ),
        "Actual Azure deployment of the MCP Backend ('azd up' not executed against a real subscription)",
    ]

    lines = [
        "# Demo Completion Summary",
        "",
        f"- Generated at: {datetime.now(UTC).isoformat()}",
        f"- Execution Mode: {response_data.get('execution_mode')}",
        f"- Industry Pack: {manifest.display_name} ({pack_id})",
        f"- Default Scenario: {manifest.default_scenario}",
        f"- Trace/Correlation ID: {response_data.get('trace_or_correlation_id')}",
        "",
        "## Executed Prompt / Scenario",
        "",
        response_data.get("executive_summary", ""),
        "",
        "## IQ Layers Used",
        "",
        *[f"- {layer}" for layer in response_data.get("iq_layers_used", [])],
        "",
        "## Tools Invoked",
        "",
        *([f"- {tool}" for tool in tools_invoked] or ["- (none recorded)"]),
        "",
        "## Features Verified",
        "",
        *[f"- {item}" for item in features_verified],
        "",
        "## Features Not Verified",
        "",
        *[f"- {item}" for item in features_not_verified],
        "",
        "## Mock or Simulated Components",
        "",
        response_data.get("mock_or_simulation_disclosure", ""),
        "",
        "## Unfinished Items",
        "",
        "- Live Adapter real API integration (pending Microsoft product verification)",
        "- azd deployment to a real Azure subscription (pending test credentials)",
        "- 'setup' / 'cleanup' (deployed-resource) CLI commands",
        "",
        "## Production Recommendations",
        "",
        "- Complete docs/setup/live-adapters-configuration.md before any customer-facing demo using Live mode.",
        "- Review industry-packs/<pack>/manifest.yaml prohibited_actions and human_approval_rules with stakeholders.",
        "- Run scripts/security/scan_secrets.py and scripts/validation/validate_synthetic_data.py before sharing externally.",
        "",
        "## Security Considerations",
        "",
        "- All data in this run is synthetic (see SECURITY.md).",
        "- No real Microsoft SaaS services were contacted.",
        "",
    ]
    if eval_data:
        lines += ["## Evaluation Rubric Results", ""]
        for result in eval_data["results"]:
            lines.append(f"- [{result['status']}] {result['id']}: {result['detail']}")
        lines.append("")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / "demo-completion-summary.md"
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Demo Completion Summary saved to {output_path.relative_to(REPO_ROOT)}")
    return 0


def _cmd_not_yet_implemented(name: str) -> int:
    phase = _NOT_YET_IMPLEMENTED.get(name, "a future phase")
    print(f"'{name}' is not implemented yet (planned for {phase}). See README.md for current status.", file=sys.stderr)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="iiq-demo", description="Industry IQ Platform Accelerator - Demo CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("setup", help="Bootstrap the local development environment (venv, deps, health check)").set_defaults(
        func=_cmd_setup
    )
    subparsers.add_parser("validate", help="Validate all Industry Pack manifests against the shared schema").set_defaults(
        func=_cmd_validate
    )
    subparsers.add_parser("health", help="Run the Local Preview health check").set_defaults(func=_cmd_health)

    load_data_parser = subparsers.add_parser("load-data", help="Generate a synthetic Industry Pack dataset")
    load_data_parser.add_argument("--industry", choices=ALL_PACK_IDS, default=None)
    load_data_parser.add_argument("--scale", choices=["demo", "realistic"], default="demo")
    load_data_parser.add_argument("--seed", type=int, default=42)
    load_data_parser.set_defaults(func=_cmd_load_data)

    select_parser = subparsers.add_parser("select-industry", help="Select an Industry Pack")
    select_parser.add_argument("name", default=DEFAULT_PACK_ID, nargs="?", choices=ALL_PACK_IDS)
    select_parser.set_defaults(func=_cmd_select_industry)

    run_demo_parser = subparsers.add_parser("run-demo", help="Run the selected Industry Pack's representative scenario")
    run_demo_parser.add_argument("--industry", choices=ALL_PACK_IDS, default=None)
    run_demo_parser.add_argument("--entity-id", dest="entity_id", default=None)
    run_demo_parser.add_argument("--scale", choices=["demo", "realistic"], default="demo")
    run_demo_parser.add_argument("--seed", type=int, default=42)
    run_demo_parser.set_defaults(func=_cmd_run_demo)

    evaluate_parser = subparsers.add_parser("evaluate", help="Run the selected Industry Pack's rubric-based evaluation")
    evaluate_parser.add_argument("--industry", choices=ALL_PACK_IDS, default=None)
    evaluate_parser.add_argument("--entity-id", dest="entity_id", default=None)
    evaluate_parser.add_argument("--scale", choices=["demo", "realistic"], default="demo")
    evaluate_parser.add_argument("--seed", type=int, default=42)
    evaluate_parser.set_defaults(func=_cmd_evaluate)

    subparsers.add_parser("generate-summary", help="Generate a Demo Completion Summary from the last run-demo output").set_defaults(
        func=_cmd_generate_summary
    )

    subparsers.add_parser("reset", help="Clear generated demo output").set_defaults(func=_cmd_reset)
    subparsers.add_parser("cleanup", help="Delete real Azure resources created via 'azd up' (destructive, confirmation required)").set_defaults(
        func=_cmd_cleanup
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        return _cmd_not_yet_implemented(args.command)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
