# 実顧客データ向けOntology設計・構築ガイド

## 1. 目的

実顧客データからMicrosoft Fabric Ontologyを設計し、Fabric IQとCopilot Studioから業務用語で安全に検索できる状態まで進める。本書は、テーブルをそのままOntologyへ移す手順ではなく、業務概念、識別子、関係、データ品質、権限、運用責任を合意するための実務手順である。

Ontologyは共有された業務語彙であり、entity type、property、directional relationship、実データへのbindingから構成される。生成AIは候補抽出、比較、レビュー準備、テスト作成に使用できるが、業務上の定義、entity key、relationship、アクセス範囲、意思決定ルールを確定する主体ではない。

本書のMicrosoft製品仕様は2026-09-14時点の公開文書で確認した。OntologyはPreviewであるため、実施時点の公式文書も再確認する。

## 2. 最初に決めること

Ontologyの設計をテーブル一覧から始めない。最初に、デモまたは本番で答える価値がある質問を3〜7件決める。

例:

- 未解決の品質問題が影響する部品、工場、設計変更は何か。
- 高リスク取引に関連するケース、口座、確認済み証跡は何か。
- 在庫不足候補に、未着注文と需要シグナルを加味すると何が不足しているか。

各質問について次を記録する。

| 項目 | 内容 |
| --- | --- |
| Question ID | 変更されない識別子 |
| 質問 | 利用者が実際に使用する業務表現 |
| 利用者 | ロールと利用場面 |
| 必要な事実 | entity、property、relationship候補 |
| 許容される鮮度 | リアルタイム、日次、月次など |
| 禁止事項 | 自動承認、診断、凍結、価格変更など |
| 根拠 | 回答で提示すべきID、時刻、情報源 |
| 成功条件 | 期待結果と許容誤差 |

質問に使われないテーブルやpropertyは初期スコープへ入れない。最初のリリースは、質問を端から端まで回答できる最小の縦断スライスとする。

## 3. 役割と承認責任

最低限、次の役割を割り当てる。1人が複数を兼務してもよいが、承認者は明示する。

| 役割 | 主な責任 | 承認対象 |
| --- | --- | --- |
| Business owner | ユースケースと業務価値 | 質問、業務定義、優先順位 |
| Data owner | データ利用目的と責任 | source利用、保持、共有範囲 |
| Data steward | 用語と品質 | entity、property、品質基準 |
| Source system owner | source仕様と変更 | key、更新頻度、抽出方法 |
| Security/Privacy | 機密性と権限 | PII、最小権限、AI利用可否 |
| Ontology designer | 論理モデル | relationship方向、命名、binding案 |
| Fabric administrator | SaaS構成 | workspace、capacity、権限、refresh |
| Test owner | 受入検証 | gold questions、期待結果、回帰判定 |

AIが生成した候補は、Data stewardとSource system ownerが確認し、Business ownerが業務上の意味を承認するまで`Draft`として扱う。

## 4. データと生成AIの安全ゲート

### 4.1 AIへ渡す前の確認

1. 顧客組織で許可されたMicrosoft 365 Copilot、Copilot Chat、または承認済みAI環境だけを使用する。
2. 利用者がsourceファイルを閲覧できることだけでなく、そのデータをAI処理へ使用してよいかをData ownerとSecurity/Privacyに確認する。
3. 最初は実レコードではなく、DDL、列名、型、説明、集計済みprofile、匿名化した例を使用する。
4. 秘密鍵、接続文字列、アクセストークン、パスワード、個人番号、カード情報、診療内容などをpromptへ貼り付けない。
5. Microsoft 365内のファイルをsourceに指定する場合も、SharePoint、OneDrive、Teamsの既存権限とsensitivity labelを確認する。
6. promptと回答は相互作用履歴として保存され得るため、保持、eDiscovery、監査要件を確認する。
7. Web検索は原則無効にする。業界標準との比較が必要な場合だけ、顧客データを含めない別promptで実行する。

