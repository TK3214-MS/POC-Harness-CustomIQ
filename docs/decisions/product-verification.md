# Microsoft Product Verification Tracker

Status: **None of the items below have been verified against current Microsoft documentation as of 2026-09-08.** Every row is `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION` until someone with access to current docs/tenant confirms it. This file is the single source of truth feeding `config/capabilities.yaml`; do not duplicate these facts elsewhere as if independently confirmed.

Do not treat anything in this file as fact. It exists so that every place in the codebase that depends on a Microsoft product detail points here instead of re-guessing.

| Capability | What needs verification | Current status in repo | Verification method (when available) |
|---|---|---|---|
| Microsoft Copilot Studio — "GitHub Copilot harness" | Exact product name, GA/Preview status, licensing model, availability of "harness" concept as described in instructions | TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION | Copilot Studio official docs + release notes |
| Work IQ | Product existence/name, GA/Preview status, supported connectors (Teams/Outlook/SharePoint/OneDrive), licensing, regional availability | TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION | Microsoft 365 Copilot / Work IQ docs |
| Foundry IQ | Product existence/name, relationship to Azure AI Search / Azure AI Foundry Knowledge, GA/Preview status, confidence score semantics | TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION | Azure AI Foundry docs |
| Fabric IQ | Product existence/name, relationship to Microsoft Fabric Data Agents / OneLake, GA/Preview status, Ontology feature maturity | TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION | Microsoft Fabric docs |
| MCP support in Copilot Studio / Foundry | Native MCP tool registration support, allowlisting mechanism, auth model | TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION | Copilot Studio / Foundry MCP docs |
| Microsoft Entra ID | Current recommended patterns for delegated vs. app-only auth for agent tool calls, On-Behalf-Of flow support for MCP tools | TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION | Microsoft Entra ID docs |
| Microsoft Purview | Current sensitivity label / DLP integration points applicable to agent-retrieved content | TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION | Microsoft Purview docs |
| Licensing/pricing for all of the above | Any $ or license-tier figures | TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION | Official pricing pages at time of verification |
| Regional availability for all of the above | Region lists | TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION | Product region availability pages |
| Preview vs. GA status for all of the above | Feature maturity | TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION | Release notes / product docs |

## Process

1. Every `capability_id` in `config/capabilities.yaml` must have a matching row here.
2. `last_verified_date` in the registry may only be set to a real date once a named person has checked a named, dated Microsoft source — never inferred from training data or general familiarity.
3. Until verified, `status` in the registry stays `Unknown` or `Verify Before Use`, and any customer-facing text referencing the capability must include the literal string `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`.
4. When a verification is performed, update this table with: verifier name, date, source URL/doc title, and the resulting status — then update the registry in the same change.
