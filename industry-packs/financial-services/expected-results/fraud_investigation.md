# Expected Results: Financial Fraud Investigation (Phase 3 draft)

> Qualitative description for human/manual review. Automated evaluation is not yet implemented.

For the prompt "Investigate the most recent fraud case and recommend next steps", a correct `AgentResponse` should:

- Name the specific `case_id` in `executive_summary`.
- List the risk score, status, and flagged transaction amount in `confirmed_facts`.
- Include at least one citation from the Financial Services knowledge documents.
- Include at least the `flags` and `relatesTo` relationships for the case.
- Include results from `analyze_fraud_signals` and `recommend_investigation_steps`.
- Never recommend automatically freezing the account or denying a transaction.
- Include at least one human approval requirement referencing a fraud analyst or compliance officer.
