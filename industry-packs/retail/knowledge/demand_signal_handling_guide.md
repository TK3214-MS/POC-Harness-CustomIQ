# Demand Signal Handling Guide (Synthetic Reference Document)

> This is a synthetic reference document created for the Industry IQ Platform Accelerator demo. It does not represent a real retailer's guide.

## Signal Types

- `spike`: demand trending sharply upward.
- `decline`: demand trending downward.
- `seasonal`: expected seasonal pattern, generally lower priority for urgent action.

## Review Requirement

Demand signals inform recommendations only. Pricing changes and reorders always require human approval from a merchandising lead or inventory manager (see `industry-packs/retail/manifest.yaml` `human_approval_rules`).
