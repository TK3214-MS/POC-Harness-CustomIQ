// Resource-group-scoped resources for hosting the MCP Backend on Azure
// Container Apps. Deliberately minimal: Log Analytics, Container
// Registry, a user-assigned managed identity with AcrPull, a Container Apps
// Environment, and one Container App. Ingress is internal-only by default -
// flip to external only with explicit approval (see instruction section 24).
@description('Azure region for all resources.')
param location string

@description('Unique token used to derive resource names.')
param resourceToken string

@description('Tags applied to all resources.')
param tags object = {}

@description('Indicates whether azd has already provisioned the MCP Backend Container App.')
param mcpBackendExists bool

@description('Industry Pack served by the MCP Backend.')
param industryPack string

@description('Seed used to generate the in-memory synthetic demo dataset.')
param dataSeed int

var containerRegistryName = 'acrxx${resourceToken}'
var logAnalyticsName = 'log-${resourceToken}'
var containerAppsEnvironmentName = 'cae-${resourceToken}'
var userAssignedIdentityName = 'id-${resourceToken}'
var containerAppName = 'ca-mcp-backend-${resourceToken}'
var containerAppFqdn = '${containerAppName}.${containerAppsEnvironment.properties.defaultDomain}'

// Well-known built-in role: AcrPull
var acrPullRoleDefinitionId = subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '7f951dda-4ed3-4680-a7ca-43fe172d538d')

resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: logAnalyticsName
  location: location
  tags: tags
  properties: {
    sku: { name: 'PerGB2018' }
    retentionInDays: 30
  }
}

resource containerRegistry 'Microsoft.ContainerRegistry/registries@2023-11-01-preview' = {
  name: containerRegistryName
  location: location
  tags: tags
  sku: { name: 'Basic' }
  properties: {
    adminUserEnabled: false
  }
}

resource userAssignedIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: userAssignedIdentityName
  location: location
  tags: tags
}

resource acrPullRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(containerRegistry.id, userAssignedIdentity.id, 'AcrPull')
  scope: containerRegistry
  properties: {
    principalId: userAssignedIdentity.properties.principalId
    principalType: 'ServicePrincipal'
    roleDefinitionId: acrPullRoleDefinitionId
  }
}

resource containerAppsEnvironment 'Microsoft.App/managedEnvironments@2024-03-01' = {
  name: containerAppsEnvironmentName
  location: location
  tags: tags
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalytics.properties.customerId
        sharedKey: logAnalytics.listKeys().primarySharedKey
      }
    }
  }
}

module mcpBackendApp 'br/public:avm/ptn/azd/container-app-upsert:0.4.0' = {
  params: {
    name: containerAppName
    location: location
    containerAppsEnvironmentName: containerAppsEnvironment.name
    containerRegistryName: containerRegistry.name
    containerName: 'mcp-backend'
    containerCpuCoreCount: '0.5'
    containerMemory: '1Gi'
    containerMinReplicas: 1
    containerMaxReplicas: 2
    containerProbes: [
      {
        type: 'Liveness'
        httpGet: {
          path: '/health'
          port: 8000
        }
        initialDelaySeconds: 10
        periodSeconds: 30
        timeoutSeconds: 5
      }
    ]
    env: [
      { name: 'IIQ_INDUSTRY_PACK', value: industryPack }
      { name: 'IIQ_DATA_SCALE', value: 'demo' }
      { name: 'IIQ_DATA_SEED', value: string(dataSeed) }
      { name: 'MCP_BACKEND_ALLOWED_HOSTS', value: containerAppFqdn }
      { name: 'PORT', value: '8000' }
    ]
    exists: mcpBackendExists
    external: false
    identityType: 'UserAssigned'
    identityName: userAssignedIdentity.name
    identityPrincipalId: userAssignedIdentity.properties.principalId
    userAssignedIdentityResourceId: userAssignedIdentity.id
    ingressEnabled: true
    tags: union(tags, { 'azd-service-name': 'mcp-backend' })
    targetPort: 8000
  }
  dependsOn: [
    acrPullRoleAssignment
  ]
}

output containerRegistryLoginServer string = containerRegistry.properties.loginServer
output containerRegistryName string = containerRegistry.name
output mcpBackendName string = mcpBackendApp.outputs.name
output mcpBackendUrl string = mcpBackendApp.outputs.uri
