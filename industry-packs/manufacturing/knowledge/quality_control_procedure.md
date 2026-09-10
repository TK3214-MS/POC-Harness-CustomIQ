# Quality Control Procedure (Synthetic Reference Document)

> This is a synthetic reference document created for the Industry IQ Platform Accelerator demo. It does not represent a real company's procedure and cites no real standards or certifications.

## Purpose

This procedure describes how incoming and in-process quality issues are triaged at a synthetic manufacturing site.

## Incoming Inspection

1. Every batch of parts received from a supplier is sampled for dimensional and surface-finish inspection.
2. A defect rate at or above **5%** on any sampled batch triggers an automatic escalation to Engineering Review.
3. A defect rate below 5% but trending upward over three consecutive batches also triggers escalation.

## Escalation to Engineering Review

When a quality issue is escalated:

1. The issue is logged with a unique `issue_id`, affected `part_id`, and the `factory_id` where it was observed.
2. A quality engineer reviews the issue within 2 business days (synthetic SLA for demo purposes).
3. If root cause is not immediately clear, an Engineering Change (EC) is opened (see `engineering_change_process.md`).

## Human Review Requirement

No quality issue may be closed automatically. A quality engineer must confirm root cause and corrective action before the issue is marked resolved.