Microsoftの公開情報では、Microsoft Copilotは利用者が閲覧権限を持つ組織データだけを提示し、prompt、response、Microsoft Graph経由で取得したデータを基盤LLMの学習には使用しない。一方、生成結果の完全性は保証されないため、人手レビューを省略してはならない。

### 4.2 AIに任せてよい作業

- 会議記録から用語候補、同義語、未解決事項を抽出する。
- DDLやデータ辞書からentity、property、key、relationship候補を作る。
- profile結果からnull、重複、orphan、型不整合の確認事項を整理する。
- 2つのモデル案の差分、利点、リスクを表にする。
- Ontologyを検証する自然言語質問と期待経路の草案を作る。
- 変更影響と回帰テスト候補を列挙する。

### 4.3 AIに確定させない作業

- 同名人物・顧客・設備が同一entityかどうかのentity resolution。
- 法的根拠、保護属性、機密区分、保持期間の決定。
- 欠損keyの推測補完。
- 相関から因果関係を作ること。
- relationship方向、cardinality、履歴の有効期間を証拠なしに確定すること。
- sourceに存在しない業務ルールや承認ルールを作ること。
- 本番Ontology、source table、権限、レコードを自動変更すること。

## 5. 必須成果物

次の7成果物をSharePointなどの管理対象領域へ保存する。最初はExcel workbookの複数sheetでもよい。

1. `use-cases`: 対象質問、利用者、成功条件、禁止事項。
2. `source-inventory`: system、table、owner、更新頻度、権限、機密区分。
3. `business-glossary`: 推奨用語、定義、同義語、除外範囲、owner。
4. `entity-property-catalog`: entity、key、property、型、単位、source mapping。
5. `relationship-catalog`: 一意な関係名、origin、target、mapping table、matched列。
6. `quality-profile`: 件数、null、重複、orphan、分布、鮮度、既知問題。
7. `gold-questions`: 質問、期待entity、期待relationship、期待ID、禁止回答。

すべての行に`status`、`owner`、`approved_by`、`approved_at`、`source_reference`を持たせる。

## 6. 工程A: ユースケースと業務語彙

### 6.1 ワークショップ

60〜90分の業務ワークショップで、次を確認する。

- 利用者が日常的に使う名詞と動詞。
- 同じ言葉が部門ごとに異なる意味を持たないか。
- 何を1件と数えるか。
- どのIDを会話、画面、帳票で使うか。
- 現在状態と履歴をどう区別するか。
- 回答できない場合に何を表示すべきか。
- 人手承認が必要な判断や操作。

### 6.2 Microsoft 365 Copilot用prompt: 用語候補

承認済みの議事録、業務手順、データ辞書をWordまたはCopilot Chatでsourceに指定する。

```text
目的:
Fabric Ontologyの候補となる業務語彙を整理してください。

コンテキスト:
対象業務は「<業務領域>」です。Ontologyは次の質問に答えるために使用します。
1. <質問1>
2. <質問2>
3. <質問3>

参照元:
この会話に添付した「<議事録>」「<業務手順>」「<データ辞書>」だけを使用してください。

期待する出力:
次の列を持つ表にしてください。
- candidate_term
- definition_from_source
- synonyms
- possible_entity_or_property_or_relationship
- source_file_and_section
- ambiguity_or_conflict
- business_owner_to_confirm

制約:
- 参照元にない定義を補完しないでください。
- 不明な項目は「要確認」としてください。
- 個人名や実レコード値は出力しないでください。
- 同じ語が複数の意味を持つ場合は行を分けてください。
```

### 6.3 人手レビュー

- entity候補は、独立したidentityとlifecycleを持つ業務上の「もの」に限定する。
- 単なる状態、分類、説明、集計値はproperty候補とする。
- 操作ログや発生事象は、独自ID、時刻、追跡要件がある場合にevent entity候補とする。
- 画面名、帳票名、物理table名をそのままentity名にしない。
- 略語ではなく、利用者が質問で使う短く一意な名称を選ぶ。

