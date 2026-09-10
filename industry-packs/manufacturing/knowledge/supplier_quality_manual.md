# Supplier Quality Manual (Synthetic Reference Document)

> This is a synthetic reference document created for the Industry IQ Platform Accelerator demo. It does not represent a real company's manual and cites no real standards or certifications.

## Supplier Reliability Scoring

Each synthetic supplier is assigned a `reliability_score` between 0.70 and 0.99, based on historical on-time delivery and defect rate (synthetic, randomly generated for demo purposes).

## Supplier Audit Triggers

A supplier audit should be considered when any of the following are true:

- `reliability_score` falls below 0.80.
- More than one open quality issue is associated with parts from the same supplier.
- A quality issue with `severity` of `high` or `critical` is traced back to a part from that supplier.

## Audit Outcomes

Audit outcomes are not automated by this accelerator. A supplier quality engineer must conduct the audit and document findings before any corrective action (such as a supplier probation status) is applied.
