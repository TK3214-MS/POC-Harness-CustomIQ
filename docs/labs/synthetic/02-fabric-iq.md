# Lab 2: Fabric IQ

想定時間: 60〜90分

このLabでは、選択したIndustry PackのCSVをLakehouse managed tableへ変換し、Ontologyのentity、property、relationshipを構成します。

## 開始前に記録する値

| 項目 | 記録値 |
| --- | --- |
| Fabric workspace | `<your-lab-workspace>` |
| Lakehouse | `IIQ<Industry>LH` |
| Ontology | `IIQ<Industry>Ontology` |
| Dataset | [`industry-packs/<pack>/sample-data/fabric/*.csv`](https://github.com/TK3214-MS/POC-Harness-CustomIQ/tree/main/industry-packs){ target="_blank" rel="noopener" } |
| Fabric workspace ID | `<実際のGUID>` |
| Lakehouse item ID | `<実際のGUID>` |
| Ontology item ID | `<実際のGUID>` |
| 接続ユーザー | `lab.user@contoso.example` |

!!! example "記録例"
    `manufacturing`を選んだ場合は、Lakehouseを`IIQManufacturingLH`、Ontologyを`IIQManufacturingOntology`のように記録します。GUIDとユーザー名は形式例を転記せず、自分のtenantの実値に置き換えます。

## 1. tableを準備

1. Fabric portalでラボ用workspaceを開き、対象capacityへ割り当てられていることを確認します。
2. **New item > Lakehouse**を選択し、`IIQ<Industry>LH`を作成します。
3. Lakehouse explorerの**Files**で`demo` folderを作成します。
4. **Get data > Upload files**から[`industry-packs/<pack>/sample-data/fabric/*.csv`](https://github.com/TK3214-MS/POC-Harness-CustomIQ/tree/main/industry-packs){ target="_blank" rel="noopener" }を`Files/demo/`へアップロードします。
5. CSVごとに**Load to tables > New table**を選び、拡張子を除いた名前のmanaged tableへ変換します。
6. table previewでID列をstring、日時列をdatetime、数値列を適切な数値型として確認します。
7. 各tableのrow countを[デモデータ投入runbook](../../evaluation/Demo-Data-Deployment-Runbook.md)の小容量datasetと照合します。

<figure class="lab-evidence">
    <a class="lab-evidence__link" href="../../../assets/images/labs/fabric-lakehouse-tables.png" target="_blank" rel="noopener" aria-label="LakehouseのFilesとTablesを原寸で開く">
        <img src="../../../assets/images/labs/fabric-lakehouse-tables.png" alt="選択業界のCSVファイルとmanaged table" loading="lazy" decoding="async">
    </a>
    <figcaption>選択業界のCSVファイルとmanaged table</figcaption>
</figure>

!!! warning "binding制約"
    OneLake security、external table、Delta column mappingなどの対応状況は、実施日時点の[公式data binding文書](https://learn.microsoft.com/en-us/fabric/iq/ontology/how-to-bind-data)で確認します。利用できないsourceを無理にbindingせず、ラボ用managed tableへ変換します。

## 2. entityを構成

1. [`industry-packs/<pack>/ontology/entities.yaml`](https://github.com/TK3214-MS/POC-Harness-CustomIQ/tree/main/industry-packs){ target="_blank" rel="noopener" }を開き、`entity_types`を確認します。
2. workspaceで**New item > Ontology (preview)**を選び、`IIQ<Industry>Ontology`を作成します。
3. **Build directly from OneLake**を選択します。
4. Home canvasの**Add entity type**から`entity_types`の各`name`を作成します。
5. entity typeの**Bind data > Add data binding > Lakehouse table**から`dataset_key`と同名のmanaged tableを選択します。
6. **Configure > Manage property bindings > Add properties**で定義済みpropertyをsource列へ対応付ける。
7. **Define entity type key**で`identifier_field`を選択し、display name propertyを設定して保存します。
8. **Instances**を開き、CSV内の既知IDを検索してproperty値を照合します。

## 業界別の完全設定

選択したセクションだけを実施します。`Property ← column`欄では、記載したpropertyを同名CSV列へbindingします。Repositoryリンクは新しいタブで開きます。

??? example "Manufacturing"
    定義: [entities.yaml](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/manufacturing/ontology/entities.yaml){ target="_blank" rel="noopener" }

    | Entity | CSV / table | Rows | Key | Display | Property ← column | 確認値 |
    | --- | --- | ---: | --- | --- | --- | --- |
    | `Factory` | [factories.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/manufacturing/sample-data/fabric/factories.csv){ target="_blank" rel="noopener" } / `factories` | 2 | `factory_id` | `name` | `factory_id`, `name`, `location` | `FAC-SYN-01` / Northfield Assembly Plant |
    | `ProductionLine` | [production_lines.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/manufacturing/sample-data/fabric/production_lines.csv){ target="_blank" rel="noopener" } / `production_lines` | 3 | `line_id` | `name` | `line_id`, `factory_id`, `name` | `LINE-SYN-01` / Valve Assembly Line |
    | `Supplier` | [suppliers.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/manufacturing/sample-data/fabric/suppliers.csv){ target="_blank" rel="noopener" } / `suppliers` | 2 | `supplier_id` | `name` | `supplier_id`, `name`, `region`, `reliability_score` | `SUP-SYN-01` / Northfield Precision Works |
    | `Part` | [parts.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/manufacturing/sample-data/fabric/parts.csv){ target="_blank" rel="noopener" } / `parts` | 4 | `part_id` | `name` | `part_id`, `name`, `supplier_id`, `used_in_line_ids` | `PART-SYN-101` / Valve Housing A |
    | `QualityIssue` | [quality_issues.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/manufacturing/sample-data/fabric/quality_issues.csv){ target="_blank" rel="noopener" } / `quality_issues` | 5 | `issue_id` | `summary` | `issue_id`, `part_id`, `factory_id`, `summary`, `severity`, `status`, `defect_rate_percent`, `detected_at` | `QI-SYN-001` / Surface crack on valve housing |
    | `EngineeringChange` | [engineering_changes.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/manufacturing/sample-data/fabric/engineering_changes.csv){ target="_blank" rel="noopener" } / `engineering_changes` | 3 | `change_id` | `description` | `change_id`, `issue_id`, `description`, `status`, `created_at` | `EC-SYN-002` / Update connector alignment fixture |

    | Relationship | Origin → Target | Mapping table | Origin key ← Matched | Target key ← Matched |
    | --- | --- | --- | --- | --- |
    | `produces` | `Factory` → `ProductionLine` | `production_lines` | `factory_id` ← `factory_id` | `line_id` ← `line_id` |
    | `supplies` | `Supplier` → `Part` | `parts` | `supplier_id` ← `supplier_id` | `part_id` ← `part_id` |
    | `usedIn` | `Part` → `ProductionLine` | `part_production_lines` | `part_id` ← `part_id` | `line_id` ← `line_id` |
    | `affects` | `QualityIssue` → `Part` | `quality_issues` | `issue_id` ← `issue_id` | `part_id` ← `part_id` |
    | `observedAt` | `QualityIssue` → `Factory` | `quality_issues` | `issue_id` ← `issue_id` | `factory_id` ← `factory_id` |
    | `addresses` | `EngineeringChange` → `QualityIssue` | `engineering_changes` | `change_id` ← `change_id` | `issue_id` ← `issue_id` |

    `usedIn`だけは`used_in_line_ids`がJSON配列のため、後述のjunction table作成を先に実施します。

??? example "Financial Services"
    定義: [entities.yaml](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/financial-services/ontology/entities.yaml){ target="_blank" rel="noopener" }

    | Entity | CSV / table | Rows | Key | Display | Property ← column | 確認値 |
    | --- | --- | ---: | --- | --- | --- | --- |
    | `Customer` | [customers.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/financial-services/sample-data/fabric/customers.csv){ target="_blank" rel="noopener" } / `customers` | 5 | `customer_id` | `display_name` | `customer_id`, `display_name`, `segment` | `CUST-SYN-101` / Synthetic Customer 101 |
    | `Account` | [accounts.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/financial-services/sample-data/fabric/accounts.csv){ target="_blank" rel="noopener" } / `accounts` | 5 | `account_id` | `account_type` | `account_id`, `customer_id`, `account_type`, `opened_at` | `ACC-SYN-201` / checking |
    | `Transaction` | [transactions.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/financial-services/sample-data/fabric/transactions.csv){ target="_blank" rel="noopener" } / `transactions` | 5 | `transaction_id` | `merchant` | `transaction_id`, `account_id`, `amount`, `currency`, `merchant`, `transaction_type`, `occurred_at` | `TX-SYN-1001` / Aurelport Digital Goods |
    | `FraudCase` | [fraud_cases.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/financial-services/sample-data/fabric/fraud_cases.csv){ target="_blank" rel="noopener" } / `fraud_cases` | 5 | `case_id` | `status` | `case_id`, `transaction_id`, `account_id`, `status`, `risk_score`, `opened_at` | `CASE-SYN-001` / open / `0.97` |

    | Relationship | Origin → Target | Mapping table | Origin key ← Matched | Target key ← Matched |
    | --- | --- | --- | --- | --- |
    | `owns` | `Customer` → `Account` | `accounts` | `customer_id` ← `customer_id` | `account_id` ← `account_id` |
    | `has` | `Account` → `Transaction` | `transactions` | `account_id` ← `account_id` | `transaction_id` ← `transaction_id` |
    | `flags` | `FraudCase` → `Transaction` | `fraud_cases` | `case_id` ← `case_id` | `transaction_id` ← `transaction_id` |
    | `relatesTo` | `FraudCase` → `Account` | `fraud_cases` | `case_id` ← `case_id` | `account_id` ← `account_id` |

??? example "Retail"
    定義: [entities.yaml](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/retail/ontology/entities.yaml){ target="_blank" rel="noopener" }

    | Entity | CSV / table | Rows | Key | Display | Property ← column | 確認値 |
    | --- | --- | ---: | --- | --- | --- | --- |
    | `Store` | [stores.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/retail/sample-data/fabric/stores.csv){ target="_blank" rel="noopener" } / `stores` | 3 | `store_id` | `name` | `store_id`, `name`, `region` | `STORE-SYN-01` / Aurelport Central |
    | `Product` | [products.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/retail/sample-data/fabric/products.csv){ target="_blank" rel="noopener" } / `products` | 4 | `product_id` | `name` | `product_id`, `name`, `category` | `PROD-SYN-501` / Everyday Travel Mug |
    | `InventoryRecord` | [inventory_records.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/retail/sample-data/fabric/inventory_records.csv){ target="_blank" rel="noopener" } / `inventory_records` | 5 | `inventory_id` | keyを使用 | `inventory_id`, `store_id`, `product_id`, `quantity_on_hand`, `reorder_point` | `INV-SYN-401` / quantity `12`, reorder `20` |
    | `Order` | [orders.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/retail/sample-data/fabric/orders.csv){ target="_blank" rel="noopener" } / `orders` | 3 | `order_id` | `order_date` | `order_id`, `store_id`, `product_id`, `quantity`, `order_date`, `status` | `ORD-SYN-601` / draft |
    | `DemandSignal` | [demand_signals.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/retail/sample-data/fabric/demand_signals.csv){ target="_blank" rel="noopener" } / `demand_signals` | 3 | `signal_id` | `signal_type` | `signal_id`, `product_id`, `store_id`, `signal_type`, `trend_percent`, `detected_at` | `SIGNAL-SYN-001` / promotion_spike / `18.5` |

    | Relationship | Origin → Target | Mapping table | Origin key ← Matched | Target key ← Matched |
    | --- | --- | --- | --- | --- |
    | `stocks` | `Store` → `Product` | `inventory_records` | `store_id` ← `store_id` | `product_id` ← `product_id` |
    | `ordered` | `Store` → `Order` | `orders` | `store_id` ← `store_id` | `order_id` ← `order_id` |
    | `relatesTo` | `DemandSignal` → `Product` | `demand_signals` | `signal_id` ← `signal_id` | `product_id` ← `product_id` |
    | `observedAt` | `DemandSignal` → `Store` | `demand_signals` | `signal_id` ← `signal_id` | `store_id` ← `store_id` |

??? example "Healthcare"
    定義: [entities.yaml](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/healthcare/ontology/entities.yaml){ target="_blank" rel="noopener" }

    | Entity | CSV / table | Rows | Key | Display | Property ← column | 確認値 |
    | --- | --- | ---: | --- | --- | --- | --- |
    | `SyntheticPatient` | [patients.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/healthcare/sample-data/fabric/patients.csv){ target="_blank" rel="noopener" } / `patients` | 5 | `patient_id` | `age_band` | `patient_id`, `age_band`, `note` | `PAT-SYN-101` / 40-49 |
    | `Provider` | [providers.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/healthcare/sample-data/fabric/providers.csv){ target="_blank" rel="noopener" } / `providers` | 3 | `provider_id` | `role` | `provider_id`, `role` | `PROV-SYN-01` / care coordinator |
    | `Encounter` | [encounters.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/healthcare/sample-data/fabric/encounters.csv){ target="_blank" rel="noopener" } / `encounters` | 5 | `encounter_id` | `reason` | `encounter_id`, `patient_id`, `provider_id`, `encounter_date`, `reason` | `ENC-SYN-003` / care coordination |
    | `ClinicalEvent` | [clinical_events.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/healthcare/sample-data/fabric/clinical_events.csv){ target="_blank" rel="noopener" } / `clinical_events` | 3 | `event_id` | `event_type` | `event_id`, `encounter_id`, `event_type`, `description`, `recorded_at` | `EVT-SYN-002` / documentation_gap |

    | Relationship | Origin → Target | Mapping table | Origin key ← Matched | Target key ← Matched |
    | --- | --- | --- | --- | --- |
    | `involves` | `Encounter` → `SyntheticPatient` | `encounters` | `encounter_id` ← `encounter_id` | `patient_id` ← `patient_id` |
    | `attendedBy` | `Encounter` → `Provider` | `encounters` | `encounter_id` ← `encounter_id` | `provider_id` ← `provider_id` |
    | `occursDuring` | `ClinicalEvent` → `Encounter` | `clinical_events` | `event_id` ← `event_id` | `encounter_id` ← `encounter_id` |

??? example "Public Sector"
    定義: [entities.yaml](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/public-sector/ontology/entities.yaml){ target="_blank" rel="noopener" }

    | Entity | CSV / table | Rows | Key | Display | Property ← column | 確認値 |
    | --- | --- | ---: | --- | --- | --- | --- |
    | `SyntheticCitizen` | [citizens.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/public-sector/sample-data/fabric/citizens.csv){ target="_blank" rel="noopener" } / `citizens` | 5 | `citizen_id` | `note` | `citizen_id`, `note` | `CIT-SYN-101` / Fully synthetic service applicant |
    | `Agency` | [agencies.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/public-sector/sample-data/fabric/agencies.csv){ target="_blank" rel="noopener" } / `agencies` | 3 | `agency_id` | `name` | `agency_id`, `name` | `AGENCY-SYN-01` / Aurelport Permit Service |
    | `Case` | [cases.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/public-sector/sample-data/fabric/cases.csv){ target="_blank" rel="noopener" } / `cases` | 5 | `case_id` | `case_type` | `case_id`, `citizen_id`, `agency_id`, `case_type`, `status`, `opened_at` | `CASE-SYN-301` / permit_review / open |
    | `Application` | [applications.csv](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/public-sector/sample-data/fabric/applications.csv){ target="_blank" rel="noopener" } / `applications` | 5 | `application_id` | `application_type` | `application_id`, `case_id`, `application_type`, `status`, `submitted_at` | `APP-SYN-401` / permit_application |

    | Relationship | Origin → Target | Mapping table | Origin key ← Matched | Target key ← Matched |
    | --- | --- | --- | --- | --- |
    | `involves` | `Case` → `SyntheticCitizen` | `cases` | `case_id` ← `case_id` | `citizen_id` ← `citizen_id` |
    | `handledBy` | `Case` → `Agency` | `cases` | `case_id` ← `case_id` | `agency_id` ← `agency_id` |
    | `partOf` | `Application` → `Case` | `applications` | `application_id` ← `application_id` | `case_id` ← `case_id` |

<figure class="lab-evidence">
    <a class="lab-evidence__link" href="../../../assets/images/labs/fabric-entity-binding.png" target="_blank" rel="noopener" aria-label="Entity typeのbinding画面を原寸で開く">
        <img src="../../../assets/images/labs/fabric-entity-binding.png" alt="Source table、entity key、property mappingを含むEntity typeのbinding画面" loading="lazy" decoding="async">
    </a>
    <figcaption>Entity typeのbinding設定</figcaption>
</figure>

## 3. relationshipを構成

1. 次の業界別relation構成ビューから1つ選びます。
2. 一意なrelationship名、origin、targetを作成します。
3. mapping tableを選び、origin keyとtarget keyに対応するMatched列を設定します。
4. 保存後、残りのrelationshipも同様に構成します。
5. 関連するGraph modelをrefreshします。
6. 起点IDを開き、期待するtargetへのedgeを確認します。

relationshipは一度に全件作らず、最初の1件でorigin instance、target instance、edgeを確認してから展開します。`used_in_line_ids`のような配列列は単一Matched列として使用せず、必要な場合は1行1relationshipのjunction tableを作成します。

### 業界別relation構成ビュー

選択した業界だけを展開し、1行ずつFabricのrelationship設定画面へ入力します。

??? info "Manufacturing relation"
    | Relation | Origin → Target | Mapping table | Origin matched | Target matched |
    | --- | --- | --- | --- | --- |
    | `produces` | `Factory` → `ProductionLine` | `production_lines` | `factory_id` | `line_id` |
    | `supplies` | `Supplier` → `Part` | `parts` | `supplier_id` | `part_id` |
    | `usedIn` | `Part` → `ProductionLine` | `part_production_lines` | `part_id` | `line_id` |
    | `affects` | `QualityIssue` → `Part` | `quality_issues` | `issue_id` | `part_id` |
    | `observedAt` | `QualityIssue` → `Factory` | `quality_issues` | `issue_id` | `factory_id` |
    | `addresses` | `EngineeringChange` → `QualityIssue` | `engineering_changes` | `change_id` | `issue_id` |

    `usedIn`を作成する前に、次のjunction table変換を実施します。

??? info "Financial Services relation"
    | Relation | Origin → Target | Mapping table | Origin matched | Target matched |
    | --- | --- | --- | --- | --- |
    | `owns` | `Customer` → `Account` | `accounts` | `customer_id` | `account_id` |
    | `has` | `Account` → `Transaction` | `transactions` | `account_id` | `transaction_id` |
    | `flags` | `FraudCase` → `Transaction` | `fraud_cases` | `case_id` | `transaction_id` |
    | `relatesTo` | `FraudCase` → `Account` | `fraud_cases` | `case_id` | `account_id` |

??? info "Retail relation"
    | Relation | Origin → Target | Mapping table | Origin matched | Target matched |
    | --- | --- | --- | --- | --- |
    | `stocks` | `Store` → `Product` | `inventory_records` | `store_id` | `product_id` |
    | `ordered` | `Store` → `Order` | `orders` | `store_id` | `order_id` |
    | `relatesTo` | `DemandSignal` → `Product` | `demand_signals` | `signal_id` | `product_id` |
    | `observedAt` | `DemandSignal` → `Store` | `demand_signals` | `signal_id` | `store_id` |

??? info "Healthcare relation"
    | Relation | Origin → Target | Mapping table | Origin matched | Target matched |
    | --- | --- | --- | --- | --- |
    | `involves` | `Encounter` → `SyntheticPatient` | `encounters` | `encounter_id` | `patient_id` |
    | `attendedBy` | `Encounter` → `Provider` | `encounters` | `encounter_id` | `provider_id` |
    | `occursDuring` | `ClinicalEvent` → `Encounter` | `clinical_events` | `event_id` | `encounter_id` |

??? info "Public Sector relation"
    | Relation | Origin → Target | Mapping table | Origin matched | Target matched |
    | --- | --- | --- | --- | --- |
    | `involves` | `Case` → `SyntheticCitizen` | `cases` | `case_id` | `citizen_id` |
    | `handledBy` | `Case` → `Agency` | `cases` | `case_id` | `agency_id` |
    | `partOf` | `Application` → `Case` | `applications` | `application_id` | `case_id` |

### Manufacturingの`usedIn`を変換する

Manufacturingを選択した場合だけ実施します。Lakehouse Notebookで次のセルを実行し、`parts.used_in_line_ids`のJSON配列を`part_production_lines`へ展開します。

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
assert invalid.count() == 0, "used_in_line_idsに存在しないProductionLineがあります"

junction = (
    expanded
    .join(production_lines, on="line_id", how="inner")
    .dropDuplicates(["part_id", "line_id"])
)
assert junction.filter(F.col("part_id").isNull() | F.col("line_id").isNull()).count() == 0

junction.write.mode("overwrite").format("delta").saveAsTable("part_production_lines")
display(junction.orderBy("part_id", "line_id"))
```

`PART-SYN-101`と`LINE-SYN-01`の組が表示されることを確認し、業界別表どおりに`usedIn`をbindingします。assertionが失敗した場合はrelationshipを作らず、`parts`と`production_lines`のIDを修正します。

<figure class="lab-evidence">
    <a class="lab-evidence__link" href="../../../assets/images/labs/fabric-ontology-graph.png" target="_blank" rel="noopener" aria-label="Ontology Graphを原寸で開く">
        <img src="../../../assets/images/labs/fabric-ontology-graph.png" alt="既知の合成ID間にrelationship edgeが表示されたOntology Graph" loading="lazy" decoding="async">
    </a>
    <figcaption>既知の合成ID間のOntology Graph</figcaption>
</figure>

## 4. Copilot Studio接続値を控える

Ontology itemのURLまたはitem情報から、**Fabric workspace ID**と**Ontology item ID**を記録します。後続Labでは汎用MCP URLではなく、Copilot Studioの専用**Fabric IQ MCP (Preview)** Toolへ入力します。

業界別のmapping tableとMatched列は[デモデータ投入runbook](../../evaluation/Demo-Data-Deployment-Runbook.md#32-relationship-binding)を参照します。

## 成功条件

- [ ] 全CSVがmanaged tableになっている。
- [ ] 全entity typeにkeyとstatic bindingがある。
- [ ] 起点IDがInstancesに表示される。
- [ ] 少なくとも1つのrelationship edgeを既知ID間で確認しました。

Instancesが0件、またはedgeがない場合は[トラブルシューティング](../../troubleshooting/README.md#fabric-iq)で解消してから進みます。

[前へ: サンプルデータ確認](01-local-setup.md){ .md-button }
[次へ: Foundry IQ](03-foundry-iq.md){ .md-button .md-button--primary }
