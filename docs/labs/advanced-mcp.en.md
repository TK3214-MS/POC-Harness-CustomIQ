# Optional Lab: Custom MCP Backend

This lab is optional. Complete it only when connecting a tool for a customer-specific Business System, which Fabric IQ, Foundry IQ, and Work IQ do not provide, to Copilot Studio.

The implementation deployed by this procedure is a validation Backend that generates the selected Industry Pack's **synthetic dataset** in memory. It does not implement a customer Business System connection or authentication of incoming requests.

## Entry Criteria

- You completed the synthetic sample data lab.
- You obtained approval to create Azure resources and incur costs.
- Owners have been assigned for HTTPS endpoint, authentication, secret management, and network boundary design.
- You understand that incoming-request authentication is not implemented in the current MCP Backend.

!!! danger "Do Not Publish"
    Do not expose the MCP Backend through public ingress without configuring authentication and network boundaries.

## 1. Validate the Local Contracts

Run the following commands from the repository root.

```bash
source .venv/bin/activate
pytest tests/contract/test_mcp_tool_contract.py -q
pytest tests/integration/test_mcp_protocol_server.py -q
python scripts/demo/test_mcp_protocol_connectivity.py
```

The last script uses the official MCP client SDK over a local socket to validate `initialize`, `tools/list`, and `tools/call`.

## 2. Configure the azd Environment

The person with Azure resource creation permission and cost approval should perform this step. Replace `<environment-name>` and `<location>` with approved values.

```bash
azd auth login
azd env new <environment-name>
azd env set AZURE_LOCATION <location>
azd env set IIQ_INDUSTRY_PACK manufacturing
azd env set IIQ_DATA_SEED 42
azd provision --preview
```

Set `IIQ_INDUSTRY_PACK` to one of `manufacturing`, `financial-services`, `retail`, `healthcare`, or `public-sector`. Review the `azd provision --preview` diff and confirm that it includes only Log Analytics, ACR, a managed identity, a Container Apps environment, and a Container App with internal ingress.

## 3. Deploy to Azure

Run the following command after the approver reviews the preview.

```bash
azd up
```

`azd up` provisions the Bicep, sends the Dockerfile and repository-root build context to an ACR remote build, and deploys the generated image to the Container App tagged `azd-service-name: mcp-backend`. Local Docker/Podman is not required. The Bicep uses the official AVM upsert pattern so rerunning `azd provision` does not restore the latest deployed image to the placeholder.

!!! note "Replicas and Cost"
        Due to constraints of the AVM upsert module, this configuration sets the minimum replicas to `1` and the maximum to `2`. Prices are not stated here. Confirm current pricing and your budget as of the date of the lab.

<figure class="lab-image-placeholder" markdown>
    **Image replacement location: Container App overview**
    `assets/images/labs/mcp-container-app-overview.png`
    <figcaption>Replace with a screen showing internal ingress, the latest revision, image, and status.</figcaption>
</figure>

## 4. Validate the Internal Endpoint

Load the output into the shell.

```bash
eval "$(azd env get-values)"
az containerapp show \
    --resource-group "$AZURE_RESOURCE_GROUP" \
    --name "$MCP_BACKEND_NAME" \
    --query "{fqdn:properties.configuration.ingress.fqdn,external:properties.configuration.ingress.external,latestReady:properties.latestReadyRevisionName,image:properties.template.containers[0].image}" \
    --output table
```

Confirm that `external` is `false` and that `latestReady` and the ACR image are displayed. Next, call the health endpoint from inside the running container. The image does not include `curl`, so use the Python standard library.

```bash
az containerapp exec \
    --resource-group "$AZURE_RESOURCE_GROUP" \
    --name "$MCP_BACKEND_NAME" \
    --command "python -c \"import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8000/health').read().decode())\""
```

Also review the startup logs.

```bash
az containerapp logs show \
    --resource-group "$AZURE_RESOURCE_GROUP" \
    --name "$MCP_BACKEND_NAME" \
    --type console \
    --tail 100
```

## 5. Stop Conditions for the Copilot Studio Connection

Internal ingress cannot be reached directly by Copilot Studio over the internet. Because the Backend also lacks incoming-request authentication, this lab does not switch it to public ingress. Treat registration under **Tools > Add Tool > Model Context Protocol** as incomplete until a separate design satisfies all of the following:

- An approved network path reachable by Copilot Studio
- Incoming authentication supported by Copilot Studio
- Secret management, rate limiting, audit logging, and host/origin allowlists
- Threat model, Security approval, and negative tests

## Completion Criteria

- [ ] The local contract, integration, and official MCP client connectivity tests passed.
- [ ] The approver reviewed `azd provision --preview`.
- [ ] `azd up`, including the ACR remote build, succeeded, and the latest ready revision contains the generated image.
- [ ] Ingress `external` is `false`.
- [ ] `/health` succeeded from inside the container.
- [ ] You did not incorrectly document the Copilot Studio connection as having implemented authentication.

See the [MCP Backend documentation](../mcp/README.md) for the implementation and contracts, the [MCP security guide](../mcp/MCP-Security-Guide.md) for pre-publication requirements, and the [production environment setup guide](../Production-Environment-Setup.md) for its place in the production architecture.
