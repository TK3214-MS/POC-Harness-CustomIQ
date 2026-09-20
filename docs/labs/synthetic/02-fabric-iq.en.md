# Lab 2: Fabric IQ

Estimated time: 60-90 minutes

In this lab, convert the selected Industry Pack's CSV files into Lakehouse managed tables, then configure Ontology entities, properties, and relationships.

## Values to Record Before You Begin

| Item | Recorded Value |
| --- | --- |
| Fabric workspace | `<your-lab-workspace>` |
| Lakehouse | `IIQ<Industry>LH` |
| Ontology | `IIQ<Industry>Ontology` |
| Dataset | [`industry-packs/<pack>/sample-data/fabric/*.csv`](https://github.com/TK3214-MS/POC-Harness-CustomIQ/tree/main/industry-packs){ target="_blank" rel="noopener" } |
| Fabric workspace ID | `<actual GUID>` |
| Lakehouse item ID | `<actual GUID>` |
| Ontology item ID | `<actual GUID>` |
| Connection user | `lab.user@contoso.example` |

!!! example "Example Record"
    If you selected `manufacturing`, record the Lakehouse as `IIQManufacturingLH` and the Ontology as `IIQManufacturingOntology`. Do not copy the example GUID and username formats; replace them with actual values from your tenant.

## 1. Prepare the Tables

1. Open the lab workspace in the Fabric portal and confirm that it is assigned to the target capacity.
2. Select **New item > Lakehouse** and create `IIQ<Industry>LH`.
3. In **Files** in the Lakehouse explorer, create a `demo` folder.
4. From **Get data > Upload files**, upload [`industry-packs/<pack>/sample-data/fabric/*.csv`](https://github.com/TK3214-MS/POC-Harness-CustomIQ/tree/main/industry-packs){ target="_blank" rel="noopener" } to `Files/demo/`.
5. For each CSV, select **Load to tables > New table** and convert it to a managed table named after the file without its extension.
6. In the table preview, confirm that ID columns are strings, date/time columns are datetime values, and numeric columns use appropriate numeric types.
7. Compare each table's row count with the small dataset in the [demo data deployment runbook](../../evaluation/Demo-Data-Deployment-Runbook.md).

<figure class="lab-evidence">
    <a class="lab-evidence__link" href="../../../../assets/images/labs/fabric-lakehouse-tables.png" target="_blank" rel="noopener" aria-label="Open the Lakehouse Files and Tables image at full size">
        <img src="../../../../assets/images/labs/fabric-lakehouse-tables.png" alt="CSV files and managed tables for the selected industry" loading="lazy" decoding="async">
    </a>
    <figcaption>CSV files and managed tables for the selected industry</figcaption>
</figure>

!!! warning "Binding Constraints"
    Confirm support for OneLake security, external tables, Delta column mapping, and related features in the current [official data binding documentation](https://learn.microsoft.com/en-us/fabric/iq/ontology/how-to-bind-data) as of the date of the lab. Do not force an unsupported source into a binding; convert it to a lab managed table.

## 2. Configure Entities

1. Open [`industry-packs/<pack>/ontology/entities.yaml`](https://github.com/TK3214-MS/POC-Harness-CustomIQ/tree/main/industry-packs){ target="_blank" rel="noopener" } and review `entity_types`.
2. In the workspace, select **New item > Ontology (preview)** and create `IIQ<Industry>Ontology`.
3. Select **Build directly from OneLake**.
4. From **Add entity type** on the Home canvas, create each `name` in `entity_types`.
5. From **Bind data > Add data binding > Lakehouse table** for the entity type, select the managed table with the same name as `dataset_key`.
6. Under **Configure > Manage property bindings > Add properties**, map each defined property to its source column.
7. Under **Define entity type key**, select `identifier_field`, set the display name property, and save.
8. Open **Instances**, search for a known ID from the CSV, and compare its property values.

## Complete Configuration by Industry

Complete only the section for your selected industry. In the `Property <- column` column, bind each listed property to the CSV column with the same name. Repository links open in a new tab.

??? example "Manufacturing"
    Definition: [entities.yaml](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/manufacturing/ontology/entities.yaml){ target="_blank" rel="noopener" }

    | Entity | CSV / table | Rows | Key | Display | Property <- column | Verification Value |
    | --- | --- | ---: | --- | --- | --- | --- |
    | `Factory` | [factories.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/manufacturing/sample-data/fabric/factories.csv){ target="_blank" rel="noopener" } / `factories` | 2 | `factory_id` | `name` | `factory_id`, `name`, `location` | `FAC-SYN-01` / Northfield Assembly Plant |
    | `ProductionLine` | [production_lines.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/manufacturing/sample-data/fabric/production_lines.csv){ target="_blank" rel="noopener" } / `production_lines` | 3 | `line_id` | `name` | `line_id`, `factory_id`, `name` | `LINE-SYN-01` / Valve Assembly Line |
    | `Supplier` | [suppliers.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/manufacturing/sample-data/fabric/suppliers.csv){ target="_blank" rel="noopener" } / `suppliers` | 2 | `supplier_id` | `name` | `supplier_id`, `name`, `region`, `reliability_score` | `SUP-SYN-01` / Northfield Precision Works |
    | `Part` | [parts.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/manufacturing/sample-data/fabric/parts.csv){ target="_blank" rel="noopener" } / `parts` | 4 | `part_id` | `name` | `part_id`, `name`, `supplier_id`, `used_in_line_ids` | `PART-SYN-101` / Valve Housing A |
    | `QualityIssue` | [quality_issues.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/manufacturing/sample-data/fabric/quality_issues.csv){ target="_blank" rel="noopener" } / `quality_issues` | 5 | `issue_id` | `summary` | `issue_id`, `part_id`, `factory_id`, `summary`, `severity`, `status`, `defect_rate_percent`, `detected_at` | `QI-SYN-001` / Surface crack on valve housing |
    | `EngineeringChange` | [engineering_changes.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/manufacturing/sample-data/fabric/engineering_changes.csv){ target="_blank" rel="noopener" } / `engineering_changes` | 3 | `change_id` | `description` | `change_id`, `issue_id`, `description`, `status`, `created_at` | `EC-SYN-002` / Update connector alignment fixture |

    | Relationship | Origin -> Target | Mapping table | Origin key <- Matched | Target key <- Matched |
    | --- | --- | --- | --- | --- |
    | `produces` | `Factory` -> `ProductionLine` | `production_lines` | `factory_id` <- `factory_id` | `line_id` <- `line_id` |
    | `supplies` | `Supplier` -> `Part` | `parts` | `supplier_id` <- `supplier_id` | `part_id` <- `part_id` |
    | `usedIn` | `Part` -> `ProductionLine` | `part_production_lines` | `part_id` <- `part_id` | `line_id` <- `line_id` |
    | `affects` | `QualityIssue` -> `Part` | `quality_issues` | `issue_id` <- `issue_id` | `part_id` <- `part_id` |
    | `observedAt` | `QualityIssue` -> `Factory` | `quality_issues` | `issue_id` <- `issue_id` | `factory_id` <- `factory_id` |
    | `addresses` | `EngineeringChange` -> `QualityIssue` | `engineering_changes` | `change_id` <- `change_id` | `issue_id` <- `issue_id` |

    Only `usedIn` requires the junction-table creation described later because `used_in_line_ids` is a JSON array.

??? example "Financial Services"
    Definition: [entities.yaml](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/financial-services/ontology/entities.yaml){ target="_blank" rel="noopener" }

    | Entity | CSV / table | Rows | Key | Display | Property <- column | Verification Value |
    | --- | --- | ---: | --- | --- | --- | --- |
    | `Customer` | [customers.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/financial-services/sample-data/fabric/customers.csv){ target="_blank" rel="noopener" } / `customers` | 5 | `customer_id` | `display_name` | `customer_id`, `display_name`, `segment` | `CUST-SYN-101` / Synthetic Customer 101 |
    | `Account` | [accounts.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/financial-services/sample-data/fabric/accounts.csv){ target="_blank" rel="noopener" } / `accounts` | 5 | `account_id` | `account_type` | `account_id`, `customer_id`, `account_type`, `opened_at` | `ACC-SYN-201` / checking |
    | `Transaction` | [transactions.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/financial-services/sample-data/fabric/transactions.csv){ target="_blank" rel="noopener" } / `transactions` | 5 | `transaction_id` | `merchant` | `transaction_id`, `account_id`, `amount`, `currency`, `merchant`, `transaction_type`, `occurred_at` | `TX-SYN-1001` / Aurelport Digital Goods |
    | `FraudCase` | [fraud_cases.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/financial-services/sample-data/fabric/fraud_cases.csv){ target="_blank" rel="noopener" } / `fraud_cases` | 5 | `case_id` | `status` | `case_id`, `transaction_id`, `account_id`, `status`, `risk_score`, `opened_at` | `CASE-SYN-001` / open / `0.97` |

    | Relationship | Origin -> Target | Mapping table | Origin key <- Matched | Target key <- Matched |
    | --- | --- | --- | --- | --- |
    | `owns` | `Customer` -> `Account` | `accounts` | `customer_id` <- `customer_id` | `account_id` <- `account_id` |
    | `has` | `Account` -> `Transaction` | `transactions` | `account_id` <- `account_id` | `transaction_id` <- `transaction_id` |
    | `flags` | `FraudCase` -> `Transaction` | `fraud_cases` | `case_id` <- `case_id` | `transaction_id` <- `transaction_id` |
    | `relatesTo` | `FraudCase` -> `Account` | `fraud_cases` | `case_id` <- `case_id` | `account_id` <- `account_id` |

??? example "Retail"
    Definition: [entities.yaml](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/retail/ontology/entities.yaml){ target="_blank" rel="noopener" }

    | Entity | CSV / table | Rows | Key | Display | Property <- column | Verification Value |
    | --- | --- | ---: | --- | --- | --- | --- |
    | `Store` | [stores.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/retail/sample-data/fabric/stores.csv){ target="_blank" rel="noopener" } / `stores` | 3 | `store_id` | `name` | `store_id`, `name`, `region` | `STORE-SYN-01` / Aurelport Central |
    | `Product` | [products.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/retail/sample-data/fabric/products.csv){ target="_blank" rel="noopener" } / `products` | 4 | `product_id` | `name` | `product_id`, `name`, `category` | `PROD-SYN-501` / Everyday Travel Mug |
    | `InventoryRecord` | [inventory_records.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/retail/sample-data/fabric/inventory_records.csv){ target="_blank" rel="noopener" } / `inventory_records` | 5 | `inventory_id` | use the key | `inventory_id`, `store_id`, `product_id`, `quantity_on_hand`, `reorder_point` | `INV-SYN-401` / quantity `12`, reorder `20` |
    | `Order` | [orders.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/retail/sample-data/fabric/orders.csv){ target="_blank" rel="noopener" } / `orders` | 3 | `order_id` | `order_date` | `order_id`, `store_id`, `product_id`, `quantity`, `order_date`, `status` | `ORD-SYN-601` / draft |
    | `DemandSignal` | [demand_signals.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/retail/sample-data/fabric/demand_signals.csv){ target="_blank" rel="noopener" } / `demand_signals` | 3 | `signal_id` | `signal_type` | `signal_id`, `product_id`, `store_id`, `signal_type`, `trend_percent`, `detected_at` | `SIGNAL-SYN-001` / promotion_spike / `18.5` |

    | Relationship | Origin -> Target | Mapping table | Origin key <- Matched | Target key <- Matched |
    | --- | --- | --- | --- | --- |
    | `stocks` | `Store` -> `Product` | `inventory_records` | `store_id` <- `store_id` | `product_id` <- `product_id` |
    | `ordered` | `Store` -> `Order` | `orders` | `store_id` <- `store_id` | `order_id` <- `order_id` |
    | `relatesTo` | `DemandSignal` -> `Product` | `demand_signals` | `signal_id` <- `signal_id` | `product_id` <- `product_id` |
    | `observedAt` | `DemandSignal` -> `Store` | `demand_signals` | `signal_id` <- `signal_id` | `store_id` <- `store_id` |

??? example "Healthcare"
    Definition: [entities.yaml](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/healthcare/ontology/entities.yaml){ target="_blank" rel="noopener" }

    | Entity | CSV / table | Rows | Key | Display | Property <- column | Verification Value |
    | --- | --- | ---: | --- | --- | --- | --- |
    | `SyntheticPatient` | [patients.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/healthcare/sample-data/fabric/patients.csv){ target="_blank" rel="noopener" } / `patients` | 5 | `patient_id` | `age_band` | `patient_id`, `age_band`, `note` | `PAT-SYN-101` / 40-49 |
    | `Provider` | [providers.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/healthcare/sample-data/fabric/providers.csv){ target="_blank" rel="noopener" } / `providers` | 3 | `provider_id` | `role` | `provider_id`, `role` | `PROV-SYN-01` / care coordinator |
    | `Encounter` | [encounters.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/healthcare/sample-data/fabric/encounters.csv){ target="_blank" rel="noopener" } / `encounters` | 5 | `encounter_id` | `reason` | `encounter_id`, `patient_id`, `provider_id`, `encounter_date`, `reason` | `ENC-SYN-003` / care coordination |
    | `ClinicalEvent` | [clinical_events.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/healthcare/sample-data/fabric/clinical_events.csv){ target="_blank" rel="noopener" } / `clinical_events` | 3 | `event_id` | `event_type` | `event_id`, `encounter_id`, `event_type`, `description`, `recorded_at` | `EVT-SYN-002` / documentation_gap |

    | Relationship | Origin -> Target | Mapping table | Origin key <- Matched | Target key <- Matched |
    | --- | --- | --- | --- | --- |
    | `involves` | `Encounter` -> `SyntheticPatient` | `encounters` | `encounter_id` <- `encounter_id` | `patient_id` <- `patient_id` |
    | `attendedBy` | `Encounter` -> `Provider` | `encounters` | `encounter_id` <- `encounter_id` | `provider_id` <- `provider_id` |
    | `occursDuring` | `ClinicalEvent` -> `Encounter` | `clinical_events` | `event_id` <- `event_id` | `encounter_id` <- `encounter_id` |

??? example "Public Sector"
    Definition: [entities.yaml](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/public-sector/ontology/entities.yaml){ target="_blank" rel="noopener" }

    | Entity | CSV / table | Rows | Key | Display | Property <- column | Verification Value |
    | --- | --- | ---: | --- | --- | --- | --- |
    | `SyntheticCitizen` | [citizens.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/public-sector/sample-data/fabric/citizens.csv){ target="_blank" rel="noopener" } / `citizens` | 5 | `citizen_id` | `note` | `citizen_id`, `note` | `CIT-SYN-101` / Fully synthetic service applicant |
    | `Agency` | [agencies.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/public-sector/sample-data/fabric/agencies.csv){ target="_blank" rel="noopener" } / `agencies` | 3 | `agency_id` | `name` | `agency_id`, `name` | `AGENCY-SYN-01` / Aurelport Permit Service |
    | `Case` | [cases.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/public-sector/sample-data/fabric/cases.csv){ target="_blank" rel="noopener" } / `cases` | 5 | `case_id` | `case_type` | `case_id`, `citizen_id`, `agency_id`, `case_type`, `status`, `opened_at` | `CASE-SYN-301` / permit_review / open |
    | `Application` | [applications.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/public-sector/sample-data/fabric/applications.csv){ target="_blank" rel="noopener" } / `applications` | 5 | `application_id` | `application_type` | `application_id`, `case_id`, `application_type`, `status`, `submitted_at` | `APP-SYN-401` / permit_application |

    | Relationship | Origin -> Target | Mapping table | Origin key <- Matched | Target key <- Matched |
    | --- | --- | --- | --- | --- |
    | `involves` | `Case` -> `SyntheticCitizen` | `cases` | `case_id` <- `case_id` | `citizen_id` <- `citizen_id` |
    | `handledBy` | `Case` -> `Agency` | `cases` | `case_id` <- `case_id` | `agency_id` <- `agency_id` |
    | `partOf` | `Application` -> `Case` | `applications` | `application_id` <- `application_id` | `case_id` <- `case_id` |

<figure class="lab-evidence">
    <a class="lab-evidence__link" href="../../../../assets/images/labs/fabric-entity-binding.png" target="_blank" rel="noopener" aria-label="Open the entity type binding image at full size">
        <img src="../../../../assets/images/labs/fabric-entity-binding.png" alt="Entity type binding with the source table, entity key, and property mappings" loading="lazy" decoding="async">
    </a>
    <figcaption>Entity type binding configuration</figcaption>
</figure>

## 3. Configure Relationships

1. Select one of the industry-specific relationship configuration views below.
2. Create a unique relationship name, origin, and target.
3. Select the mapping table and set the Matched columns corresponding to the origin key and target key.
4. After saving, configure the remaining relationships in the same way.
5. Refresh the related Graph model.
6. Open a starting ID and confirm its edge to the expected target.

Do not create every relationship at once. Confirm the origin instance, target instance, and edge for the first relationship before expanding the configuration. Do not use an array column such as `used_in_line_ids` as a single Matched column; create a junction table with one relationship per row when necessary.

### Relationship Configuration Views by Industry

Expand only the selected industry and enter each row into the Fabric relationship settings screen.

??? info "Manufacturing relationship"
    | Relationship | Origin -> Target | Mapping table | Origin matched | Target matched |
    | --- | --- | --- | --- | --- |
    | `produces` | `Factory` -> `ProductionLine` | `production_lines` | `factory_id` | `line_id` |
    | `supplies` | `Supplier` -> `Part` | `parts` | `supplier_id` | `part_id` |
    | `usedIn` | `Part` -> `ProductionLine` | `part_production_lines` | `part_id` | `line_id` |
    | `affects` | `QualityIssue` -> `Part` | `quality_issues` | `issue_id` | `part_id` |
    | `observedAt` | `QualityIssue` -> `Factory` | `quality_issues` | `issue_id` | `factory_id` |
    | `addresses` | `EngineeringChange` -> `QualityIssue` | `engineering_changes` | `change_id` | `issue_id` |

    Before creating `usedIn`, perform the following junction-table conversion.

??? info "Financial Services relationship"
    | Relationship | Origin -> Target | Mapping table | Origin matched | Target matched |
    | --- | --- | --- | --- | --- |
    | `owns` | `Customer` -> `Account` | `accounts` | `customer_id` | `account_id` |
    | `has` | `Account` -> `Transaction` | `transactions` | `account_id` | `transaction_id` |
    | `flags` | `FraudCase` -> `Transaction` | `fraud_cases` | `case_id` | `transaction_id` |
    | `relatesTo` | `FraudCase` -> `Account` | `fraud_cases` | `case_id` | `account_id` |

??? info "Retail relationship"
    | Relationship | Origin -> Target | Mapping table | Origin matched | Target matched |
    | --- | --- | --- | --- | --- |
    | `stocks` | `Store` -> `Product` | `inventory_records` | `store_id` | `product_id` |
    | `ordered` | `Store` -> `Order` | `orders` | `store_id` | `order_id` |
    | `relatesTo` | `DemandSignal` -> `Product` | `demand_signals` | `signal_id` | `product_id` |
    | `observedAt` | `DemandSignal` -> `Store` | `demand_signals` | `signal_id` | `store_id` |

??? info "Healthcare relationship"
    | Relationship | Origin -> Target | Mapping table | Origin matched | Target matched |
    | --- | --- | --- | --- | --- |
    | `involves` | `Encounter` -> `SyntheticPatient` | `encounters` | `encounter_id` | `patient_id` |
    | `attendedBy` | `Encounter` -> `Provider` | `encounters` | `encounter_id` | `provider_id` |
    | `occursDuring` | `ClinicalEvent` -> `Encounter` | `clinical_events` | `event_id` | `encounter_id` |

??? info "Public Sector relationship"
    | Relationship | Origin -> Target | Mapping table | Origin matched | Target matched |
    | --- | --- | --- | --- | --- |
    | `involves` | `Case` -> `SyntheticCitizen` | `cases` | `case_id` | `citizen_id` |
    | `handledBy` | `Case` -> `Agency` | `cases` | `case_id` | `agency_id` |
    | `partOf` | `Application` -> `Case` | `applications` | `application_id` | `case_id` |

### Convert Manufacturing `usedIn`

Complete this step only if you selected Manufacturing. Run the following cell in a Lakehouse Notebook to expand the JSON array in `parts.used_in_line_ids` into `part_production_lines`.

```python
from pyspark.sql import functions as F
from pyspark.sql.types import ArrayType, StringType

parts = spark.table("parts")
production_lines = spark.table("production_lines").select("line_id").distinct()

expanded = parts.select(
    "part_id",
    F.explode(F.from_json("used_in_line_ids", ArrayType(StringType()))).alias("line_id"),
)
invalid = expanded.join(production_lines, on="line_id", how="left_anti")
assert invalid.count() == 0, "ProductionLine contains values not found in used_in_line_ids"

junction = (
    expanded
    .join(production_lines, on="line_id", how="inner")
    .dropDuplicates(["part_id", "line_id"])
)
assert junction.filter(F.col("part_id").isNull() | F.col("line_id").isNull()).count() == 0

junction.write.mode("overwrite").format("delta").saveAsTable("part_production_lines")
display(junction.orderBy("part_id", "line_id"))
```

Confirm that the `PART-SYN-101` and `LINE-SYN-01` pair is displayed, then bind `usedIn` as shown in the industry-specific table. If the assertion fails, do not create the relationship; correct the IDs in `parts` and `production_lines`.

<figure class="lab-evidence">
    <a class="lab-evidence__link" href="../../../../assets/images/labs/fabric-ontology-graph.png" target="_blank" rel="noopener" aria-label="Open the Ontology Graph image at full size">
        <img src="../../../../assets/images/labs/fabric-ontology-graph.png" alt="Ontology Graph showing relationship edges between known synthetic IDs" loading="lazy" decoding="async">
    </a>
    <figcaption>Ontology Graph for known synthetic IDs</figcaption>
</figure>

## 4. Record Copilot Studio Connection Values

From the Ontology item's URL or item information, record the **Fabric workspace ID** and **Ontology item ID**. In a later lab, enter them in Copilot Studio's dedicated **Fabric IQ MCP (Preview)** tool, not a generic MCP URL.

See the [demo data deployment runbook](../../evaluation/Demo-Data-Deployment-Runbook.md#32-relationship-binding) for each industry's mapping tables and Matched columns.

## Acceptance Criteria

- [ ] Every CSV is a managed table.
- [ ] Every entity type has a key and static binding.
- [ ] The starting ID appears in Instances.
- [ ] You confirmed at least one relationship edge between known IDs.

If Instances contains zero items or no edge appears, resolve the issue using [troubleshooting](../../troubleshooting/README.md#fabric-iq) before continuing.

[Back: Review sample data](01-local-setup.md){ .md-button }
[Next: Foundry IQ](03-foundry-iq.md){ .md-button .md-button--primary }
