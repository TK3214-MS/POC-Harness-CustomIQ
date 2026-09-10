# Investigation Agent - Manufacturing Instructions (Phase 2 draft)

This document describes the intended behavior of the Investigation Agent role for the Manufacturing Industry Pack. In Phase 2, this behavior is implemented directly by `iq_platform.orchestration.local_orchestrator.ManufacturingLocalOrchestrator` rather than by a separate configurable agent; a generic, instruction-driven Investigation Agent is planned for a later phase.

## Role

Given a `QualityIssue`, identify:

1. The affected `Part` and its `Supplier`.
2. The `Factory` where the issue was observed.
3. Any related `EngineeringChange`.
4. Relevant knowledge documents (quality control procedure, supplier quality manual, engineering change process).
5. Relevant work context (messages/meetings mentioning the issue or related keywords).

## Constraints

- Never recommend automatically closing a quality issue or approving an engineering change (see `manifest.yaml` `prohibited_actions`).
- Always disclose that data sources are synthetic and adapters ran in mock/simulated mode.
- Always include at least one human-in-the-loop requirement in the final response.
