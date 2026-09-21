# IQデモデータ投入・再構成ランブック

## 1. 目的

5業界の合成データをFabric IQ、Foundry IQ、Work IQへ投入し、Copilot Studioの質問集で0件や検索失敗が発生した場合に、データ不足とサービス構成不備を切り分ける。

本ランブックでは小容量デモデータを使用する。すべてのレイヤーで`*-SYN-*`形式のIDを維持し、enterpriseデータの連番IDと混在させない。

実顧客データを使用する場合は、本ランブックのCSV投入手順をそのまま適用せず、先に[実顧客データ向けOntology設計・構築ガイド](../Customer-Data-Ontology-Design-Guide.md)で利用目的、業務語彙、key、relationship、機密区分、curated table、承認責任を確定する。

## 2. ローカル生成と検証

リポジトリルートで次を実行する。

```bash
source .venv/bin/activate
python scripts/generate_demo_iq_data.py
pytest tests/contract/test_demo_iq_data.py
python scripts/validation/validate_synthetic_data.py
```

生成結果の目安は次のとおり。

| 業界 | Fabric table数 | Fabric行数 | Foundry文書数 |
| --- | ---: | ---: | ---: |
| Manufacturing | 6 | 19 | 8 |
| Financial Services | 4 | 20 | 8 |
| Retail | 5 | 18 | 8 |
| Healthcare | 4 | 16 | 8 |
| Public Sector | 4 | 18 | 8 |

出力先:

- Fabric: `industry-packs/<pack>/sample-data/fabric/*.csv`
- Foundry補助コーパス: `industry-packs/<pack>/sample-data/foundry/demo/knowledge.jsonl`
- Foundryの推奨投入元: `industry-packs/<pack>/knowledge/*.md`
- Work IQテンプレート: `industry-packs/<pack>/sample-data/work-iq/*.md`

生成スクリプトは同じ内容を再生成する。CSVやJSONLを直接修正せず、継続利用する変更は`DEMO_DATA`またはKnowledge文書へ反映して再生成する。

## 3. Fabric IQへの投入

### 3.1 Lakehouse table

1. 1業界ずつ専用のFabric workspaceとLakehouseを使用する。
2. 対象packの`sample-data/fabric/`直下にあるCSVをすべてLakehouseの`Files/demo/`へアップロードする。`enterprise/`は今回使用しない。
3. CSVごとに、拡張子を除いた名前のmanaged Lakehouse tableを作成する。
4. table名、列名、型、行数を確認する。ID列は文字列、日時列はdatetime、数値列は数値型とする。
5. Ontologyの各entity typeを`ontology/entities.yaml`の`dataset_key`と同名tableへbindingする。
6. entity type keyを`identifier_field`へ設定し、すべてのpropertyを対応する同名列へbindingして保存する。

