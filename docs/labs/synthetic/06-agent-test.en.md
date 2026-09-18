# Lab 6: Test the Copilot Studio Agent

Estimated time: 30-45 minutes

On this page, do not modify the agent developed in Lab 5; perform only testing and result recording. If you need to add questions or correct tool settings, save the test results before returning to [Copilot Studio configuration](05-copilot-studio.md).

## 1. Fix the Test Conditions

| Item | Recorded Value |
| --- | --- |
| Industry Pack | `<pack>` |
| Agent / environment | |
| Connection user | |
| Fabric workspace / Ontology | |
| Foundry Knowledge Base | |
| Work IQ test user | |
| Execution date/time / timezone | |
| Dataset | `small` |

Do not change the browser, user, destinations, or data version during testing. Record the first run separately as a warm-up.

## 2. Run the Required Tests

Open the [IQ layer test execution and evaluation guide](../../evaluation/Copilot-Studio-IQ-Layer-Test-Catalog.md) in a new tab. Expand the panel for the selected industry and run the tests in this order.

1. Use `F-01` and `F-02` to confirm the Fabric IQ schema and known ID.
2. Use `K-01` to confirm the Foundry IQ document name and citation.
3. Use `W-01` to confirm Work IQ user permissions and cross-M365 retrieval.
4. After every single-layer test passes, run `X-01` and `X-02`.

After each question, open the Activity trace and record the expected tool, actual tool, input, result, error, and Correlation ID.

## 3. Record the Results

| Test ID | Actual Tool | Evidence / Citation | Response Time | Result | Remaining Issue |
| --- | --- | --- | ---: | --- | --- |
| `<pack>-F-01` | | | | Pass / Partial / Fail | |
| `<pack>-F-02` | | | | Pass / Partial / Fail | |
| `<pack>-K-01` | | | | Pass / Partial / Fail | |
| `<pack>-W-01` | | | | Pass / Partial / Fail | |
| `<pack>-X-01` | | | | Pass / Partial / Fail | |
| `<pack>-X-02` | | | | Pass / Partial / Fail | |

The expected answer examples are not exact-match answer keys. Use them as baselines for comparing values, citations, source separation, and safety.

## Acceptance Criteria

- [ ] Every required single-layer test is `Pass`.
- [ ] Cross-layer answers separate evidence from Fabric, Foundry, and Work IQ.
- [ ] Zero results, insufficient permissions, and tool failures are not treated as success.
- [ ] High-impact decisions are not executed automatically, and required human approvals are identified.
- [ ] Differences from the expected answer examples are recorded as remaining issues.

[Back: Configure Copilot Studio](05-copilot-studio.md){ .md-button }
[Next: Completion check](06-complete.md){ .md-button .md-button--primary }
