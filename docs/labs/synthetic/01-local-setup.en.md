# Lab 1: Review Sample Data

Estimated time: 15 minutes

## 1. Review the Stored Data

Review the following directories in the selected Industry Pack. This lab uses the stored files as-is and does not regenerate them.

```text
industry-packs/<pack>/sample-data/fabric/
industry-packs/<pack>/sample-data/foundry/demo/
industry-packs/<pack>/sample-data/work-iq/
industry-packs/<pack>/knowledge/
```

Developers who need to regenerate the data should see the [sample data regeneration guide](../../reference/Sample-Data-Regeneration-Guide.md).

## 2. Automated Validation (Optional)

Complete this step only if you generated or modified the sample data yourself. If you are using the files stored in the repository as-is, continue to "Review the Mappings."

```bash
pytest tests/contract/test_demo_iq_data.py -q
python scripts/validation/validate_synthetic_data.py
```

## 3. Review the Mappings

Open [`industry-packs/<pack>/ontology/entities.yaml`](https://github.com/TK3214-MS/POC-Harness-CustomIQ/tree/main/industry-packs){ target="_blank" rel="noopener" }, then review each entity's `dataset_key` and `identifier_field`. Confirm that the corresponding CSV has a table and key column with the same names.

!!! tip "Keep IDs Consistent"
    This lab uses the small synthetic dataset's `*-SYN-*` IDs. Do not mix them with sequential IDs from `enterprise/`.

## Acceptance Criteria

- [ ] You reviewed the Fabric, Foundry, and Work IQ sources for the selected pack.
- [ ] If you generated or modified the data yourself, the contract test and synthetic data validation passed.

[Back: Lab overview](index.md){ .md-button }
[Next: Fabric IQ](02-fabric-iq.md){ .md-button .md-button--primary }
