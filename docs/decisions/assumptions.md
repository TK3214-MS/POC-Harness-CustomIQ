# Assumptions Log

Status: Living document. Every assumption below is a **reasonable local default**, not a verified Microsoft product fact. Anything about Microsoft product behavior, licensing, pricing, or availability is tracked separately in [product-verification.md](./product-verification.md) and must never be promoted out of "TBD" status without an external source.

## How to read this file

- **Assumption**: what we chose.
- **Reason**: why, given the instruction document and repo state on 2026-09-08.
- **Reversible?**: whether changing it later requires a breaking change to contracts/schemas.
- **Owner action needed?**: whether a human stakeholder should confirm/override this before Phase 3+.

---

## A1. Repository root = accelerator root

**Assumption**: The workspace root (`/Users/tk3214/GitHub/POC-Harness-CustomIQ`) *is* the `industry-iq-platform/` root described in the instructions, rather than nesting an extra `industry-iq-platform/` folder inside the repo.
**Reason**: The repo already contains `LICENSE` at root and no nested folder. Nesting would create an awkward double root for a git repo.
**Reversible?**: Yes, cosmetic.
**Owner action needed?**: No.

## A2. Primary implementation language: Python

**Assumption**: Platform orchestration, adapters, MCP backend (FastAPI is explicitly required), CLI, and test suites are implemented in Python (3.11+).
**Reason**: The instructions mandate FastAPI for the MCP Backend. Using one language across orchestration/adapters/backend/tests minimizes cross-language contract drift for a solo/near-term build, and Python has mature libraries for Pydantic schema validation, YAML parsing, and CLI tooling (Typer/Click).
**Reversible?**: Partially — adapter/tool contracts are language-agnostic (JSON over HTTP), so a future rewrite of one component in another language is possible without breaking contracts.
**Owner action needed?**: Confirm if there is an organizational preference for .NET/TypeScript instead (e.g., to match Copilot Studio/Power Platform tooling conventions).

## A3. Demo UI deferred, Demo CLI first

**Assumption**: `apps/demo-cli/` is implemented before `apps/demo-ui/`. The web/desktop UI is a Phase 2+ nice-to-have, not a Phase 0/1 blocker.
**Reason**: Section 28 lists a CLI command surface (`setup`, `validate`, `health`, ...) as the baseline experience; a UI is additive. Building CLI first lets contract/adapter work be validated headlessly.
**Reversible?**: Yes.
**Owner action needed?**: No, unless a UI is required for the first demo milestone.

## A4. Documentation language: Japanese only (for now)

**Assumption**: All customer-facing and internal documentation (README, guides, ADRs) is authored in Japanese for now, per stakeholder decision (2026-09-08, resolved [Q1](./open-questions.md)). An English translation pass may be added later if the accelerator needs to go external/global, but is not in scope until requested.
**Reason**: Explicit stakeholder answer to open question Q1.
**Reversible?**: Yes, but re-translating later is costly.
**Owner action needed?**: No — resolved.

## A5. Manifest validation via Pydantic v2 + JSON Schema export

**Assumption**: Industry Pack `manifest.yaml` and Capability Registry entries are validated using Pydantic v2 models, with JSON Schema exported for tooling/CI use.
**Reason**: Section 8 explicitly allows "JSON Schema or Pydantic model"; Pydantic gives us both validation and typed Python objects for the orchestrator with one definition.
**Reversible?**: Yes.
**Owner action needed?**: No.

## A6. Default Industry Pack = Manufacturing

**Assumption**: Manufacturing is the default pack loaded by Local Preview Mode and the only pack fully implemented end-to-end in Phase 2.
**Reason**: Explicitly stated in sections 9.1, 14.3 (implicitly), 15, and 19.
**Reversible?**: N/A, explicit requirement.
**Owner action needed?**: No.

## A7. "Mock", "Simulated", "Live" mode terminology is used verbatim in code and UI

**Assumption**: Adapter `mode` field uses the exact enum from section 6.1 (`live`, `mock`, `simulated`, `unavailable`, `verification_required`), surfaced verbatim in logs, CLI output, and agent responses.
**Reason**: Ensures consistent, greppable disclosure of mock/simulation status per sections 3.8, 14, and Definition of Done.
**Reversible?**: Changing enum values later is a breaking contract change.
**Owner action needed?**: No.

## A8. Mock/Simulated first (Phase 0–3), Live validated against a real test subscription from Phase 4 onward

**Assumption**: Phase 0–3 (contracts, 5 Industry Packs, contract/E2E tests) still uses only Mock/Simulated adapters — this is a build-order decision, not a statement that Live services are unavailable. Per stakeholder decision (2026-09-08, resolved [Q3](./open-questions.md) and [Q4](./open-questions.md)): the real Microsoft products (Copilot Studio, Work IQ, Foundry IQ, Fabric IQ) are assumed available, and a **test Azure subscription** will be provided so Live adapters can be implemented and validated for real in Phase 4/5, including Full Hybrid Mode testing. Any manual SaaS-side configuration/setup required to reach that state must be written up in the SaaS Configuration Guide (§20) as it is discovered.
**Reason**: Explicit stakeholder answers to open questions Q3/Q4; instructions still require safe-failure and no silent fallback when a Live adapter is not yet reachable.
**Reversible?**: N/A, sequencing decision.
**Owner action needed?**: Provide actual tenant ID / subscription ID / Copilot Studio environment ID / Fabric workspace ID etc. via `.env` (never committed) when Phase 4 work starts.

## A9. License for the accelerator itself: MIT (already present)

**Assumption**: The existing root `LICENSE` (MIT, © 2026 Yasuki Takami) is retained as-is and applies to the accelerator code. Not overwritten.
**Reason**: Pre-existing file; instructions do not request a license change.
**Reversible?**: Yes.
**Owner action needed?**: No.

## A10. Deployment tooling priority

**Assumption**: Per section 15's explicit priority, `azd` (Azure Developer CLI) is implemented first in Phase 5; Bicep second; Terraform only if time permits, and never represented as "done" unless actually completed and tested.
**Reason**: Directly specified priority order.
**Reversible?**: N/A.
**Owner action needed?**: No.

## A11. Synthetic data volume: thousands of records per entity type

**Assumption**: Sample data generators for every Industry Pack target realistic scale (thousands of records per major entity type, e.g. `Transaction`, `QualityIssue`, `Order`), not a minimal "tens of records" demo set.
**Reason**: Explicit stakeholder answer to open question Q10 — realism was preferred over minimal footprint.
**Reversible?**: Yes, but affects mock adapter pagination/filtering design and evaluation-test runtime — should be decided before Phase 2 data generator work.
**Owner action needed?**: No — resolved. Note: 30-minute demo scenarios will still query/filter down to a small relevant subset at run time, so demo pacing is unaffected by the larger underlying dataset.

## A12. CI is live, not just authored

**Assumption**: `.github/workflows/` pipelines (lint, unit, contract, security scan) are expected to actually run in GitHub Actions for this repo, not just be authored as inert reference files.
**Reason**: Explicit stakeholder answer to open question Q5 confirming CI availability.
**Reversible?**: Yes.
**Owner action needed?**: Flag any required repo secrets/environment configuration in documentation as they are identified (per stakeholder request); no secrets will be committed.
