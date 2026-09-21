# IQ Demo Data Deployment and Reconstruction Runbook

## 1. Purpose

Deploy synthetic data for five industries to Fabric IQ, Foundry IQ, and Work IQ, and distinguish between insufficient data and service configuration problems when the Copilot Studio question catalog returns zero results or retrieval failures.

This runbook uses small demo data. Maintain IDs in the `*-SYN-*` format across all layers, and do not mix them with the sequential IDs in enterprise data.

When using actual customer data, do not apply this runbook's CSV deployment procedure as-is. First use the [Ontology Design and Implementation Guide for Actual Customer Data](../Customer-Data-Ontology-Design-Guide.md) to establish the purpose of use, business vocabulary, keys, relationships, confidentiality classifications, curated tables, and approval responsibilities.

## 2. Local Generation and Validation

Run the following from the repository root.

```bash
source .venv/bin/activate
python scripts/generate_demo_iq_data.py
pytest tests/contract/test_demo_iq_data.py
python scripts/validation/validate_synthetic_data.py
```

The expected generated results are as follows.

| Industry | Fabric table count | Fabric row count | Foundry document count |
| --- | ---: | ---: | ---: |
| Manufacturing | 6 | 19 | 8 |
| Financial Services | 4 | 20 | 8 |
| Retail | 5 | 18 | 8 |
| Healthcare | 4 | 16 | 8 |
| Public Sector | 4 | 18 | 8 |

Output locations:

- Fabric: `industry-packs/<pack>/sample-data/fabric/*.csv`
- Foundry supplemental corpus: `industry-packs/<pack>/sample-data/foundry/demo/knowledge.jsonl`
- Recommended Foundry deployment source: `industry-packs/<pack>/knowledge/*.md`
- Work IQ templates: `industry-packs/<pack>/sample-data/work-iq/*.md`

The generation script regenerates the same content. Do not edit CSV or JSONL files directly; apply changes that will be retained to `DEMO_DATA` or the Knowledge documents, and then regenerate the files.

## 3. Deploy to Fabric IQ

### 3.1 Lakehouse Tables

1. Use a dedicated Fabric workspace and Lakehouse for one industry at a time.
2. Upload all CSV files directly under the target pack's `sample-data/fabric/` to `Files/demo/` in the Lakehouse. Do not use `enterprise/` for this procedure.
3. For each CSV, create a managed Lakehouse table named after the file without its extension.
4. Confirm the table names, column names, types, and row counts. ID columns must be strings, date/time columns must be datetime, and numeric columns must use numeric types.
5. Bind each Ontology entity type to the table with the same name as its `dataset_key` in `ontology/entities.yaml`.
6. Set the entity type key to `identifier_field`, bind every property to the corresponding column of the same name, and save.

