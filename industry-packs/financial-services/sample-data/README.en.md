# Financial Services Sample Data

[![日本語](https://img.shields.io/badge/%E3%81%82-%E6%97%A5%E6%9C%AC%E8%AA%9E-5B6670?style=for-the-badge)](README.md) [![English](https://img.shields.io/badge/A-English-087F8C?style=for-the-badge)](README.en.md)

All data is synthetic. Directly under `fabric/` are small CSV files corresponding to all four Ontology entity types, allowing relationships to be verified using the same `*-SYN-*` IDs. `fabric/enterprise/` contains large CSV files that can be reproduced from the generator.

`work-iq/` contains four items that refer to the same fraud case: a SharePoint document, a Teams conversation, an Outlook email, and meeting notes. Register them in dedicated test accounts, and do not mix them with real customer or account information.

The eight documents in `knowledge/` are managed documents for Foundry IQ. `foundry/demo/knowledge.jsonl` is a supplemental corpus that bundles the eight documents, and `foundry/enterprise/records.jsonl` is for validating searches over structured business records; neither replaces the managed Markdown documents. `prompts/enterprise_prompts.yaml` contains 50 evaluation questions across five scenarios.

For regeneration and ingestion, see the [IQ demo data deployment and reconstruction runbook](../../../docs/evaluation/Demo-Data-Deployment-Runbook.md).
