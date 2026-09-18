# Troubleshooting

[![日本語](https://img.shields.io/badge/%E3%81%82-%E6%97%A5%E6%9C%AC%E8%AA%9E-5B6670?style=for-the-badge)](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/docs/troubleshooting/README.md) [![English](https://img.shields.io/badge/A-English-087F8C?style=for-the-badge)](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/docs/troubleshooting/README.en.md)

## Build Order

If you skip steps in the build order, answers may be empty even when Copilot Studio can connect. First complete the SaaS-side configuration in the [Production Environment Setup Guide](../Production-Environment-Setup.md), and then connect the Copilot Studio Tool.

## Fabric IQ

- Cannot create an Ontology item: Check the tenant setting **Enable Ontology item (preview)**, capacity, and workspace permissions.
- Instances are empty: Check the Lakehouse managed table, entity type key, property binding, and Graph model refresh.
- The Tool does not work from Copilot Studio: Check the workspace ID, Ontology ID, the user's Fabric permissions, and connection consent.

### `Failed to translate NL query to ontology query`

This error occurs after the Fabric IQ Tool is called, during the step that translates natural language into an Ontology query. Isolate the cause in the following order.

1. In the Fabric IQ Tool details in Copilot Studio, confirm that `list_ontology_entity_types` and `search_ontology` are displayed.
2. In the Test pane, ask, "Using only Fabric IQ, list the available entity types and properties." If listing fails, check the connected workspace/Ontology ID, the connected user's permissions, and whether the Ontology is published and available.
3. On the Fabric Ontology screen, open **Instances** for the target entity type and confirm that actual data is displayed. If it is not displayed, check the managed Lakehouse table, entity type key, property binding, column names, and data access.
4. Manually refresh the Graph model and confirm that additional rows in upstream tables are reflected.
5. Give entity type names, property names, and relationship names business-readable names and descriptions. Do not duplicate relationship names anywhere in the Ontology.
6. Avoid ambiguous questions, and initially specify the entity type and properties. For the Manufacturing Pack, ask, "From `QualityIssue` in Fabric IQ, show 5 records with `issue_id`, `summary`, `severity`, `status`, and `detected_at`."
7. After a single-entity search succeeds, add relationships one at a time, as in "From `QualityIssue`, retrieve the related `Part` through `affects`."
8. For a term such as "incident" that can have multiple meanings, specify whether it means a quality issue, equipment outage, system outage, or supply disruption. The current Manufacturing Ontology structures `QualityIssue`; it has no dedicated entity type for equipment or system outages.
9. In Activity trace, confirm that the failed Tool is Fabric IQ's `search_ontology`. The fact that Foundry IQ or Work IQ was not called for the same question does not indicate a failure in either connection.
10. If the issue is reproducible, save the Activity trace, question text, workspace/Ontology ID, Correlation ID, Timestamp, and whether the schema list succeeded, and provide them to Microsoft support. Do not save or share access tokens or connection secrets.

Official information:

- [Fabric IQ Ontology MCP](https://learn.microsoft.com/en-us/microsoft-copilot-studio/mcp-fabric-iq-ontology)
- [Ontology troubleshooting](https://learn.microsoft.com/en-us/fabric/iq/ontology/resources-troubleshooting)
- [Entity type creation](https://learn.microsoft.com/en-us/fabric/iq/ontology/how-to-create-entity-types)
- [Ontology data binding](https://learn.microsoft.com/en-us/fabric/iq/ontology/how-to-bind-data)

## Foundry IQ

- Knowledge Base is empty: Check the Knowledge Source ingestion status, Indexer, Index, and Storage Blob Data Reader.
- Answers have no citations: Check the Knowledge Base's Knowledge Source, retrieval instructions, answer settings, and model permissions.
- Cannot select it in Copilot Studio: Confirm that the Knowledge Base has been created in Foundry/Azure AI Search and that the target user has access.

## Work IQ

- Work IQ (preview) does not appear under Tools: Check the GitHub Copilot harness, Preview availability, Work IQ tenant enablement, Copilot Credits billing, and spending policy.
- No data is returned: Confirm that the test user can access the target data in Exchange, Teams, SharePoint, and OneDrive through normal M365 permissions.
- Writes fail: Work IQ is read-only by default. Check the Work IQ MCP policy and spending policy in the Microsoft 365 admin center.

## MCP Backend

- `tools/list` fails: Check the HTTPS endpoint, `/mcp` path, ingress, authentication, and `MCP_BACKEND_ALLOWED_HOSTS`.
- Tools are not displayed: Check `MCP_BACKEND_ALLOWED_TOOLS`, the Industry Pack manifest, and MCP Backend logs.
- Tool execution fails: Check Activity trace, the MCP Backend correlation ID, the Tool input schema, and errors from the business Tool.

This repository does not directly diagnose failures in SaaS-side admin consoles or within customer Business Systems. Check the administrator logs and Activity trace for each service.
