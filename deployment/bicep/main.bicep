// Subscription-scoped entry point (azd convention). Creates the resource
// group, then deploys resources.bicep into it. Deploys only the MCP Backend
// container hosting. Fabric IQ, Foundry IQ, and Work IQ are configured in
// their SaaS administration surfaces and have no infrastructure here.
targetScope = 'subscription'

@minLength(1)
@maxLength(64)
@description('Name of the azd environment; used to derive resource names.')
param environmentName string

@minLength(1)
@description('Azure region for all resources.')
param location string

@description('Container image for the MCP Backend. Override once a real image is built and pushed to the registry created here.')
param mcpBackendImage string = 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'

var resourceToken = toLower(uniqueString(subscription().id, environmentName, location))
var tags = {
  'azd-env-name': environmentName
}

resource rg 'Microsoft.Resources/resourceGroups@2024-03-01' = {
  name: 'rg-${environmentName}'
  location: location
  tags: tags
}

module resources 'resources.bicep' = {
  name: 'resources'
  scope: rg
  params: {
    location: location
    resourceToken: resourceToken
    tags: tags
    mcpBackendImage: mcpBackendImage
  }
}

output AZURE_RESOURCE_GROUP string = rg.name
output AZURE_CONTAINER_REGISTRY_ENDPOINT string = resources.outputs.containerRegistryLoginServer
output AZURE_CONTAINER_REGISTRY_NAME string = resources.outputs.containerRegistryName
output MCP_BACKEND_URL string = resources.outputs.mcpBackendUrl