完了条件は、各用語について定義、owner、含むもの、含まないもの、同義語が合意されていること。

## 7. 工程B: source inventoryとデータprofile

### 7.1 収集するmetadata

実レコードをAIへ渡す前に、source system ownerから次を収集する。

| 分類 | 必須項目 |
| --- | --- |
| Source | system、database、schema、table、owner、用途 |
| Column | name、native type、nullable、description、unit、classification |
| Key | primary key候補、unique制約、複合key、生成規則 |
| Relationship | foreign key、join列、想定cardinality、履歴上の意味 |
| Operation | 更新方式、更新頻度、削除方式、late arrival、SLA |
| Security | PII、機密区分、row/column制御、利用可能なworkspace |
| Quality | 行数、null率、distinct数、重複、orphan、最小・最大日時 |

### 7.2 profile指標

entity key候補ごとに最低限、次を計測する。

$$
\text{一意率} = \frac{\text{重複を除いた非NULL key数}}{\text{全行数}}
$$

$$
\text{NULL率} = \frac{\text{keyがNULLの行数}}{\text{全行数}}
$$

$$
\text{orphan率} = \frac{\text{target keyが存在しないrelationship行数}}{\text{relationship全行数}}
$$

entity type keyは各instanceを安定して識別できなければならない。NULLや重複がある候補は、ETLで解決するか複合keyを検討し、理由なく行番号を業務keyとして採用しない。

分布確認では、status値、日時範囲、単位、通貨、タイムゾーン、大小文字、前後空白、削除済みレコード、履歴重複も確認する。閾値は製品既定と決めつけず、データ所有者がユースケースごとに承認する。

### 7.3 Copilot in Excel用prompt: profileレビュー

実データを含むworkbookを使用する場合は、組織がそのworkbookでCopilot利用を許可していることを確認する。編集を避けたい初回レビューではChatまたはPlan modeを使用する。

```text
目的:
このworkbookの「ColumnProfile」tableから、Fabric Ontology設計前に解消すべき品質問題を整理してください。

コンテキスト:
各行はtable/column単位の集計で、row_count、null_count、distinct_count、duplicate_key_count、min_value、max_value、sample_format、classificationを含みます。

期待する出力:
1. entity key候補として不適切な列
2. 型または単位が競合する同名列
3. relationship binding前にorphan確認が必要な列
4. 日時・通貨・小数精度・タイムゾーンの注意点
5. PIIまたは機密情報としてSecurity/Privacy確認が必要な列

各指摘について、table、column、根拠となるprofile値、推奨する確認作業、確認担当を表にしてください。
値を推測せず、profileにない情報は「未計測」としてください。workbookは変更しないでください。
```

### 7.4 Copilot用prompt: DDLから候補抽出

```text
目的:
以下のDDLとデータ辞書からOntology候補を作成してください。これは設計候補であり確定版ではありません。

ユースケース:
<承認済みgold questionを貼る>

入力:
<機密値を含まないDDL、table説明、column説明、profile要約を貼る>

出力形式:
A. entity候補
entity_name | business_definition | source_table | candidate_key | key_risk | lifecycle_owner

B. property候補
entity_name | property_name | business_definition | source_column | proposed_type | unit | sensitivity | include_reason

C. relationship候補
unique_relationship_name | origin_entity | target_entity | mapping_table | origin_match_column | target_match_column | expected_cardinality | evidence

D. 未解決事項
question | required_owner | blocking_or_nonblocking

制約:
- tableを自動的にentityと見なさないでください。
- foreign key名だけで意味を推測しないでください。
- key、方向、cardinalityの証拠がない候補は「要確認」としてください。
- sourceにないrelationshipや業務ルールを作らないでください。
- relationship名は方向が分かる動詞にしてください。
```

## 8. 工程C: 論理Ontology設計

### 8.1 entity選定基準

