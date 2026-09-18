# deployment/bicep/

[![日本語](https://img.shields.io/badge/%E3%81%82-%E6%97%A5%E6%9C%AC%E8%AA%9E-5B6670?style=for-the-badge)](README.md) [![English](https://img.shields.io/badge/A-English-087F8C?style=for-the-badge)](README.en.md)

Bicep templates for the MCP Backend deployment.

`main.bicep` operates at subscription scope and creates the resource group. `resources.bicep` defines Log Analytics, Container Registry, a user-assigned managed identity, a Container Apps environment, and the Container App for the MCP Backend. The Container App uses AVM `container-app-upsert:0.4.0` and configures internal ingress, managed-identity pulls from ACR, a `/health` liveness probe, and Industry Pack environment variables.

The templates have been compiled with `az bicep build --file deployment/bicep/main.bicep --stdout`. Because `SERVICE_MCP_BACKEND_RESOURCE_EXISTS`, which is set by `azd`, is required, use `azd up` from the repository root instead of running `az deployment` independently. Deployment to actual Azure resources has not been validated.
