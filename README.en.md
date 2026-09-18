# Industry IQ Platform Accelerator

[![日本語](https://img.shields.io/badge/%E3%81%82-%E6%97%A5%E6%9C%AC%E8%AA%9E-5B6670?style=for-the-badge)](README.md) [![English](https://img.shields.io/badge/A-English-087F8C?style=for-the-badge)](README.en.md)

An Industry Pack-enabled Enterprise Intelligence Platform accelerator that uses Fabric IQ, Foundry IQ, and Work IQ through the GitHub Copilot harness in Microsoft Copilot Studio.

## Start Here

To explore the configuration hands-on, start with the [Industry IQ Platform Labs](docs/index.en.md). Developers and architects reviewing the production architecture should use the [Production Environment Setup Guide](docs/Production-Environment-Setup.en.md).

The guide configures the environment in this order:

1. Confirm prerequisites and permissions for Azure, Fabric, Copilot Studio, and Work IQ.
2. Configure a Lakehouse, managed tables, Ontology, entity types, relationships, and data bindings in Fabric.
3. Configure Knowledge Sources, indexers, a Knowledge Base, and search settings in Foundry and Azure AI Search.
4. Enable the Work IQ tenant and prepare billing, policies, and Microsoft 365 validation data.
5. Connect Fabric IQ MCP, Foundry IQ, and Work IQ (preview) in Copilot Studio.
6. Connect this repository's MCP Backend as a business tool only when needed.

## Repository Responsibilities

This repository provides Industry Packs, MCP Tool contracts, an MCP Backend, Azure deployment definitions, and tests. The SaaS administration interfaces and Copilot Studio are responsible for configuring Fabric IQ, Foundry IQ, and Work IQ and retrieving IQ data.

## Developer Validation

After changing the MCP Backend or an Industry Pack:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
ruff check .
pytest tests/
```

For the MCP Backend Azure deployment definitions, see the [Production Environment Setup Guide](docs/Production-Environment-Setup.en.md) and [Bicep README](deployment/bicep/README.en.md).

## Design and Validation Records

- [Labs portal](docs/index.en.md)
- [Production environment setup guide](docs/Production-Environment-Setup.en.md)
- [Ontology design and implementation guide for real customer data](docs/Customer-Data-Ontology-Design-Guide.en.md)
- [IQ demo data deployment and reconfiguration runbook](docs/evaluation/Demo-Data-Deployment-Runbook.en.md)
- [Copilot Studio IQ-layer test execution and evaluation guide](docs/evaluation/Copilot-Studio-IQ-Layer-Test-Catalog.en.md)
- [Troubleshooting](docs/troubleshooting/README.en.md)
- [MCP Backend documentation](docs/mcp/README.en.md)
- [Security policy](SECURITY.en.md)

## Preview the Labs Site Locally

```bash
source .venv/bin/activate
mkdocs serve
```

## License

[MIT License](LICENSE)