次の質問の多くに`Yes`ならentity候補とする。

- 業務で独立した名前と定義があるか。
- 複数sourceまたは複数processから参照されるか。
- 安定したkeyを持つか、管理されたkeyを作れるか。
- 独自のlifecycleやownerがあるか。
- 他のentityとの関係を辿る価値があるか。
- gold questionの主語、目的語、絞り込み対象になるか。

初期モデルは通常5〜12 entity程度に抑える。大きな万能entity、列を1つずつentityにする設計、source tableと1対1の大量entityを避ける。

### 8.2 property選定基準

- key、表示名、状態、分類、時刻、質問に必要な測定値を優先する。
- 重複する説明文、自由記述全文、機密情報は必要性をレビューする。
- 値の単位と通貨を明記する。単位が混在する場合は正規化するか単位propertyを保持する。
- timestampは業務時刻、取込時刻、更新時刻を区別し、タイムゾーンを統一する。
- `status`など同名propertyは、entity間で型と意味が大きく異ならないか確認する。
- Fabricで対応しないsource typeはETLで変換する。

公式文書上、entity type keyに使用できるOntology型はstringまたはintegerである。property名とentity名には長さ・文字制約があるため、構築時点の公式文書で確認する。

### 8.3 relationship選定基準

relationshipはdirectionalな業務上の接続として定義する。

| 確認事項 | 例 |
| --- | --- |
| 読み方 | `QualityIssue affects Part` |
| 逆方向の意味 | `Part isAffectedBy QualityIssue`として質問可能か |
| Origin key | `QualityIssue.issue_id` |
| Target key | `Part.part_id` |
| Mapping table | 両keyを同じ行に持つtableまたはjunction table |
| Cardinality | 1:1、1:N、N:M |
| 有効期間 | 現在のみか、開始・終了日時が必要か |
| 品質 | orphan率、重複edge、self-loop |

Fabricのrelationship bindingには、originとtargetのentity type keyに対応する列を同じ行に持つmapping tableが必要である。配列列やカンマ区切りIDを直接N:M relationshipとして扱わず、1行1組のjunction tableへ正規化する。

relationship名はOntology全体で一意にし、`has`や`relatesTo`だけを乱用しない。既知問題として重複relationship名が自然言語query errorにつながる可能性があるため、必要なら`customerOwnsAccount`のようにdomainを含める。

### 8.4 Microsoft 365 Copilot用prompt: 設計レビュー

```text
目的:
添付したentity、property、relationship台帳を、承認済みgold questionsに対してレビューしてください。

確認観点:
- 各質問をどのentityから開始し、どのpropertyでfilterし、どのrelationshipを辿るか
- keyが不安定、NULL、重複、またはsource依存になっていないか
- relationshipの方向とmapping列に証拠があるか
- N:M関係にjunction tableが必要か
- 現在状態と履歴が混ざっていないか
- PIIや機密propertyが質問に不要なのに含まれていないか
- 曖昧または重複するentity/property/relationship名がないか

出力:
question_id | proposed_query_path | pass_or_gap | evidence | required_change | owner

制約:
台帳にないkey、join、業務ルールを作らないでください。確信度ではなく、参照した行またはsourceを示してください。
```

## 9. 工程D: 物理モデルと構築経路

### 9.1 経路の選択

| 条件 | 推奨する開始方法 |
| --- | --- |
| Direct Lake semantic modelに、整理済みtable、primary key、relationshipがある | semantic modelからOntology候補を生成 |
| sourceがLakehouse table中心だがsemantic modelが未整備 | OneLakeから直接構築 |
| ImportまたはDirectQuery semantic modelしかない | 定義候補の生成可否を確認し、bindingは別途設計 |
| 複数sourceの意味・keyが未統一 | 先にcurated managed tableをETLで作る |

semantic modelからの生成では、tableからentity type、columnからproperty、semantic relationshipからrelationship候補が作られる。ただし、time series binding、欠落key、relationship binding、全体レビューは手動作業として残る。

