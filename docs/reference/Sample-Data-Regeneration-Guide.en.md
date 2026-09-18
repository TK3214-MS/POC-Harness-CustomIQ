# Sample Data Regeneration Guide

[![日本語](https://img.shields.io/badge/%E3%81%82-%E6%97%A5%E6%9C%AC%E8%AA%9E-5B6670?style=for-the-badge)](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/docs/reference/Sample-Data-Regeneration-Guide.md) [![English](https://img.shields.io/badge/A-English-087F8C?style=for-the-badge)](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/docs/reference/Sample-Data-Regeneration-Guide.en.md)

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