Use managed Lakehouse tables in the Ontology. Recheck constraints such as OneLake security, external tables, and Delta column mapping against the current [official Ontology data binding documentation](https://learn.microsoft.com/en-us/fabric/iq/ontology/how-to-bind-data) at deployment time.

### 3.2 Relationship Binding

Create each relationship and resolve the origin and target keys from one row of the mapping table.

#### Manufacturing

| Relationship | Origin | Target | Mapping table | Matched origin | Matched target |
| --- | --- | --- | --- | --- | --- |
| `produces` | `Factory` | `ProductionLine` | `production_lines` | `factory_id` | `line_id` |
| `supplies` | `Supplier` | `Part` | `parts` | `supplier_id` | `part_id` |
| `affects` | `QualityIssue` | `Part` | `quality_issues` | `issue_id` | `part_id` |
| `observedAt` | `QualityIssue` | `Factory` | `quality_issues` | `issue_id` | `factory_id` |
| `addresses` | `EngineeringChange` | `QualityIssue` | `engineering_changes` | `change_id` | `issue_id` |

Do not bind `usedIn` in this small dataset because `used_in_line_ids` is an array. If needed, create a managed junction table with one `part_id` and one `line_id` per row.

#### Financial Services

| Relationship | Origin | Target | Mapping table | Matched origin | Matched target |
| --- | --- | --- | --- | --- | --- |
| `owns` | `Customer` | `Account` | `accounts` | `customer_id` | `account_id` |
| `has` | `Account` | `Transaction` | `transactions` | `account_id` | `transaction_id` |
| `flags` | `FraudCase` | `Transaction` | `fraud_cases` | `case_id` | `transaction_id` |
| `relatesTo` | `FraudCase` | `Account` | `fraud_cases` | `case_id` | `account_id` |

#### Retail

| Relationship | Origin | Target | Mapping table | Matched origin | Matched target |
| --- | --- | --- | --- | --- | --- |
| `stocks` | `Store` | `Product` | `inventory_records` | `store_id` | `product_id` |
| `ordered` | `Store` | `Order` | `orders` | `store_id` | `order_id` |
| `relatesTo` | `DemandSignal` | `Product` | `demand_signals` | `signal_id` | `product_id` |
| `observedAt` | `DemandSignal` | `Store` | `demand_signals` | `signal_id` | `store_id` |

#### Healthcare

| Relationship | Origin | Target | Mapping table | Matched origin | Matched target |
| --- | --- | --- | --- | --- | --- |
| `involves` | `Encounter` | `SyntheticPatient` | `encounters` | `encounter_id` | `patient_id` |
| `attendedBy` | `Encounter` | `Provider` | `encounters` | `encounter_id` | `provider_id` |
| `occursDuring` | `ClinicalEvent` | `Encounter` | `clinical_events` | `event_id` | `encounter_id` |

#### Public Sector

| Relationship | Origin | Target | Mapping table | Matched origin | Matched target |
| --- | --- | --- | --- | --- | --- |
| `involves` | `Case` | `SyntheticCitizen` | `cases` | `case_id` | `citizen_id` |
| `handledBy` | `Case` | `Agency` | `cases` | `case_id` | `agency_id` |
| `partOf` | `Application` | `Case` | `applications` | `application_id` | `case_id` |

### 3.3 Refresh and Pass Criteria

1. Save all entities and relationships.
2. Manually refresh the Graph model associated with the Ontology.
3. Search for a representative ID under **Instances** in the entity type details.
4. Under **Overview/Graph**, confirm the edge from the representative ID to the target entity.
5. Satisfy the following Fabric-side criteria before proceeding to Copilot Studio.

| Industry | Origin check | Relationship check | Target check |
| --- | --- | --- | --- |
| Manufacturing | `QI-SYN-001` | `affects` | `PART-SYN-101` |
| Financial Services | `CASE-SYN-001` | `flags` | `TX-SYN-1001` |
| Retail | `SIGNAL-SYN-001` | `relatesTo` | `PROD-SYN-501` |
| Healthcare | `ENC-SYN-003` | `involves` | `PAT-SYN-103` |
| Public Sector | `APP-SYN-401` | `partOf` | `CASE-SYN-301` |

If the origin is not in Instances, fix the table or entity binding. If the origin and target exist but only the edge is missing, fix the relationship binding. Do not retry in Copilot Studio before refreshing the Graph.

## 4. Deploy to Foundry IQ

### 4.1 Recommended Method

Use a separate Blob container, Knowledge Source, and Knowledge Base for each industry. For the initial demo, upload all 8 files from the target pack's `knowledge/*.md` to the Blob container. Using Markdown makes it easier to isolate document-level citations and retrieval failures.

The generated `sample-data/foundry/demo/knowledge.jsonl` is a supplemental format for validating automated deployment and field search. When using JSONL, verify the API version and the indexer's JSON Lines parsing settings in the actual environment, and explicitly map `id`, `title`, `source_file`, and `content` into the search index. Use Markdown if these settings have not been verified.

### 4.2 Reindex

1. Update the old files in Blob with files of the same names, or empty the demo-only container and reupload all 8 files.
2. Run Knowledge Source synchronization or the indexer.
3. Check the completion status, success and failure counts, and warnings in the execution history.
4. Confirm that all 8 files are searchable. If even one document failed, resolve its retrieval or parsing error first.
5. Run K-01 and K-02 from the question catalog in Knowledge Base Retrieve or Playground.
6. Confirm that the correct `source_file` or Markdown document name is cited, not just that the answer text is correct.

Updating only the Knowledge Source may leave answers based on an old index. Verify Blob update, indexer success, and Knowledge Base retrieval success as three separate stages.

### 4.3 Retrieval Instructions

Include at least the following intent in each industry-specific Knowledge Base.

```text
Use only this industry's uploaded synthetic policy and procedure documents.
For each material claim, cite the source document.
Separate mandatory requirements, recommendations, missing information, and human approvals.
If no supporting passage is retrieved, state that the knowledge base did not provide supporting information.
Answer in English.
```

Do not reproduce product models, prices, regions, or GA/Preview status as fixed values; verify them against Microsoft official documentation at build time.

## 5. Reflect in Work IQ

Do not deploy the Work IQ Markdown files to a dedicated API. Register each document in the Microsoft 365 service used by the test user according to its channel type.

1. Place case-summary files such as `quality-review.md` in a test SharePoint library.
2. Post each message from `*-teams-thread.md` to a test Teams channel.
3. Send the contents of `*-email.md` as Outlook email between test users.
4. Register the date/time, participant roles, and body of `*-meeting.md` in a test calendar and meeting record.
5. Confirm that the test user can find the target records in SharePoint, Teams, Outlook, and the calendar.
6. Connect Work IQ as the same user, and run W-01 and W-02.

If Work IQ returns zero results, check the target user's permissions, retention state, Microsoft 365 search propagation, and matching IDs in the question before adding document content.

## 6. Reconnect and Test in Copilot Studio

1. If a Fabric Ontology or Foundry Knowledge Base was newly created, update the workspace ID, Ontology ID, and Knowledge Base selection for the Copilot Studio Tool.
2. If the same item was updated, do not remove the connection. Start a new test session after the Fabric Graph and Foundry indexer complete.
3. Run F-01, K-01, and W-01 for each industry to verify each single-layer connection.
4. Run the ID-specific F-02, cross-document K-02, and meeting-progress W-02.
5. After all of these succeed, run X-01 through X-03.
6. Save the Tools actually called, inputs, results, response times, and Correlation IDs from Activity trace.

Use the [Copilot Studio IQ Layer Test Execution and Evaluation Guide](Copilot-Studio-IQ-Layer-Test-Catalog.md) for the questions and evaluation criteria.

## 7. Isolate Zero Results and Retrieval Failures

| Symptom | First place to check | Main possible causes |
| --- | --- | --- |
| Fabric Instances has zero results | Fabric Ontology | Managed table, entity key, property binding, data access |
| Fabric has entities but no edges | Fabric Ontology Graph | Relationship origin/target, mapping table, Matched columns, Graph refresh |
| `Failed to translate NL query` | Copilot Studio Activity trace and Fabric | Schema names, duplicate relationship names, Preview translation error |
| Foundry synchronization fails | Knowledge Source/indexer history | Blob permissions, parsing, index mapping, network |
| Foundry synchronization succeeds but returns zero results | Knowledge Base Retrieve | Target Knowledge Source, search terms, document content, filter |
| Foundry answer has no citations | Knowledge Base settings | Answer/retrieval instructions, output settings, number of retrieved documents |
| Work IQ returns zero results | Microsoft 365 search and permissions | Test user permissions, posting destination, search propagation, ID mismatch |
| Only compound questions fail | Copilot Studio Activity trace | Single-layer failure, Tool selection, timeout, unhandled partial failure |

Fabric IQ Ontology MCP is a Preview feature. If Instances and Graph work normally but an explicit single-entity question still fails translation, save the question text, Timestamp, workspace/Ontology ID, Activity trace, and Correlation ID, and provide them to Microsoft support. Do not save credentials or access tokens.

## 8. Pre-Demo Checklist

- [ ] The generation script and contract tests succeeded
- [ ] All CSV files for the target industry were deployed to Fabric as managed tables
- [ ] Instances were displayed for all entities
- [ ] A representative relationship was displayed in Graph
- [ ] The Graph model was refreshed
- [ ] 8 Markdown files were deployed to Foundry
- [ ] The indexer completed with zero failures
- [ ] Correct document citations were confirmed with K-01 and K-02
- [ ] The Work IQ test user could access records in all 4 channels
- [ ] F-01, K-01, and W-01 each succeeded individually
- [ ] The Copilot Studio connection IDs match the target industry
- [ ] Prohibited operations and human-approval boundaries can be explained during the demo
