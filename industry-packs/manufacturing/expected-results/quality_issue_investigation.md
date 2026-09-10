# Expected Results: Manufacturing Quality Issue Investigation (Phase 2 draft)

> This is a qualitative description for human/manual review. Automated evaluation against this document is not yet implemented (see `evaluations/rubric.yaml` and `iq_platform/evaluation/README.md`, planned for a later phase).

For the prompt "Investigate the most recent quality issue and recommend next actions", a correct `AgentResponse` should:

- Name the specific `issue_id` being investigated in `executive_summary`.
- List at least the detected date, severity, and defect rate in `confirmed_facts`.
- Include at least one citation from the Manufacturing knowledge documents in `documents_and_citations`.
- Include at least the `affects` and `observedAt` relationships in `entities_and_relationships`.
- Include results from at least `get_part_traceability` and `recommend_quality_actions` in `mcp_tool_results`.
- Flag missing engineering change follow-up in `uncertainty_and_conflicts` when applicable.
- Include at least one human approval requirement referencing a quality engineer or engineering lead.
- Set `execution_mode` to `local_preview` and disclose mock/simulated status in `mock_or_simulation_disclosure`.

A real captured example is committed at [docs/architecture/sample-outputs/manufacturing-quality-issue-investigation.json](../../../docs/architecture/sample-outputs/manufacturing-quality-issue-investigation.json).
