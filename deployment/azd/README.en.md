# deployment/azd/

[![日本語](https://img.shields.io/badge/%E3%81%82-%E6%97%A5%E6%9C%AC%E8%AA%9E-5B6670?style=for-the-badge)](README.md) [![English](https://img.shields.io/badge/A-English-087F8C?style=for-the-badge)](README.en.md)

Azure Developer CLI configuration.

**Status: Configuration implemented; real deployment not verified.** Because `azd` requires the `azure.yaml` file at the repository root, the actual file is located directly under the repository root. See [deployment/bicep/](../bicep/README.en.md) for the infrastructure implementation.

Run these commands after connecting to an approved Azure subscription (to be run by the user):

```bash
azd auth login
azd env new <environment-name>
azd env set AZURE_LOCATION <location>
azd env set IIQ_INDUSTRY_PACK manufacturing
azd env set IIQ_DATA_SEED 42
azd provision --preview
azd up
```

`azd up` sends the source to an ACR remote build and deploys the generated container image to a Container App with internal ingress. Local Docker or Podman is not required. The Bicep implementation uses an AVM upsert pattern with `SERVICE_MCP_BACKEND_RESOURCE_EXISTS` to prevent the latest image from being overwritten during reprovisioning.

Compilation validation with `az bicep build` is complete, but a real deployment with `azd up` has not been verified. See the [Custom MCP Backend lab](../../docs/labs/advanced-mcp.en.md) for the procedure and stopping conditions.