公開文書で確認した主な制約:

- static bindingはentity typeごとに1つのOneLake-backed source。
- managed Lakehouse tableが必要で、external tableは対象外。
- OneLake securityが有効なLakehouseやDelta column mappingには制約がある。
- upstream dataの更新はOntology graphへ自動反映されないため、明示的なrefreshまたはscheduleが必要。
- semantic modelからの自動binding可否はImport、Direct Lake、DirectQueryで異なる。
- current documentationではFabric GraphのDecimal制約が記載されている。金額をDoubleへ変換すると精度要件に影響するため、金融・会計データはData ownerと設計判断を記録し、構築時点の仕様を再確認する。

### 9.2 curated tableの作成

次の場合はraw tableへ直接bindingせず、Ontology専用のcurated managed tableを作る。

- composite keyの表現や型統一が必要。
- 複数sourceの優先順位を決める必要がある。
- soft deleteや履歴からcurrent rowを選ぶ必要がある。
- PII列を除外またはtoken化する必要がある。
- status、通貨、単位、タイムゾーンを正規化する必要がある。
- N:M relationship用junction tableが必要。
- source変更からOntology契約を隔離したい。

curated tableには、可能なら`source_system`、`source_record_id`、`ingested_at`、`effective_from`、`effective_to`、`is_current`などのlineage・履歴項目を保持する。ただし、Ontology propertyとして公開するのは質問と監査に必要な項目だけとする。

## 10. 工程E: 最小縦断スライスの構築

最初の1回は、次の順序を崩さない。

1. 代表質問を1件選ぶ。
2. 起点entityを1つ作成する。
3. key、display name、質問に必要なpropertyだけをbindingする。
4. Instancesで既知IDと期待値を確認する。
5. target entityを1つ追加する。
6. 両keyを持つmapping tableを確認する。
7. relationshipを一意な名前で作成し、origin、target、Matched列を保存する。
8. Graphをrefreshし、既知ID間のedgeを確認する。
9. Graph query builderで1-hopの結果を確認する。
10. Copilot Studioでentity type一覧、単一entity、relationshipの順に質問する。

最初から全entityと全relationshipを作ると、0件やNL2Ontology変換失敗の原因を特定しにくい。1-hopが成功してから2-hop、集計、時系列へ広げる。

## 11. 工程F: 検証

### 11.1 gold dataset

本番全件ではなく、承認済みの代表IDを10〜30件用意する。各IDに期待するpropertyとrelationship先を記録する。PIIが必要ない検証では匿名化または合成IDを使用する。

### 11.2 検証レベル

| レベル | 確認内容 | 合格条件 |
| --- | --- | --- |
| Source | row、key、join | 件数と既知IDがsource ownerの期待と一致 |
| Binding | Instances | keyとpropertyがNULL化・型変換されていない |
| Graph | edge | origin、relationship、targetが期待どおり |
| Query | Graph query builder | filterと1-hop traversalが期待結果を返す |
| MCP | `list_ontology_entity_types` | entityとpropertyを発見できる |
| NL2Ontology | `search_ontology` | 明示的な単一entity質問が成功 |
| Agent | Copilot Studio | ID、根拠、不足情報を区別して回答 |
| Security | 別ロール | 未許可データを返さない |

### 11.3 Copilot用prompt: テスト作成

```text
目的:
承認済みOntology台帳から、段階的な受入テストを作成してください。

入力:
<entity-property catalog>
<relationship catalog>
<匿名化したgold datasetの期待値>

出力:
test_id | level | Japanese_question | start_entity | filter_property | relationship_path | expected_ids | expected_empty_or_nonempty | prohibited_claim

配分:
- schema discovery 2件
- 単一entity ID検索 3件
- property filter 3件
- 1-hop relationship 4件
- 2-hop relationship 2件
- 0件が正しいnegative test 2件
- 権限または機密性test 2件

制約:
- 入力にないIDや期待値を作らないでください。
- 0件が正しいtestと構成不備による0件を区別できる質問にしてください。
- 自動承認や確定判断を期待結果に含めないでください。
```

