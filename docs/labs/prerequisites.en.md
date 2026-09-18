# Prerequisites

[![日本語](https://img.shields.io/badge/%E3%81%82-%E6%97%A5%E6%9C%AC%E8%AA%9E-5B6670?style=for-the-badge)](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/docs/labs/prerequisites.md) [![English](https://img.shields.io/badge/A-English-087F8C?style=for-the-badge)](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/docs/labs/prerequisites.en.md)

Estimated time: 20-30 minutes

If you cannot confirm every item on this page, do not proceed with the SaaS setup. Availability requirements, licenses, regions, and Preview statuses can change, so defer to current official Microsoft documentation and the tenant administrator's decision as of the date you perform the lab.

## 1. Microsoft Environment (Required)

Confirm the following with your tenant administrator. This lab does not prescribe specific licenses, prices, regions, or GA/Preview statuses.

- [ ] You have a capacity and workspace that can use Microsoft Fabric.
- [ ] Fabric Ontology and the required related features are available in the tenant.
- [ ] You can create managed tables in a Lakehouse.
- [ ] You can use Azure AI Search and the Foundry IQ features required by the lab.
- [ ] You can create an agent in Copilot Studio and add the Fabric IQ, Foundry IQ, and Work IQ tools.
- [ ] If you use Work IQ, tenant settings, billing policies, and user policies are configured.
- [ ] You can place synthetic lab content in SharePoint, Teams, and Exchange.

Use the [lab cost estimation guide](../reference/Cost-Estimation-Guide.md) to confirm a budget limit based on the solutions you will use and their expected monthly usage.

## 2. Local Environment (Only If You Generate Samples Yourself)

You do not need this section if you use the synthetic data already stored in the repository. Complete it only if you are a developer changing the generation source or if you regenerate the sample data yourself.

Run the following commands from the repository root.

```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest tests/contract/test_demo_iq_data.py -q
python scripts/validation/validate_synthetic_data.py
```

### Acceptance Criteria

- You are using Python 3.11 or later.
- The demo data contract tests pass.
- Synthetic data validation passes.

For regeneration details, see the [sample data regeneration guide](../reference/Sample-Data-Regeneration-Guide.md).

## 3. Permissions (Required)

| Target | Required Tasks | Owner to Confirm |
| --- | --- | --- |
| Fabric workspace | Review Lakehouse, Ontology, binding, and Graph | Fabric administrator |
| Azure AI Search / Foundry | Configure Knowledge Source, index, and Knowledge Base | Azure administrator |
| Microsoft 365 | Prepare synthetic documents, Teams posts, emails, and meetings | M365 administrator |
| Copilot Studio | Create agent, connect tools, and review Activity trace | Power Platform administrator |

!!! danger "If Anything Is Missing"
    Do not work around missing items based on assumptions. Give the administrator the workspace name, required operation, target user, and usage period for confirmation. Do not begin the setup in [Choose an industry](choose-industry.md) or later until all conditions are met.

**Completion criteria**: You have confirmed every Microsoft environment and permission checklist item. If you generate the data yourself, local validation has also passed.

[Back: Lab guide](index.md){ .md-button }
[Next: Choose an industry](choose-industry.md){ .md-button .md-button--primary }
