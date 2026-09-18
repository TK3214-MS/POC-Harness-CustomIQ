# Lab 3: Foundry IQ

Estimated time: 60-90 minutes

Register the selected Industry Pack's procedure and policy documents so answers include document names and citations.

## 1. Confirm Availability Requirements and Region

This lab creates Azure Blob Storage, Azure AI Search, a Microsoft Foundry project, and embedding/chat models. Because this may incur charges, designate the person authorized to create resources and the person responsible for deleting them before you begin.

1. Use [Azure AI Search region support](https://learn.microsoft.com/en-us/azure/search/search-region-support){ target="_blank" rel="noopener" } to identify a region where Agentic Retrieval is available.
2. Use [Foundry region support](https://learn.microsoft.com/en-us/azure/foundry/reference/region-support){ target="_blank" rel="noopener" } and the model catalog to confirm that an available embedding/chat model and quota exist in the same region.
3. Confirm with the administrator that Storage, Search, and Foundry will be created in the same subscription, resource group, and region.
4. For the Search tier, choose Basic or higher, which can use a system-assigned managed identity, and select an option that meets Agentic Retrieval requirements and the budget. Reconfirm specific prices and tier availability when creating the service.

!!! danger "Stop If You Cannot Confirm"
    Do not guess model, quota, region, tier, license, or GA/Preview status. Record any value you cannot confirm as `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`, and resume only after administrator confirmation. The Agentic Retrieval UI in the Microsoft Foundry portal and Azure portal may be labeled Preview.

## 2. Create a Working Record

The names below are examples. Use your initials or a similar value for `<suffix>`, and confirm globally unique names on each Azure creation screen.

| Item | Example Record | Actual Value |
| --- | --- | --- |
| Subscription ID | `00000000-0000-0000-0000-000000000000` | |
| Resource group | `rg-iiq-lab-<suffix>` | |
| Region | `<region confirmed for all features>` | |
| Storage account | `stiiqlab<suffix>` | |
| Blob container | `<pack>-knowledge` | |
| Search service | `srch-iiq-lab-<suffix>` | |
| Search endpoint | `https://srch-iiq-lab-<suffix>.search.windows.net` | |
| Foundry resource | `ai-iiq-lab-<suffix>` | |
| Foundry project | `iiq-<pack>-project` | |
| Project endpoint | `<endpoint displayed on project Home>` | |
| Embedding deployment | `<validated deployment name>` | |
| Chat deployment | `<validated deployment name>` | |
| Knowledge Source | `ks-<pack>-policy` | |
| Knowledge Base | `kb-<pack>-operations` | |
| Setup user | `lab.user@contoso.example` | |
| Search identity object ID | `<GUID displayed on the Search Identity screen>` | |

## 3. Create Azure Resources

### 3.1 Resource Group and Storage

1. In the [Azure portal](https://portal.azure.com/){ target="_blank" rel="noopener" }, select **Resource groups > Create** and use the subscription, resource group, and region from your record.
2. Select **Storage accounts > Create** and specify the same resource group and region.
3. Select the equivalent of general-purpose v2 for Account kind, **Standard** for Performance, and a Redundancy option that meets the lab requirements and organizational policy. Confirm pricing when creating the account.
4. Under **Security**, require secure transfer, set minimum TLS to 1.2 or later, and disable anonymous access. Decide whether Shared Key can be disabled based on the portal/API path you use and organizational policy; do not change it without confirmation.
5. Select **Review + create > Create**.
6. After creation, select **Data storage > Containers > + Container** and create the recorded container as **Private (no anonymous access)**.

### 3.2 Azure AI Search

1. In the Azure portal, select **Azure AI Search > Create**, then specify the same resource group and confirmed region.
2. Enter a unique Search service name, select the confirmed tier, and create the service.
3. Under **Settings > Identity > System assigned**, set the identity to **On**, save, and record the object ID.
4. Under **Settings > Keys**, set API access control to **Both** while assigning roles. After role-based connectivity is confirmed, switch to **Role-based access control** according to organizational policy.

### 3.3 Foundry Resource, Project, and Models

1. Sign in to [Microsoft Foundry](https://ai.azure.com/){ target="_blank" rel="noopener" } and confirm that **New Foundry** is enabled.
2. From the project name at the upper left, select **Create new project** and open **Advanced options**.
3. Enter the resource group, Foundry resource name, project name, and confirmed region from your record, then create the project. The portal also creates the Foundry resource.
4. Record the project endpoint shown on project Home.
5. Under **Discover > Models**, select an embedding model currently supported by the Blob Knowledge Source, then use **Deploy > Custom settings** to review the deployment name and quota and create it.
6. Similarly, deploy a chat model supported for Knowledge Base answer synthesis.
7. Under **Build > Models**, confirm that both deployments have status **Succeeded**, and record each **deployment name**, not its model name.

Because specific model names, versions, deployment types, and capacities vary by subscription and region, this lab does not prescribe them. Defer to the [official model deployment procedure](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/how-to/deploy-foundry-models){ target="_blank" rel="noopener" } and the available options shown when you create the deployments.

## 4. Configure Identity and RBAC

Role assignments require Owner, User Access Administrator, Role Based Access Control Administrator, or another permission that includes `Microsoft.Authorization/roleAssignments/write`. Propagation may take time.

| Scope | Principal | Role | Purpose |
| --- | --- | --- | --- |
| Search service | Setup user | **Search Service Contributor** | Manage Search objects such as Knowledge Sources and Bases |
| Search service | Setup user | **Search Index Data Contributor** | Read and write index content and retrieve from the Knowledge Base |
| Storage account | Setup user | **Storage Blob Data Contributor** | Upload eight documents from the portal |
| Storage account | Search system-assigned identity | **Storage Blob Data Reader** | Read the Blob Knowledge Source |
| Foundry resource | Search system-assigned identity | **Cognitive Services User** | Use embedding/chat deployments |
| Foundry resource | Model creator | **Cognitive Services Contributor** or equivalent permission | Create and manage model deployments |

At each scope, select **Access control (IAM) > Add > Add role assignment** and assign each Principal and Role from the table. When selecting the Search identity, choose **Managed identity > Search service**. Do not grant excessive Owner permissions to a runtime identity.

## 5. Upload the Selected Industry's Eight Documents

Upload only the eight files for the selected industry to the container. Do not mix industries. Each link opens the repository source in a new tab.

??? example "Manufacturing"
    [quality_control_procedure.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/manufacturing/knowledge/quality_control_procedure.md){ target="_blank" rel="noopener" } · [supplier_quality_manual.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/manufacturing/knowledge/supplier_quality_manual.md){ target="_blank" rel="noopener" } · [engineering_change_process.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/manufacturing/knowledge/engineering_change_process.md){ target="_blank" rel="noopener" } · [nonconforming_material_control.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/manufacturing/knowledge/nonconforming_material_control.md){ target="_blank" rel="noopener" } · [supplier_escalation_and_recovery.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/manufacturing/knowledge/supplier_escalation_and_recovery.md){ target="_blank" rel="noopener" } · [corrective_action_governance.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/manufacturing/knowledge/corrective_action_governance.md){ target="_blank" rel="noopener" } · [quality_audit_evidence_guide.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/manufacturing/knowledge/quality_audit_evidence_guide.md){ target="_blank" rel="noopener" } · [production_release_readiness.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/manufacturing/knowledge/production_release_readiness.md){ target="_blank" rel="noopener" }

??? example "Financial Services"
    [fraud_investigation_procedure.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/financial-services/knowledge/fraud_investigation_procedure.md){ target="_blank" rel="noopener" } · [transaction_monitoring_policy.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/financial-services/knowledge/transaction_monitoring_policy.md){ target="_blank" rel="noopener" } · [investigation_evidence_handling.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/financial-services/knowledge/investigation_evidence_handling.md){ target="_blank" rel="noopener" } · [customer_contact_governance.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/financial-services/knowledge/customer_contact_governance.md){ target="_blank" rel="noopener" } · [data_quality_and_false_positive_review.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/financial-services/knowledge/data_quality_and_false_positive_review.md){ target="_blank" rel="noopener" } · [case_handoff_and_segregation.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/financial-services/knowledge/case_handoff_and_segregation.md){ target="_blank" rel="noopener" } · [case_closure_readiness.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/financial-services/knowledge/case_closure_readiness.md){ target="_blank" rel="noopener" } · [compliance_escalation_process.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/financial-services/knowledge/compliance_escalation_process.md){ target="_blank" rel="noopener" }

??? example "Retail"
    [inventory_replenishment_procedure.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/retail/knowledge/inventory_replenishment_procedure.md){ target="_blank" rel="noopener" } · [returns_and_demand_anomaly_review.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/retail/knowledge/returns_and_demand_anomaly_review.md){ target="_blank" rel="noopener" } · [store_operations_escalation_guide.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/retail/knowledge/store_operations_escalation_guide.md){ target="_blank" rel="noopener" } · [inventory_accuracy_reconciliation.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/retail/knowledge/inventory_accuracy_reconciliation.md){ target="_blank" rel="noopener" } · [supplier_disruption_response.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/retail/knowledge/supplier_disruption_response.md){ target="_blank" rel="noopener" } · [promotion_readiness_review.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/retail/knowledge/promotion_readiness_review.md){ target="_blank" rel="noopener" } · [demand_signal_handling_guide.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/retail/knowledge/demand_signal_handling_guide.md){ target="_blank" rel="noopener" } · [allocation_and_transfer_governance.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/retail/knowledge/allocation_and_transfer_governance.md){ target="_blank" rel="noopener" }

??? example "Healthcare"
    [minimum_necessary_information_handling.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/healthcare/knowledge/minimum_necessary_information_handling.md){ target="_blank" rel="noopener" } · [care_team_escalation_process.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/healthcare/knowledge/care_team_escalation_process.md){ target="_blank" rel="noopener" } · [case_history_documentation_guideline.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/healthcare/knowledge/case_history_documentation_guideline.md){ target="_blank" rel="noopener" } · [documentation_correction_and_addendum.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/healthcare/knowledge/documentation_correction_and_addendum.md){ target="_blank" rel="noopener" } · [downtime_record_reconciliation.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/healthcare/knowledge/downtime_record_reconciliation.md){ target="_blank" rel="noopener" } · [documentation_completeness_checklist.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/healthcare/knowledge/documentation_completeness_checklist.md){ target="_blank" rel="noopener" } · [documentation_incident_escalation.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/healthcare/knowledge/documentation_incident_escalation.md){ target="_blank" rel="noopener" } · [care_transition_handoff.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/healthcare/knowledge/care_transition_handoff.md){ target="_blank" rel="noopener" }

??? example "Public Sector"
    [accessible_communication_and_accommodation.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/public-sector/knowledge/accessible_communication_and_accommodation.md){ target="_blank" rel="noopener" } · [case_review_procedure.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/public-sector/knowledge/case_review_procedure.md){ target="_blank" rel="noopener" } · [fairness_and_protected_attribute_safeguards.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/public-sector/knowledge/fairness_and_protected_attribute_safeguards.md){ target="_blank" rel="noopener" } · [inter_agency_referral_guide.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/public-sector/knowledge/inter_agency_referral_guide.md){ target="_blank" rel="noopener" } · [case_records_and_evidence_handling.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/public-sector/knowledge/case_records_and_evidence_handling.md){ target="_blank" rel="noopener" } · [case_transfer_and_service_continuity.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/public-sector/knowledge/case_transfer_and_service_continuity.md){ target="_blank" rel="noopener" } · [decision_audit_and_closure_readiness.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/public-sector/knowledge/decision_audit_and_closure_readiness.md){ target="_blank" rel="noopener" } · [application_handling_policy.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/public-sector/knowledge/application_handling_policy.md){ target="_blank" rel="noopener" }

Under **Containers > `<pack>-knowledge` > Upload** in the Storage account, select the eight files. After uploading, confirm that the blob count is `8`.

## 6. Configure the Knowledge Source

1. Open the project in the Foundry portal and go to **Build > Knowledge**.
2. If the Search service is not connected, use the connection action to select the Search service from your record. If screen names differ, consult the [official Foundry IQ overview](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/what-is-foundry-iq){ target="_blank" rel="noopener" }; do not create another resource based on assumptions.
3. Select **Create knowledge source** and set Source type to **Azure Blob Storage**.
4. Enter the following values.

    | Field | Value |
    | --- | --- |
    | Name | Recorded `ks-<pack>-policy` |
    | Storage account / connection | Recorded Storage account; use managed identity |
    | Container | Recorded `<pack>-knowledge` |
    | Folder path | Leave blank |
    | Content extraction | A validated setting that ingests text/Markdown |
    | Embedding model | Recorded embedding **deployment name** |
    | Chat completion model | Recorded chat **deployment name** |
    | Image verbalization | Disabled for this Markdown-only lab |

5. Create the source and start synchronization. A 403 immediately after role assignment may be caused by propagation; recheck the role, principal, and scope before retrying.
6. In Knowledge Source status, confirm that `lastSynchronizationState.endTime` has a value, `itemsUpdatesFailed` is `0`, and eight documents were processed.
7. Review the data source, skillset, indexer, and index automatically generated under `createdResources` or in the Search service. Do not edit them directly.
8. In Search Explorer or the Knowledge Source preview, confirm that you can retrieve document content and the source filename.

!!! note "API and Portal Availability Status"
    The core Agentic Retrieval features are documented as GA in Azure AI Search REST API `2026-04-01`, but operations in the Azure portal and Microsoft Foundry portal may be labeled Preview. Defer to the current [official Blob Knowledge Source procedure](https://learn.microsoft.com/en-us/azure/search/agentic-knowledge-source-how-to-blob){ target="_blank" rel="noopener" } as of the date of the lab.

<figure class="lab-image-placeholder" markdown>
    **Image replacement location: Knowledge Source synchronization result**
    `assets/images/labs/foundry-knowledge-source.png`
    <figcaption>Replace with a screen showing the source name, completed synchronization, and zero failures.</figcaption>
</figure>

## 7. Create and Validate the Knowledge Base

1. Select **Build > Knowledge > Create knowledge base** and set Name to the recorded `kb-<pack>-operations`.
2. Add only `ks-<pack>-policy` as the Knowledge Source.
3. Select the recorded chat deployment and, if available on the current screen, enable answer synthesis.
4. Enter the following Retrieval instructions.

    ```text
    Use only this Knowledge Source for questions about procedures, policies, and review items for the selected industry.
    Return the supporting document name and relevant passage, and do not fill in facts that cannot be retrieved.
    ```

5. Enter the following Answer instructions.

    ```text
    Answer in English. Separate confirmed facts, recommendations, and unverified items.
    Do not treat high-impact operations that require human approval as approved.
    List the referenced document names at the end of the answer.
    ```

6. After saving, ask in Playground or Retrieve: "List the procedure documents available for reference in this Knowledge Base."
7. Run the question for the selected industry.

    | Industry | Question | Main Expected Citation Source |
    | --- | --- | --- |
    | Manufacturing | Show the conditions for escalating a quality issue to Engineering Review, including the document name and relevant passage. | `quality_control_procedure.md` |
    | Financial Services | Show the records that must be retained in a fraud investigation, including the document name and relevant passage. | Investigation/evidence documents |
    | Retail | Show the review procedure and required approvals when inventory falls below the reorder point, including the document name. | `inventory_replenishment_procedure.md` |
    | Healthcare | Show the items used to verify case-history record completeness, including the document name and relevant passage. | Completeness/checklist documents |
    | Public Sector | Show the review procedure for cases awaiting additional information, including the document name and relevant passage. | Case/application documents |

8. Confirm that the answer cites the document name and relevant passage and does not include documents from another industry.

<figure class="lab-image-placeholder" markdown>
    **Image replacement location: Knowledge Base answer with citations**
    `assets/images/labs/foundry-knowledge-base-result.png`
    <figcaption>Replace with a screen showing the question, answer, and cited source documents together.</figcaption>
</figure>

!!! note "Models and Availability Requirements"
    This lab does not prescribe available models, deployments, regions, billing, or GA/Preview statuses. Confirm them against current official Microsoft documentation and the available options for the target subscription as of the date of the lab.

## Acceptance Criteria

- [ ] Only documents from the selected pack are targeted for ingestion.
- [ ] You created Storage, Search, a Foundry project, and two model deployments, and recorded their actual values.
- [ ] You assigned the user and Search identity roles at the correct scopes.
- [ ] The indexer processed eight documents with zero failures.
- [ ] A question that does not specify a document name can still retrieve the relevant document.
- [ ] The answer includes citations and does not generate procedures absent from the source.

[Back: Fabric IQ](02-fabric-iq.md){ .md-button }
[Next: Work IQ](04-work-iq.md){ .md-button .md-button--primary }
