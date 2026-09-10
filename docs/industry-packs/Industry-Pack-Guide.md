# Industry Pack ガイド

このガイドは、既存の Industry Pack を理解する、または新しい Industry Pack（6業界目以降）を追加するための詳細な参照資料です。全体像は [docs/industry-packs/README.md](README.md) を、レイヤー構成全体は [アーキテクチャガイド](../architecture/architecture-guide.md) を参照してください。

## 目次

1. [manifest.yaml フィールドリファレンス](#1-manifestyaml-フィールドリファレンス)
2. [新しい Industry Pack 追加チェックリスト](#2-新しい-industry-pack-追加チェックリスト)
3. [オントロジー設計ガイド](#3-オントロジー設計ガイド)
4. [セマンティックモデルガイド](#4-セマンティックモデルガイド)
5. [サンプルデータガイド](#5-サンプルデータガイド)
6. [Responsible AI ガイド](#6-responsible-ai-ガイド)

---

## 1. manifest.yaml フィールドリファレンス

各 Industry Pack のルートに置く `manifest.yaml` は `iq_platform.contracts.manifest.IndustryPackManifest`（[iq_platform/contracts/manifest.py](../../iq_platform/contracts/manifest.py)）で検証されます。実例として [industry-packs/manufacturing/manifest.yaml](../../industry-packs/manufacturing/manifest.yaml) を参照してください。

| フィールド | 型 | 説明 |
|---|---|---|
| `id` | `str` | Pack の一意な識別子。`industry-packs/` 配下のフォルダ名と一致させる（例: `manufacturing`）。 |
| `display_name` | `str` | 人間可読な表示名（例: `Manufacturing`）。 |
| `version` | `str` | Pack のバージョン文字列。 |
| `description` | `str` | Pack の概要。合成データであることを明記する。 |
| `default_scenario` | `str` | Demo CLI がデフォルトで実行する代表シナリオの識別子。 |
| `ontology_path` | `str` | エンティティ種別・関係性定義ファイルへの相対パス。 |
| `semantic_model_path` | `str` | セマンティックモデル定義ファイルへの相対パス。現行5 Pack では `ontology_path` と同一ファイルを指す簡易実装（Phase 2 由来）だが、将来的な発散を許容するため別フィールドとして分離されている。 |
| `sample_data_path` | `str` | 合成データ生成モジュール（`generate_dataset(seed, scale) -> dict` を実装）への相対パス。 |
| `knowledge_path` | `str` | Knowledge 文書群を格納するディレクトリへの相対パス。 |
| `work_context_path` | `str` | Work Context フィクスチャ（JSON）への相対パス。 |
| `mcp_tools_path` | `str` | MCP Tool 実装モジュール（`TOOL_FUNCTIONS`/`TOOL_DESCRIPTIONS` を公開）への相対パス。 |
| `semantic_relationships_path` | `str` | Fabric IQ Mock Adapter が委譲するセマンティクスプラグイン（`get_relationships`/`get_metrics`）への相対パス（[ADR-0011](../decisions/0011-generic-orchestrator-and-semantic-adapter.md)）。 |
| `scenario_module_path` | `str` | Orchestrator が委譲するシナリオ実行プラグイン（`run_scenario`）への相対パス（[ADR-0011](../decisions/0011-generic-orchestrator-and-semantic-adapter.md)）。 |
| `agent_instructions_path` | `str` | エージェントへの指示文書への相対パス。 |
| `demo_prompts_path` | `str` | デモ用プロンプト集（YAML）への相対パス。 |
| `expected_results_path` | `str` | 代表シナリオの期待結果ドキュメントへの相対パス。 |
| `evaluation_path` | `str` | `iq_platform/evaluation/rubric_evaluator.py` が読み込む評価ルーブリック（`evaluations/rubric.yaml`）への相対パス。 |
| `terminology_path` | `str` | 業界用語集への相対パス。 |
| `responsible_ai_path` | `str` | Responsible AI 通知文（`AgentResponse.responsible_ai_notice` にそのまま反映される）への相対パス。 |
| `prohibited_actions` | `list[str]` | エージェントが自動実行してはならないアクションの一覧。 |
| `human_approval_rules` | `list[HumanApprovalRule]` | `action` / `reason` / `required_approver_role`（任意）からなる、人間承認が必須なアクションの一覧。 |

`prohibited_actions` と `human_approval_rules` は少なくとも一方が非空でなければならず、これは [tests/contract/test_all_industry_packs_manifest_schema.py](../../tests/contract/test_all_industry_packs_manifest_schema.py) の `test_pack_has_at_least_one_prohibited_action_or_approval_rule` で強制されています。

---

## 2. 新しい Industry Pack 追加チェックリスト

新しい6業界目を追加する際、**`iq_platform/` および `services/mcp-backend/` 配下のプラットフォームコードは一切変更してはいけません**（[ADR-0010](../decisions/0010-industry-pack-plugin-loading.md)、[ADR-0011](../decisions/0011-generic-orchestrator-and-semantic-adapter.md)）。これがこのアクセラレータの中核的な価値提案です。以下の順序で作業してください。

1. `industry-packs/<new-pack-id>/` フォルダを作成する（ケバブケース）。
2. [manifest.yaml フィールドリファレンス](#1-manifestyaml-フィールドリファレンス)に従って `manifest.yaml` を作成する。
3. `ontology/` にエンティティ種別・関係性定義を作成する（[§3 オントロジー設計ガイド](#3-オントロジー設計ガイド)参照）。
4. `data/generator.py` に合成データ生成モジュールを実装する（[§5 サンプルデータガイド](#5-サンプルデータガイド)参照）。
5. `tools/<pack>_tools.py` に MCP Tool 実装（`TOOL_FUNCTIONS`/`TOOL_DESCRIPTIONS`）を実装する。
6. `semantics/<pack>_semantics.py` に `get_relationships(dataset, entity_type, entity_id)` と `get_metrics(dataset)` を実装する（[§4 セマンティックモデルガイド](#4-セマンティックモデルガイド)参照）。
7. `agents/scenario.py` に `run_scenario(context, entity_id=None) -> dict` を実装する。
8. `knowledge/`、`work-context/fixtures.json`、`prompts/demo_prompts.yaml`、`expected-results/`、`terminology/glossary.md` を作成する。
9. `evaluations/rubric.yaml` を作成する（評価エンジン `demo-cli evaluate` の入力）。
10. `responsible-ai/notice.md` を作成する（[§6 Responsible AI ガイド](#6-responsible-ai-ガイド)参照）。
11. `agents/investigation_agent_instructions.md`（相当のファイル）にエージェント指示を作成する。
12. `README.md` を Pack 内に作成し、実装したエンティティ種別のサブセットを明記する。
13. `python3 scripts/validation/validate_synthetic_data.py` を実行し、合成データ検証をパスさせる（マージ前必須。[§5 サンプルデータガイド](#5-サンプルデータガイド)参照）。
14. 以下のテストに新しい Pack ID を追加し、パスすることを確認する。
    - [tests/contract/test_all_industry_packs_manifest_schema.py](../../tests/contract/test_all_industry_packs_manifest_schema.py) — manifest スキーマ準拠、宣言された全パスの存在確認、ガードレール非空確認（`ALL_PACK_IDS` リストに新 Pack ID を追加する）。
    - [tests/end-to-end/test_industry_pack_switching.py](../../tests/end-to-end/test_industry_pack_switching.py) — `GenericLocalOrchestrator` 経由での代表シナリオ実行、Pack 切り替え時の状態非漏洩、禁止アクション文言の非混入確認（同様に `ALL_PACK_IDS` に追加する）。
    - [tests/integration/test_mcp_backend_integration.py](../../tests/integration/test_mcp_backend_integration.py) — `/health` / `/tools` / `/tools/{tool_name}/invoke` エンドポイントの疎通確認（同様に `ALL_PACK_IDS` に追加する）。
15. `pytest` をリポジトリ全体で実行し、既存の5業界のテストに影響がないことを確認する。

各ステップの詳細な作法は、既存の5 Pack（特に `industry-packs/manufacturing/`）を実装例として参照してください。

---

## 3. オントロジー設計ガイド

`ontology_path` が指す YAML ファイル（例: [industry-packs/manufacturing/ontology/entities.yaml](../../industry-packs/manufacturing/ontology/entities.yaml)）は、次の2セクションから構成されます。

- `entity_types`: 各エンティティ種別について `name`（型名）、`description`、`identifier_field`（主キー項目名）、`dataset_key`（`generate_dataset()` が返す辞書内でこのエンティティのリストを保持するキー名）、`fields`（保持するフィールド名一覧）を定義する。
- `relationships`: 各関係性について `name`（関係名）、`subject_type`、`object_type`、`description` を定義する。

`dataset_key` は特に重要です。これは合成データ生成モジュール（`generate_dataset()`）が返す辞書のトップレベルキーと、セマンティクスプラグイン（`get_relationships`/`get_metrics`）がデータを参照する際のキーを一致させる規約であり、汎用 Fabric IQ Mock Adapter（`iq_platform/adapters/semantic/mock_adapter.py`）は具体的なエンティティ種別を一切知らず、この規約に従ってプラグインへ委譲するだけです（[ADR-0011](../decisions/0011-generic-orchestrator-and-semantic-adapter.md)）。新しい Pack を設計する際は、代表シナリオの実行に必要な最小限のエンティティ種別のサブセットに絞ることを推奨します（既存5 Pack もすべて instruction 記載の全種ではなくサブセットのみを実装しています）。

---

## 4. セマンティックモデルガイド

`semantic_relationships_path` が指すモジュール（例: [industry-packs/manufacturing/semantics/manufacturing_semantics.py](../../industry-packs/manufacturing/semantics/manufacturing_semantics.py)）は、次の2関数を実装しなければなりません。

```python
def get_relationships(dataset: dict, entity_type: str | None, entity_id: str | None) -> list[dict[str, str]]:
    """entity_type/entity_id に関連するエンティティ間の関係性を
    {"subject": ..., "relationship": ..., "object": ...} の辞書リストとして返す。"""

def get_metrics(dataset: dict) -> dict[str, Any]:
    """データセット全体から算出される業界固有の集計メトリクスを返す。"""
```

これらは Fabric IQ Mock Adapter からそのまま委譲呼び出しされ、`AgentResponse.entities_and_relationships` の元データになります（[ADR-0011](../decisions/0011-generic-orchestrator-and-semantic-adapter.md)）。実装内容自体は Pack ごとに完全に自由ですが、[オントロジー設計ガイド](#3-オントロジー設計ガイド)で定義した `entity_types`/`relationships` と整合させてください。

---

## 5. サンプルデータガイド

`sample_data_path` が指すモジュール（例: [industry-packs/manufacturing/data/generator.py](../../industry-packs/manufacturing/data/generator.py)）は、次の関数を実装しなければなりません（[ADR-0010](../decisions/0010-industry-pack-plugin-loading.md)）。

```python
def generate_dataset(seed: int, scale: str) -> dict:
    """seed に基づき決定的に合成データセットを生成し、
    dataset_key をトップレベルキーとするエンティティリストの辞書を返す。"""
```

**現実的な規模の要件**: [docs/decisions/assumptions.md](../decisions/assumptions.md) の A11 により、主要なエンティティ種別ごとに数千件規模の合成データを生成することが前提とされています（最小限の「数十件」デモセットではありません）。30分デモのシナリオ実行時には、その大規模データセットから関連する小さなサブセットへ絞り込んで表示するため、デモの進行速度には影響しません。

**マージ前必須の検証**: 新しい Pack のデータ生成モジュール・Knowledge 文書・Work Context フィクスチャを追加したら、必ず次のスキャナを実行してください。

```bash
python3 scripts/validation/validate_synthetic_data.py
```

このスクリプト（[scripts/validation/validate_synthetic_data.py](../../scripts/validation/validate_synthetic_data.py)）は、実在企業名の denylist、`example.com`/`example.org`/`example.net` 以外のドメインを持つメールアドレス、電話番号らしきパターン、SSN 様の識別子パターンを `industry-packs/` 配下の `.py`/`.md`/`.json`/`.yaml`/`.yml` ファイルからスキャンします。**これはヒューリスティックなパターンスキャンであり、「完全に合成データである」ことを保証するものではありません。** 手動レビュー（instruction §23 記載のチェックリスト）と組み合わせて使用してください。

---

## 6. Responsible AI ガイド

各 Industry Pack は次の3層で Responsible AI の考慮事項を表現します。

1. **manifest.yaml の `prohibited_actions`**: エージェントが自動実行してはならないアクションの一覧（例: 「品質問題を人間レビューなしに自動クローズする」）。
2. **manifest.yaml の `human_approval_rules`**: `action` / `reason` / `required_approver_role` からなる、人間承認が必須なアクションの一覧。
3. **`responsible_ai_path` が指す文書**（例: [industry-packs/manufacturing/responsible-ai/notice.md](../../industry-packs/manufacturing/responsible-ai/notice.md)）: 業界固有の注意文言（例: 医療業界では「これは診断ではない」、金融業界では「口座を自動凍結しない」）を記載した通知文。この内容は `GenericLocalOrchestrator` によりそのまま読み込まれ、`AgentResponse.responsible_ai_notice` として使われます（[ADR-0011](../decisions/0011-generic-orchestrator-and-semantic-adapter.md)）。

これらに加えて、`iq_platform.contracts.agent_response.AgentResponse`（[ADR-0005](../decisions/0005-agent-response-contract.md)）には次の必須フィールドがあり、**省略した状態でオブジェクトを構築することはできません**（Pydantic の必須フィールド）。

- `human_in_the_loop_requirements`: このシナリオ実行結果に基づき、人間が承認・確認すべき事項の一覧。
- `mock_or_simulation_disclosure`: 実行結果が Mock/Simulated/Live のいずれのモードで得られたかを明示する開示文。
- `responsible_ai_notice`: 上記 `responsible_ai_path` の内容から転記される通知文。

新しい Pack の `agents/scenario.py`（`run_scenario()`）を実装する際は、これら3フィールドに対応する値を必ず返す辞書に含めてください。[tests/end-to-end/test_industry_pack_switching.py](../../tests/end-to-end/test_industry_pack_switching.py) はこれらのフィールドが非空であること、および `mock_or_simulation_disclosure` に `synthetic`/`mock`/`simulated` の各語が含まれることを検証します。
