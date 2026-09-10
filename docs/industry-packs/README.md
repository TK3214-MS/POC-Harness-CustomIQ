# Industry Pack ガイド インデックス

このフォルダは、本アクセラレータの中核的な差し替え可能単位である **Industry Pack** に関するドキュメントの入口です。Industry Pack は「業界固有のオントロジー・データ・ツール・エージェントロジック」を1つのフォルダにまとめたプラグインであり、`iq_platform/` 配下のプラットフォームコードを変更せずに追加・切り替えができるように設計されています（[アーキテクチャガイド §5](../architecture/architecture-guide.md)）。

新しい Industry Pack を追加する手順、および Ontology / Semantic Model / Sample Data / Responsible AI の各観点の詳細な執筆ガイドは、[Industry-Pack-Guide.md](Industry-Pack-Guide.md) にまとめています。本ページはその概要と索引です。

## 1. Manifest スキーマ

各 Industry Pack のルートには `manifest.yaml` があり、`iq_platform.contracts.manifest.IndustryPackManifest`（Pydantic モデル）で検証されます（[ADR-0004](../decisions/0004-industry-pack-manifest-schema.md)、[ADR-0011](../decisions/0011-generic-orchestrator-and-semantic-adapter.md)）。主なフィールドは次のとおりです。

| フィールド | 内容 |
|---|---|
| `id` / `display_name` / `version` / `description` | Pack の識別情報 |
| `default_scenario` | Demo CLI がデフォルトで実行する代表シナリオ名 |
| `ontology_path` / `semantic_model_path` | エンティティ種別・関係性の定義ファイル |
| `sample_data_path` | 合成データ生成モジュール（`data/generator.py`） |
| `knowledge_path` / `work_context_path` | Knowledge 文書 / Work Context フィクスチャ |
| `mcp_tools_path` | MCP Tool 実装モジュール |
| `semantic_relationships_path` | Fabric IQ Mock Adapter が委譲するセマンティクスプラグイン |
| `scenario_module_path` | Orchestrator が委譲するシナリオ実行プラグイン |
| `agent_instructions_path` / `demo_prompts_path` / `expected_results_path` | エージェント指示・デモプロンプト・期待結果 |
| `evaluation_path` | `evaluations/rubric.yaml`（評価エンジンの入力） |
| `terminology_path` / `responsible_ai_path` | 用語集 / Responsible AI 通知文 |
| `prohibited_actions` / `human_approval_rules` | ガードレール（禁止アクション一覧 / 人間承認が必須なアクション一覧） |

フィールドの完全な一覧・型・執筆時の注意点は [Industry-Pack-Guide.md](Industry-Pack-Guide.md) の「manifest.yaml フィールドリファレンス」を参照してください。

## 2. 実装済みの5業界 Industry Pack

| Pack ID | 業界 | 代表シナリオ (`default_scenario`) |
|---|---|---|
| `manufacturing` | Manufacturing | `quality-issue-investigation`（品質問題調査） |
| `financial-services` | Financial Services | `fraud-investigation`（不正調査） |
| `retail` | Retail | `demand-and-inventory-analysis`（需要・在庫分析） |
| `healthcare` | Healthcare | `case-history-search`（ケース履歴検索） |
| `public-sector` | Public Sector | `case-investigation`（案件調査） |

いずれも同一の `IndustryPackManifest` スキーマに準拠しており、[tests/contract/test_all_industry_packs_manifest_schema.py](../../tests/contract/test_all_industry_packs_manifest_schema.py) と [tests/end-to-end/test_industry_pack_switching.py](../../tests/end-to-end/test_industry_pack_switching.py) で検証済みです。各 Pack が実装しているエンティティ種別は instruction 記載の全種ではなく代表シナリオに必要な最小限のサブセットである点に注意してください（[アーキテクチャガイド §10](../architecture/architecture-guide.md)）。

## 3. プラグインロードアーキテクチャ（概念レベル）

Industry Pack 内の実行可能コード（データ生成・MCP Tool・セマンティクス・シナリオ）は、Python のドット区切りパッケージとして静的にインポートされるのではなく、`iq_platform.orchestration.industry_pack_loader.load_plugin_module()` が `manifest.yaml` に記載されたファイルパスを **実行時に動的ロード** します（[ADR-0010](../decisions/0010-industry-pack-plugin-loading.md)）。これは `industry-packs/` 配下のフォルダ名がケバブケース（例: `financial-services`）であり、Python の `import` 文がハイフンを含む識別子をサポートしないためです。

さらに、[ADR-0011](../decisions/0011-generic-orchestrator-and-semantic-adapter.md) により、`iq_platform/` 側のコード（`GenericLocalOrchestrator`、汎用 Fabric IQ Mock Adapter）は特定業界のロジックを一切含みません。業界固有のロジックはすべて Pack 内のプラグインモジュールが提供する安定インターフェース（`generate_dataset()`、`TOOL_FUNCTIONS`/`TOOL_DESCRIPTIONS`、`get_relationships()`/`get_metrics()`、`run_scenario()`）に委譲されます。この2つの ADR の組み合わせにより、**新しい Industry Pack を追加してもプラットフォームコードを変更する必要がない** という本アクセラレータの中核価値が実現されています。

## 4. 関連ドキュメント

- [Industry-Pack-Guide.md](Industry-Pack-Guide.md) — manifest フィールドリファレンス、新規 Pack 追加チェックリスト、Ontology / Semantic Model / Sample Data / Responsible AI の各執筆ガイド
- [アーキテクチャガイド](../architecture/architecture-guide.md) — レイヤー構成全体における Industry Pack の位置づけ
- [docs/mcp/](../mcp/README.md) — MCP Tool の設計・認証・セキュリティ
- [docs/decisions/assumptions.md](../decisions/assumptions.md) — A11（合成データの現実的な規模に関する前提）
