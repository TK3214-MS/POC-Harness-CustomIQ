# Fraud Investigation Procedure (Synthetic Reference Document)

> This is a synthetic reference document created for the Industry IQ Platform Accelerator demo. It does not represent a real institution's procedure and cites no real regulations.

## Purpose

Describes how a synthetic fraud case is triaged once a transaction is flagged.

## Triage Steps

1. A flagged transaction generates a `FraudCase` with a `risk_score` between 0 and 1.
2. A `risk_score` at or above **0.7** requires contacting the customer to verify the transaction before any further action.
3. A `FraudCase` may never be closed as `confirmed_fraud` or `closed_no_fraud` without a fraud analyst's review.

## Human Review Requirement

No fraud case may be closed automatically. No account may be frozen automatically. No transaction may be denied or reversed automatically. A fraud analyst must review the case and a compliance officer must approve closure.