## 12. 工程G: 本番化と変更管理

### 12.1 リリース前

- Business ownerがgold questionsを承認した。
- Data stewardが用語、key、property、relationshipを承認した。
- Security/Privacyが公開propertyと利用者範囲を承認した。
- Source system ownerが更新頻度と変更通知方法を承認した。
- Instances、Graph、MCP、Copilot Studioのテスト結果を保存した。
- refresh時間、失敗通知、再実行手順を決めた。
- Preview機能の変更リスクとfallbackを記録した。

### 12.2 schema変更時

sourceの列名、型、table名、key、status値、更新方式が変わる場合は、次の順で処理する。

1. source ownerが変更を通知する。
2. AIに旧新schemaの差分整理を依頼してもよいが、影響判定はownerが行う。
3. binding、relationship、gold questionsへの影響を記録する。
4. 非本番workspaceで変更する。
5. Graphをrefreshして回帰テストを実行する。
6. 承認後に本番へ反映する。
7. Ontology台帳と変更履歴を更新する。

### 12.3 Copilot用prompt: 変更影響分析

```text
目的:
source schema変更がOntologyへ与える影響候補を整理してください。

入力:
- 旧schema: <貼り付け>
- 新schema: <貼り付け>
- entity/property/relationship/binding台帳: <添付>
- gold questions: <添付>

出力:
change | affected_binding | affected_relationship | affected_question | severity | evidence | recommended_test | owner_to_approve

制約:
- 自動修正案を実行しないでください。
- rename、type change、key change、削除、nullable化を区別してください。
- 不明な影響は「要検証」とし、推測で互換性ありと判定しないでください。
```

## 13. よくある失敗

| 失敗 | 結果 | 対応 |
| --- | --- | --- |
| tableをすべてentity化 | 用語が技術寄りでNL queryが不安定 | gold questionsから必要概念を絞る |
| keyを表示名で代用 | 重複・変更でinstanceが不安定 | governed IDまたは承認済み複合keyを使う |
| relationshipをpropertyだけで済ませる | traversalできずjoinの意味が共有されない | mapping tableとrelationshipを明示する |
| 配列IDを直接binding | N:M edgeを正しく作れない | junction tableへ正規化する |
| `has`を複数箇所で使用 | 曖昧化と重複名問題 | 一意で方向が分かる名前にする |
| PIIを全列公開 | 不要な露出と権限リスク | 質問に必要な最小propertyへ削減する |
| source更新後に未refresh | 古い回答または0件 | batch更新後にGraph refreshを実行する |
| Copilot案を無承認で採用 | 架空のjoinや定義が混入 | source evidenceとowner承認を必須にする |
| 曖昧な質問だけで試験 | NL2Ontologyとbinding障害を分離できない | schema、単一entity、1-hopの順で試す |

## 14. 完了判定

次をすべて満たした時点で、対象スコープのOntology構成完了とする。

- [ ] 3〜7件のgold questionsと期待結果が承認済み
- [ ] 全entityに定義、owner、安定したkeyがある
- [ ] 全propertyに意味、型、単位、source、機密区分がある
- [ ] 全relationshipに一意な名前、方向、mapping table、両Matched列がある
- [ ] key重複、NULL、orphanの基準と実測値が記録されている
- [ ] curated managed tableがFabricの現行binding制約を満たす
- [ ] 代表IDがInstancesに表示される
- [ ] 代表edgeがGraphに表示される
- [ ] 単一entityと1-hopのNL queryが成功する
- [ ] 権限の異なる利用者でnegative testを実施した
- [ ] refresh、監視、障害対応、schema変更手順がある
- [ ] AIが生成した候補をData stewardとBusiness ownerが承認した

## 15. 公式情報

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
