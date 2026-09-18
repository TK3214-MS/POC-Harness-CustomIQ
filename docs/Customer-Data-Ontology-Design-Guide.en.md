# Ontology Design and Implementation Guide for Actual Customer Data

[![日本語](https://img.shields.io/badge/%E3%81%82-%E6%97%A5%E6%9C%AC%E8%AA%9E-5B6670?style=for-the-badge)](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/docs/Customer-Data-Ontology-Design-Guide.md) [![English](https://img.shields.io/badge/A-English-087F8C?style=for-the-badge)](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/docs/Customer-Data-Ontology-Design-Guide.en.md)

## 1. Purpose

This guide describes how to design a Microsoft Fabric Ontology from actual customer data and make it safely searchable with business terminology from Fabric IQ and Copilot Studio. It is not a procedure for transferring tables directly into an Ontology. It is a practical process for reaching agreement on business concepts, identifiers, relationships, data quality, permissions, and operational responsibilities.

An Ontology is a shared business vocabulary composed of entity types, properties, directional relationships, and bindings to actual data. Generative AI can be used for candidate extraction, comparison, review preparation, and test creation, but it is not the authority that determines business definitions, entity keys, relationships, access scope, or decision rules.

The Microsoft product specifications in this guide were verified against public documentation as of 2026-09-14. Because Ontology is in Preview, also recheck the official documentation current at the time of implementation.

## 2. Decisions to Make First

Do not begin Ontology design from a list of tables. First identify 3 to 7 questions worth answering in a demonstration or production environment.

Examples:

- Which parts, factories, and engineering changes are affected by unresolved quality issues?
- Which cases, accounts, and verified information are associated with high-risk transactions?
- When outstanding orders and demand signals are considered, which items are at risk of insufficient inventory?

Record the following for each question.

| Item | Description |
| --- | --- |
| Question ID | Immutable identifier |
| Question | Business language that users will actually use |
| User | Role and usage context |
| Required facts | Candidate entities, properties, and relationships |
| Acceptable freshness | Real time, daily, monthly, and so on |
| Prohibited actions | Automatic approval, diagnosis, account freeze, price change, and so on |
| Evidence | IDs, timestamps, and sources that the response must present |
| Success criteria | Expected result and acceptable error |

Do not include tables or properties unused by these questions in the initial scope. The first release should be the smallest end-to-end vertical slice that can answer the questions.

## 3. Roles and Approval Responsibilities

Assign at least the following roles. One person may hold multiple roles, but the approver must be explicit.

| Role | Primary responsibility | Approval scope |
| --- | --- | --- |
| Business owner | Use case and business value | Questions, business definitions, priorities |
| Data owner | Purpose and accountability for data use | Source use, retention, sharing scope |
| Data steward | Terminology and quality | Entities, properties, quality standards |
| Source system owner | Source specifications and changes | Keys, update frequency, extraction method |
| Security/Privacy | Confidentiality and permissions | PII, least privilege, eligibility for AI use |
| Ontology designer | Logical model | Relationship direction, naming, binding proposal |
| Fabric administrator | SaaS configuration | Workspace, capacity, permissions, refresh |
| Test owner | Acceptance validation | Gold questions, expected results, regression decisions |

Treat AI-generated candidates as `Draft` until the Data steward and Source system owner review them and the Business owner approves their business meaning.

## 4. Safety Gates for Data and Generative AI

### 4.1 Checks Before Providing Data to AI

1. Use only Microsoft 365 Copilot, Copilot Chat, or another AI environment approved by the customer organization.
2. Confirm with the Data owner and Security/Privacy not only that the user can view the source file, but also that the data may be used for AI processing.
3. Begin with DDL, column names, types, descriptions, aggregated profiles, and anonymized examples rather than actual records.
4. Do not paste private keys, connection strings, access tokens, passwords, personal identification numbers, card information, clinical details, or similar data into prompts.
5. Even when specifying files in Microsoft 365 as sources, review the existing permissions and sensitivity labels in SharePoint, OneDrive, and Teams.
6. Because prompts and responses may be retained as interaction history, review retention, eDiscovery, and audit requirements.
7. Disable web search by default. Only when comparison with industry standards is necessary, run a separate prompt that contains no customer data.

According to Microsoft's public information, Microsoft Copilot presents only organizational data that the user has permission to view, and does not use prompts, responses, or data retrieved through Microsoft Graph to train foundation LLMs. However, generated results are not guaranteed to be complete, so human review must not be omitted.

### 4.2 Tasks That May Be Delegated to AI

- Extract candidate terms, synonyms, and unresolved issues from meeting records.
- Generate candidate entities, properties, keys, and relationships from DDL or a data dictionary.
- Organize issues to review for nulls, duplicates, orphans, and type inconsistencies from profile results.
- Tabulate the differences, benefits, and risks of two model proposals.
- Draft natural-language questions and expected paths for validating the Ontology.
- Enumerate candidate change impacts and regression tests.

### 4.3 Tasks That AI Must Not Finalize

- Entity resolution that determines whether people, customers, or equipment with the same name are the same entity.
- Decisions about legal basis, protected attributes, confidentiality classification, or retention periods.
- Inferred completion of missing keys.
- Creating causal relationships from correlation.
- Finalizing relationship direction, cardinality, or historical validity periods without confirming the source.
- Creating business rules or approval rules that do not exist in the source.
- Automatically modifying the production Ontology, source tables, permissions, or records.

## 5. Required Deliverables

Save the following seven deliverables in a governed location such as SharePoint. Initially, they may be separate sheets in an Excel workbook.

1. `use-cases`: Target questions, users, success criteria, and prohibited actions.
2. `source-inventory`: System, table, owner, update frequency, permissions, and confidentiality classification.
3. `business-glossary`: Preferred term, definition, synonyms, exclusions, and owner.
4. `entity-property-catalog`: Entity, key, property, type, unit, and source mapping.
5. `relationship-catalog`: Unique relationship name, origin, target, mapping table, and matched columns.
6. `quality-profile`: Counts, nulls, duplicates, orphans, distributions, freshness, and known issues.
7. `gold-questions`: Question, expected entity, expected relationship, expected IDs, and prohibited responses.

Include `status`, `owner`, `approved_by`, `approved_at`, and `source_reference` in every row.

## 6. Phase A: Use Cases and Business Vocabulary

### 6.1 Workshop

In a 60 to 90-minute business workshop, confirm the following.

- Nouns and verbs that users employ in their daily work.
- Whether the same term has different meanings in different departments.
- What constitutes one countable record.
- Which IDs are used in conversations, screens, and reports.
- How current state is distinguished from history.
- What should be displayed when a question cannot be answered.
- Decisions and operations that require human approval.

### 6.2 Prompt for Microsoft 365 Copilot: Candidate Terms

Specify approved meeting minutes, business procedures, and data dictionaries as sources in Word or Copilot Chat.

```text
Purpose:
Organize candidate business vocabulary for a Fabric Ontology.

Context:
The target business domain is "<business-domain>". The Ontology will be used to answer the following questions.
1. <question-1>
2. <question-2>
3. <question-3>

Sources:
Use only the "<meeting-minutes>", "<business-procedures>", and "<data-dictionary>" attached to this conversation.

Expected output:
Create a table with the following columns.
- candidate_term
- definition_from_source
- synonyms
- possible_entity_or_property_or_relationship
- source_file_and_section
- ambiguity_or_conflict
- business_owner_to_confirm

Constraints:
- Do not add definitions that are absent from the sources.
- Mark unknown items as "Requires confirmation".
- Do not output personal names or actual record values.
- If one term has multiple meanings, create a separate row for each meaning.
```

### 6.3 Human Review

- Limit entity candidates to business "things" with an independent identity and lifecycle.
- Treat a mere state, classification, description, or aggregate value as a property candidate.
- Treat an operation log or occurrence as an event entity candidate when it has its own ID, timestamp, and traceability requirements.
- Do not use screen names, report names, or physical table names directly as entity names.
- Choose a short, unique name that users employ in questions rather than an abbreviation.

Completion requires agreement on each term's definition, owner, inclusions, exclusions, and synonyms.

## 7. Phase B: Source Inventory and Data Profile

### 7.1 Metadata to Collect

Before providing actual records to AI, collect the following from the source system owner.

| Category | Required items |
| --- | --- |
| Source | System, database, schema, table, owner, purpose |
| Column | Name, native type, nullable, description, unit, classification |
| Key | Primary key candidate, unique constraint, composite key, generation rule |
| Relationship | Foreign key, join column, expected cardinality, historical meaning |
| Operation | Update method, update frequency, deletion method, late arrival, SLA |
| Security | PII, confidentiality classification, row/column controls, permitted workspace |
| Quality | Row count, null rate, distinct count, duplicates, orphans, minimum and maximum timestamps |

### 7.2 Profile Metrics

Measure at least the following for each entity key candidate.

$$
\text{Uniqueness rate} = \frac{\text{Number of distinct non-NULL keys}}{\text{Total number of rows}}
$$

$$
\text{NULL rate} = \frac{\text{Number of rows with a NULL key}}{\text{Total number of rows}}
$$

$$
\text{Orphan rate} = \frac{\text{Number of relationship rows whose target key does not exist}}{\text{Total number of relationship rows}}
$$

An entity type key must identify each instance reliably. Resolve candidates containing NULLs or duplicates through ETL or consider a composite key. Do not adopt a row number as a business key without justification.

When reviewing distributions, also check status values, date ranges, units, currencies, time zones, letter casing, leading and trailing whitespace, deleted records, and duplicate history records. Do not assume that thresholds are product defaults; the Data owner must approve them for each use case.

### 7.3 Prompt for Copilot in Excel: Profile Review

When using a workbook that contains actual data, confirm that the organization permits Copilot use with that workbook. For an initial review that should avoid edits, use Chat or Plan mode.

```text
Purpose:
From the "ColumnProfile" table in this workbook, organize the quality issues that must be resolved before designing a Fabric Ontology.

Context:
Each row is an aggregate for one table/column and includes row_count, null_count, distinct_count, duplicate_key_count, min_value, max_value, sample_format, and classification.

Expected output:
1. Columns unsuitable as entity key candidates
2. Columns with the same name but conflicting types or units
3. Columns that require orphan checks before relationship binding
4. Considerations for dates, currencies, decimal precision, and time zones
5. Columns that require Security/Privacy review as PII or confidential information

For each finding, create a table containing the table, column, supporting profile value, recommended validation task, and responsible reviewer.
Do not infer values. Mark information absent from the profile as "Not measured". Do not modify the workbook.
```

### 7.4 Prompt for Copilot: Extract Candidates from DDL

```text
Purpose:
Create Ontology candidates from the following DDL and data dictionary. These are design candidates, not a finalized design.

Use cases:
<paste-approved-gold-questions>

Input:
<paste-DDL-table-descriptions-column-descriptions-and-profile-summary-without-confidential-values>

Output format:
A. Entity candidates
entity_name | business_definition | source_table | candidate_key | key_risk | lifecycle_owner

B. Property candidates
entity_name | property_name | business_definition | source_column | proposed_type | unit | sensitivity | include_reason

C. Relationship candidates
unique_relationship_name | origin_entity | target_entity | mapping_table | origin_match_column | target_match_column | expected_cardinality | validation_basis

D. Unresolved issues
question | required_owner | blocking_or_nonblocking

Constraints:
- Do not automatically treat a table as an entity.
- Do not infer meaning from a foreign key name alone.
- Mark candidates whose key, direction, or cardinality cannot be validated as "Requires confirmation".
- Do not create relationships or business rules that are absent from the source.
- Use directional verbs for relationship names.
```

## 8. Phase C: Logical Ontology Design

### 8.1 Entity Selection Criteria

Treat an item as an entity candidate when the answer to many of the following questions is `Yes`.

- Does it have an independent business name and definition?
- Is it referenced by multiple sources or processes?
- Does it have a stable key, or can a governed key be created?
- Does it have its own lifecycle or owner?
- Is there value in traversing its relationships to other entities?
- Is it a subject, object, or filter in a gold question?

Usually limit the initial model to approximately 5 to 12 entities. Avoid a large universal entity, designs that make every column an entity, and numerous entities in a one-to-one correspondence with source tables.

### 8.2 Property Selection Criteria

- Prioritize keys, display names, states, classifications, timestamps, and measurements required by the questions.
- Review whether duplicated descriptions, full free-text content, and confidential information are necessary.
- Specify units and currencies. If units are mixed, normalize them or retain a unit property.
- Distinguish business timestamps, ingestion timestamps, and update timestamps, and standardize time zones.
- For same-named properties such as `status`, verify that their types and meanings do not differ substantially across entities.
- Convert unsupported Fabric source types through ETL.

According to the official documentation, Ontology types that may be used for an entity type key are string or integer. Because property and entity names have length and character restrictions, verify the official documentation current at the time of implementation.

### 8.3 Relationship Selection Criteria

Define a relationship as a directional business connection.

| Check | Example |
| --- | --- |
| Reading | `QualityIssue affects Part` |
| Reverse meaning | Can it be queried as `Part isAffectedBy QualityIssue`? |
| Origin key | `QualityIssue.issue_id` |
| Target key | `Part.part_id` |
| Mapping table | A table or junction table containing both keys in the same row |
| Cardinality | 1:1, 1:N, N:M |
| Validity period | Current only, or whether start and end timestamps are required |
| Quality | Orphan rate, duplicate edges, self-loops |

Fabric relationship binding requires a mapping table that contains columns corresponding to the origin and target entity type keys in the same row. Do not treat array columns or comma-separated IDs directly as N:M relationships; normalize them into a junction table containing one pair per row.

Make relationship names unique across the Ontology, and do not overuse `has` or `relatesTo`. A known issue is that duplicate relationship names may cause natural-language query errors, so include the domain when needed, as in `customerOwnsAccount`.

### 8.4 Prompt for Microsoft 365 Copilot: Design Review

```text
Purpose:
Review the attached entity, property, and relationship catalogs against the approved gold questions.

Review criteria:
- For each question, which entity is the starting point, which property provides the filter, and which relationships are traversed
- Whether any key is unstable, NULL, duplicated, or dependent on a source
- Whether relationship direction and mapping columns can be validated from the source
- Whether an N:M relationship requires a junction table
- Whether current state and history are mixed
- Whether PII or confidential properties unnecessary to the questions are included
- Whether any entity, property, or relationship names are ambiguous or duplicated

Output:
question_id | proposed_query_path | pass_or_gap | validation_result | required_change | owner

Constraints:
Do not create keys, joins, or business rules that are absent from the catalogs. Cite the referenced row or source rather than a confidence score.
```

## 9. Phase D: Physical Model and Implementation Path

### 9.1 Select a Path

| Condition | Recommended starting method |
| --- | --- |
| A Direct Lake semantic model has organized tables, primary keys, and relationships | Generate Ontology candidates from the semantic model |
| Sources are primarily Lakehouse tables, but the semantic model is not prepared | Build directly from OneLake |
| Only an Import or DirectQuery semantic model exists | Confirm whether definitions can be generated, and design bindings separately |
| Meanings and keys are not standardized across multiple sources | First create curated managed tables through ETL |

Generation from a semantic model creates candidate entity types from tables, properties from columns, and relationships from semantic relationships. However, time-series binding, missing keys, relationship binding, and the overall review remain manual tasks.

Primary constraints verified in public documentation:

- Static binding supports one OneLake-backed source per entity type.
- Managed Lakehouse tables are required; external tables are not supported.
- Lakehouses with OneLake security enabled and Delta column mapping are subject to constraints.
- Updates to upstream data are not automatically reflected in the Ontology graph, so an explicit refresh or schedule is required.
- Automatic binding availability from semantic models differs among Import, Direct Lake, and DirectQuery.
- Current documentation describes a Decimal constraint in Fabric Graph. Because converting monetary values to Double may affect precision requirements, document the design decision with the Data owner for financial and accounting data, and recheck the specifications current at the time of implementation.

### 9.2 Create Curated Tables

Do not bind directly to raw tables in the following cases. Create curated managed tables dedicated to the Ontology.

- Composite key representation or type standardization is required.
- Priorities among multiple sources must be determined.
- A current row must be selected from soft deletes or history.
- PII columns must be removed or tokenized.
- Statuses, currencies, units, or time zones must be normalized.
- A junction table is required for an N:M relationship.
- The Ontology contract should be isolated from source changes.

Where possible, retain lineage and history fields such as `source_system`, `source_record_id`, `ingested_at`, `effective_from`, `effective_to`, and `is_current` in curated tables. However, expose as Ontology properties only the fields required for questions and audits.

## 10. Phase E: Build the Minimum Vertical Slice

For the first iteration, do not change the following order.

1. Select one representative question.
2. Create one starting entity.
3. Bind only the key, display name, and properties required by the question.
4. Verify a known ID and its expected values in Instances.
5. Add one target entity.
6. Verify the mapping table containing both keys.
7. Create a uniquely named relationship, and save the origin, target, and Matched columns.
8. Refresh the Graph and verify the edge between known IDs.
9. Verify a one-hop result in the Graph query builder.
10. In Copilot Studio, ask questions in this order: entity type list, single entity, and relationship.

Creating every entity and relationship at the outset makes it difficult to identify the cause of zero results or an NL2Ontology conversion failure. After one-hop queries succeed, expand to two-hop queries, aggregations, and time series.

## 11. Phase F: Validation

### 11.1 Gold Dataset

Prepare 10 to 30 approved representative IDs rather than the entire production dataset. Record the expected properties and relationship targets for each ID. Use anonymized or synthetic IDs for validation that does not require PII.

### 11.2 Validation Levels

| Level | What to verify | Acceptance criterion |
| --- | --- | --- |
| Source | Rows, keys, joins | Counts and known IDs match the source owner's expectations |
| Binding | Instances | Keys and properties have not become NULL or undergone unintended type conversion |
| Graph | Edges | Origin, relationship, and target match expectations |
| Query | Graph query builder | Filters and one-hop traversal return expected results |
| MCP | `list_ontology_entity_types` | Entities and properties can be discovered |
| NL2Ontology | `search_ontology` | An explicit single-entity question succeeds |
| Agent | Copilot Studio | Responses distinguish IDs, evidence, and missing information |
| Security | Different role | Unauthorized data is not returned |

### 11.3 Prompt for Copilot: Create Tests

```text
Purpose:
Create phased acceptance tests from the approved Ontology catalogs.

Input:
<entity-property-catalog>
<relationship-catalog>
<expected-values-from-an-anonymized-gold-dataset>

Output:
test_id | level | English_question | start_entity | filter_property | relationship_path | expected_ids | expected_empty_or_nonempty | prohibited_claim

Distribution:
- 2 schema discovery tests
- 3 single-entity ID search tests
- 3 property filter tests
- 4 one-hop relationship tests
- 2 two-hop relationship tests
- 2 negative tests where zero results are correct
- 2 permission or confidentiality tests

Constraints:
- Do not create IDs or expected values that are absent from the input.
- Write questions that distinguish a test where zero results are correct from zero results caused by misconfiguration.
- Do not include automatic approval or a definitive decision in the expected result.
```

## 12. Phase G: Production Readiness and Change Management

### 12.1 Before Release

- The Business owner has approved the gold questions.
- The Data steward has approved the terminology, keys, properties, and relationships.
- Security/Privacy has approved the exposed properties and user scope.
- The Source system owner has approved the update frequency and change notification method.
- Test results for Instances, Graph, MCP, and Copilot Studio have been saved.
- Refresh timing, failure notifications, and rerun procedures have been established.
- Risks and fallback measures for changes to Preview features have been documented.

### 12.2 When the Schema Changes

When a source column name, type, table name, key, status value, or update method changes, process it in the following order.

1. The source owner communicates the change.
2. AI may be asked to organize the differences between the old and new schemas, but the owner assesses the impact.
3. Record the impact on bindings, relationships, and gold questions.
4. Apply the change in a non-production workspace.
5. Refresh the Graph and run regression tests.
6. Apply the change to production after approval.
7. Update the Ontology catalogs and change history.

### 12.3 Prompt for Copilot: Change Impact Analysis

```text
Purpose:
Organize candidate impacts of a source schema change on the Ontology.

Input:
- Old schema: <paste>
- New schema: <paste>
- Entity/property/relationship/binding catalogs: <attach>
- Gold questions: <attach>

Output:
change | affected_binding | affected_relationship | affected_question | severity | validation_result | recommended_test | owner_to_approve

Constraints:
- Do not execute proposed automatic fixes.
- Distinguish renames, type changes, key changes, deletions, and changes to nullable.
- Mark unknown impacts as "Requires validation"; do not infer compatibility.
```

## 13. Common Failures

| Failure | Result | Response |
| --- | --- | --- |
| Making every table an entity | Terminology becomes technical and NL queries become unstable | Narrow the scope to concepts required by the gold questions |
| Substituting a display name for a key | Instances become unstable because of duplicates and changes | Use a governed ID or approved composite key |
| Representing a relationship only as a property | Traversal is impossible and join semantics are not shared | Define the mapping table and relationship explicitly |
| Binding array IDs directly | N:M edges cannot be created correctly | Normalize them into a junction table |
| Using `has` in multiple places | Ambiguity and duplicate-name issues | Use unique, directional names |
| Exposing every PII column | Unnecessary exposure and permission risk | Reduce exposure to the minimum properties required by the questions |
| Failing to refresh after source updates | Stale responses or zero results | Run a Graph refresh after batch updates |
| Adopting a Copilot proposal without approval | Fabricated joins or definitions are introduced | Require source-definition verification and owner approval |
| Testing only ambiguous questions | NL2Ontology and binding failures cannot be isolated | Test schema, a single entity, and one hop in that order |

## 14. Completion Criteria

The Ontology configuration for the target scope is complete when all of the following conditions are satisfied.

- [ ] 3 to 7 gold questions and their expected results have been approved
- [ ] Every entity has a definition, owner, and stable key
- [ ] Every property has a meaning, type, unit, source, and confidentiality classification
- [ ] Every relationship has a unique name, direction, mapping table, and both Matched columns
- [ ] Criteria and measured values for key duplicates, NULLs, and orphans are recorded
- [ ] Curated managed tables satisfy the current Fabric binding constraints
- [ ] Representative IDs are displayed in Instances
- [ ] Representative edges are displayed in Graph
- [ ] Single-entity and one-hop NL queries succeed
- [ ] Negative tests have been performed with users who have different permissions
- [ ] Refresh, monitoring, incident response, and schema-change procedures exist
- [ ] The Data steward and Business owner have approved AI-generated candidates

## 15. Official Information

- [What Is Ontology](https://learn.microsoft.com/en-us/fabric/iq/ontology/overview)
- [Generate an Ontology from a semantic model](https://learn.microsoft.com/en-us/fabric/iq/ontology/concepts-generate)
- [Create entity types](https://learn.microsoft.com/en-us/fabric/iq/ontology/how-to-create-entity-types)
- [Add relationship types](https://learn.microsoft.com/en-us/fabric/iq/ontology/how-to-create-relationship-types)
- [Bind data](https://learn.microsoft.com/en-us/fabric/iq/ontology/how-to-bind-data)
- [View entity type details and refresh](https://learn.microsoft.com/en-us/fabric/iq/ontology/how-to-view-entity-type-details)
- [Troubleshoot Ontology](https://learn.microsoft.com/en-us/fabric/iq/ontology/resources-troubleshooting)
- [Data, Privacy, and Security for Microsoft Copilot](https://learn.microsoft.com/en-us/microsoft-365/copilot/microsoft-365-copilot-privacy)
- [Write a great prompt in Microsoft Copilot](https://support.microsoft.com/en-us/topic/cook-up-great-prompts-getting-the-most-from-copilot-7b614306-d5aa-4b62-8509-e46674a29165)
- [Get started with Copilot in Excel](https://support.microsoft.com/en-us/topic/get-started-with-copilot-in-excel-d7110502-0334-4b4f-a175-a73abdfc118a)
