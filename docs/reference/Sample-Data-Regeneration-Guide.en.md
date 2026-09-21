# Sample Data Regeneration Guide

This page is a reference for developers who need to modify or regenerate the synthetic data stored in the repository. For standard labs, do not run the generation commands; use the existing files in `industry-packs/<pack>/sample-data/`.

## Environment Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Small Demo Data

```bash
python scripts/generate_demo_iq_data.py
pytest tests/contract/test_demo_iq_data.py -q
python scripts/validation/validate_synthetic_data.py
```

Output locations:

- Fabric: `industry-packs/<pack>/sample-data/fabric/*.csv`
- Foundry supplemental corpus: `industry-packs/<pack>/sample-data/foundry/demo/knowledge.jsonl`

Work IQ templates and Foundry Markdown knowledge are managed in `sample-data/work-iq/` and `knowledge/`, respectively.

## Enterprise Data

```bash
python scripts/generate_enterprise_sample_data.py
python scripts/generate_enterprise_prompts.py
pytest tests/contract -q
python scripts/validation/validate_synthetic_data.py
```

Output locations:

- Fabric: `industry-packs/<pack>/sample-data/fabric/enterprise/*.csv`
- Foundry: `industry-packs/<pack>/sample-data/foundry/enterprise/records.jsonl`
- Questions: `industry-packs/<pack>/sample-data/prompts/enterprise_prompts.yaml`

## Principles for Changes

1. For changes that will be retained, do not edit only the generated CSV or JSONL files directly; update the generator or the source Knowledge documents.
2. Preserve the synthetic ID system and relationship references across all industries.
3. Run the contract tests and synthetic data validation after generation.
4. Do not add information about real individuals, organizations, patients, customers, accounts, or residents.

For deployment targets and expected counts, see the [IQ Demo Data Deployment and Reconstruction Runbook](../evaluation/Demo-Data-Deployment-Runbook.md).
