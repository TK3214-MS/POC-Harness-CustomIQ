// Resource-group-scoped resources for hosting the MCP Backend on Azure
// Container Apps. Deliberately minimal (Phase 5): Log Analytics, Container
// Registry, a user-assigned managed identity with AcrPull, a Container Apps
// Environment, and one Container App. Ingress is internal-only by default -
// flip to external only with explicit approval (see instruction section 24).
@description('Azure region for all resources.')
param location string

@description('Unique token used to derive resource names.')
param resourceToken string

@description('Tags applied to all resources.')
param tags object = {}

@description('Container image for the MCP Backend.')
param mcpBackendImage string

var containerRegistryName = 'acrxx${resourceToken}'
var logAnalyticsName = 'log-${resourceToken}'
var containerAppsEnvironmentName = 'cae-${resourceToken}'
var userAssignedIdentityName = 'id-${resourceToken}'
var containerAppName = 'ca-mcp-backend-${resourceToken}'

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

resource mcpBackendApp 'Microsoft.App/containerApps@2024-03-01' = {
  name: containerAppName
  location: location
  tags: union(tags, { 'azd-service-name': 'mcp-backend' })
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${userAssignedIdentity.id}': {}
    }
  }
  properties: {
    environmentId: containerAppsEnvironment.id
    configuration: {
      // Internal-only by default - this is a demo/sample-data service, not a
      // production API. Flip to external=true only with explicit approval.
      ingress: {
        external: false
        targetPort: 8000
        transport: 'http'
      }
      registries: [
        {
          server: containerRegistry.properties.loginServer
          identity: userAssignedIdentity.id
        }
      ]
    }
    template: {
      containers: [
        {
          name: 'mcp-backend'
          image: mcpBackendImage
          resources: {
            cpu: json('0.5')
            memory: '1Gi'
          }
          env: [
            { name: 'IIQ_INDUSTRY_PACK', value: 'manufacturing' }
            { name: 'IIQ_DATA_SCALE', value: 'demo' }
          ]
        }
      ]
      scale: {
        minReplicas: 0
        maxReplicas: 2
      }
    }
  }
  dependsOn: [
    acrPullRoleAssignment
  ]
}

output containerRegistryLoginServer string = containerRegistry.properties.loginServer
output containerRegistryName string = containerRegistry.name
output mcpBackendUrl string = 'https://${mcpBackendApp.properties.configuration.ingress.fqdn}'