Ontologyではmanaged Lakehouse tableを使用する。OneLake security、external table、Delta column mappingなどの制約は、投入時点の[Ontology data binding公式文書](https://learn.microsoft.com/en-us/fabric/iq/ontology/how-to-bind-data)で再確認する。

### 3.2 Relationship binding

各relationshipを作成し、mapping tableの1行からoriginとtargetのキーを解決する。

#### Manufacturing

| Relationship | Origin | Target | Mapping table | Matched origin | Matched target |
| --- | --- | --- | --- | --- | --- |
| `produces` | `Factory` | `ProductionLine` | `production_lines` | `factory_id` | `line_id` |
| `supplies` | `Supplier` | `Part` | `parts` | `supplier_id` | `part_id` |
| `affects` | `QualityIssue` | `Part` | `quality_issues` | `issue_id` | `part_id` |
| `observedAt` | `QualityIssue` | `Factory` | `quality_issues` | `issue_id` | `factory_id` |
| `addresses` | `EngineeringChange` | `QualityIssue` | `engineering_changes` | `change_id` | `issue_id` |

`usedIn`は`used_in_line_ids`が配列なので、この小容量データではbindingしない。必要な場合は`part_id`と`line_id`を1行ずつ持つmanaged junction tableを作る。

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

### 3.3 Refreshと合格条件

1. すべてのentityとrelationshipを保存する。
2. Ontologyに関連するGraph modelを手動更新する。
3. entity type detailsの**Instances**で代表IDを検索する。
4. **Overview/Graph**で代表IDからtarget entityへのエッジを確認する。
5. Copilot Studioへ進む前にFabric側で次を満たす。

| 業界 | Origin確認 | Relationship確認 | Target確認 |
| --- | --- | --- | --- |
| Manufacturing | `QI-SYN-001` | `affects` | `PART-SYN-101` |
| Financial Services | `CASE-SYN-001` | `flags` | `TX-SYN-1001` |
| Retail | `SIGNAL-SYN-001` | `relatesTo` | `PROD-SYN-501` |
| Healthcare | `ENC-SYN-003` | `involves` | `PAT-SYN-103` |
| Public Sector | `APP-SYN-401` | `partOf` | `CASE-SYN-301` |

Instancesにoriginがなければtableまたはentity binding、originとtargetが存在してエッジだけなければrelationship bindingを修正する。Graph更新前にCopilot Studioで再試行しない。

## 4. Foundry IQへの投入

### 4.1 推奨方式

業界ごとにBlob container、Knowledge Source、Knowledge Baseを分ける。最初のデモでは、対象packの`knowledge/*.md`全8件をBlob containerへアップロードする。Markdownを使用すると、文書単位の引用と検索失敗の切り分けが容易になる。

生成済み`sample-data/foundry/demo/knowledge.jsonl`は、自動投入やフィールド検索を検証するための補助形式である。JSONLを使用する場合は、利用するAPI versionとindexerのJSON Lines解析設定を実環境で確認し、`id`、`title`、`source_file`、`content`が検索indexへ格納されるよう明示的にmappingする。未確認の場合はMarkdownを使用する。

### 4.2 再index

1. Blob上の旧ファイルを同名で更新するか、デモ専用containerを空にして8件を再アップロードする。
2. Knowledge Sourceの同期またはindexerを実行する。
3. 実行履歴で終了状態、成功・失敗件数、警告を確認する。
4. 8件すべてが検索対象になったことを確認する。失敗文書が1件でもあれば、その文書の取得・解析エラーを先に解消する。
5. Knowledge BaseのRetrieveまたはPlaygroundで、質問集のK-01とK-02を実行する。
6. 回答本文だけでなく、正しい`source_file`またはMarkdown文書名が引用されることを確認する。

Knowledge Sourceを更新しただけでは、古いindexのまま回答される場合がある。Blob更新、indexer成功、Knowledge Base retrieval成功の3段階を個別に確認する。

### 4.3 Retrieval instructions

業界別Knowledge Baseには、少なくとも次の意図を含める。

```text
Use only this industry's uploaded synthetic policy and procedure documents.
For each material claim, cite the source document.
Separate mandatory requirements, recommendations, missing information, and human approvals.
If no supporting passage is retrieved, state that the knowledge base did not provide supporting information.
Answer in Japanese.
```

製品のモデル、価格、リージョン、GA/Preview状態は固定値として転記せず、構築時点のMicrosoft公式文書で確認する。

## 5. Work IQへの反映

Work IQ用Markdownを専用APIへ投入するのではない。テストユーザーが利用するMicrosoft 365サービスへ、各文書のチャネル種別に合わせて登録する。

1. `quality-review.md`などの案件概要をテスト用SharePointライブラリへ配置する。
2. `*-teams-thread.md`の各発言をテスト用Teamsチャンネルへ投稿する。
3. `*-email.md`の内容をテストユーザー間のOutlookメールとして送信する。
4. `*-meeting.md`の日時、参加ロール、本文をテスト用予定表・会議記録へ登録する。
5. テストユーザー自身がSharePoint、Teams、Outlook、予定表から対象を検索できることを確認する。
6. Work IQでは同じユーザーで接続し、W-01、W-02を実行する。

Work IQで0件の場合は、文書内容を増やす前に、対象ユーザーの権限、保持状態、Microsoft 365側の検索反映、質問内IDの一致を確認する。

## 6. Copilot Studioでの再接続とテスト

1. Fabric OntologyまたはFoundry Knowledge Baseを新規作成した場合は、Copilot Studio Toolのworkspace ID、Ontology ID、Knowledge Base選択を更新する。
2. 同じitemを更新した場合は、接続を削除せず、Fabric GraphとFoundry indexerの完了後に新しいテストセッションを開始する。
3. 各業界でF-01、K-01、W-01を実行し、単一レイヤーの接続を確認する。
4. ID指定のF-02、文書横断のK-02、会議進捗のW-02を実行する。
5. すべて成功した後にX-01からX-03を実行する。
6. Activity traceで実際に呼ばれたTool、入力、結果、応答時間、Correlation IDを保存する。

質問と評価項目は[Copilot Studio IQレイヤー別テスト実行・評価ガイド](Copilot-Studio-IQ-Layer-Test-Catalog.md)を使用する。

## 7. 0件・検索失敗の切り分け

| 症状 | 最初に確認する場所 | 主な原因候補 |
| --- | --- | --- |
| Fabric Instancesが0件 | Fabric Ontology | managed table、entity key、property binding、データアクセス |
| Fabricでentityはあるがエッジがない | Fabric Ontology Graph | relationshipのorigin/target、mapping table、Matched列、Graph refresh |
| `Failed to translate NL query` | Copilot Studio Activity traceとFabric | schema名、重複relationship名、Previewの変換エラー |
| Foundry同期に失敗 | Knowledge Source/indexer履歴 | Blob権限、解析、index mapping、ネットワーク |
| Foundry同期成功だが0件 | Knowledge Base Retrieve | 対象Knowledge Source、検索語、文書内容、filter |
| Foundry回答に引用がない | Knowledge Base設定 | answer/retrieval instructions、出力設定、取得文書数 |
| Work IQが0件 | Microsoft 365検索と権限 | テストユーザー権限、投稿先、検索反映、ID不一致 |
| 複合質問だけ失敗 | Copilot Studio Activity trace | 単一レイヤー失敗、Tool選択、timeout、部分失敗の未処理 |

Fabric IQ Ontology MCPはPreview機能である。InstancesとGraphが正常で、単一entityの明示的な質問も変換失敗する場合は、質問文、Timestamp、workspace/Ontology ID、Activity trace、Correlation IDを保存してMicrosoftサポートへ提示する。資格情報やアクセストークンは保存しない。

## 8. デモ実施前チェックリスト

- [ ] 生成スクリプトと契約テストが成功した
- [ ] Fabricに対象業界の全CSVをmanaged tableとして投入した
- [ ] 全entityのInstancesが表示された
- [ ] 代表relationshipがGraphで表示された
- [ ] Graph modelを更新した
- [ ] Foundryへ8件のMarkdownを投入した
- [ ] indexerが失敗0件で完了した
- [ ] K-01とK-02で正しい文書引用を確認した
- [ ] Work IQテストユーザーが4チャネルの記録を参照できた
- [ ] F-01、K-01、W-01が個別に成功した
- [ ] Copilot Studioの接続先IDと対象業界が一致した
- [ ] デモ中の禁止操作と人手承認境界を説明できる
