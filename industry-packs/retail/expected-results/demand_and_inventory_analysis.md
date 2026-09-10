# Expected Results: Retail Demand and Inventory Analysis (Phase 3 draft)

> Qualitative description for human/manual review. Automated evaluation is not yet implemented.

For the prompt "Investigate the most recent demand signal and recommend inventory actions", a correct `AgentResponse` should:

- Name the specific `signal_id`, product, and store in `executive_summary`.
- List the signal type, trend percent, and (if available) on-hand quantity vs. reorder point in `confirmed_facts`.
- Include at least one citation from the Retail knowledge documents.
- Include at least the `relatesTo` and `observedAt` relationships for the signal.
- Include results from `get_inventory_status` and `recommend_inventory_actions`.
- Never recommend automatically placing a reorder or changing pricing.
- Include at least one human approval requirement referencing an inventory manager.
