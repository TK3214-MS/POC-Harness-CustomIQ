# ADR-0011: Orchestrator と Fabric IQ Mock Adapter を Industry Pack 非依存に汎化する

- ステータス: Accepted
- 日付: 2026-09-10

## コンテキスト

Phase 2 では `iq_platform/orchestration/local_orchestrator.py` に `ManufacturingLocalOrchestrator` を実装したが、これは Manufacturing 業界のエンティティ名・フィールド名・シナリオロジックを直接ハードコードしていた。同様に `iq_platform/adapters/semantic/mock_adapter.py`（Mock Fabric IQ Adapter）の `_get_relationships` は `if entity_type == "QualityIssue"` のような Manufacturing 固有の分岐を含んでいた。

これは指示書 §2 の最重要原則「業界切り替え時に、プラットフォームコードを直接変更してはいけない」に反する。Phase 3 で残り4業界を追加するにあたり、この問題を先送りせず修正する。

## 決定

1. `IndustryPackManifest` に2つのフィールドを追加する（[ADR-0004](0004-industry-pack-manifest-schema.md) の拡張）。
   - `semantic_relationships_path`: Fabric IQ Mock Adapter が委譲する、業界固有のリレーションシップ/メトリクス計算プラグインへのパス。
   - `scenario_module_path`: Orchestrator が委譲する、業界固有のシナリオ実行プラグインへのパス。
   両フィールドとも [ADR-0010](0010-industry-pack-plugin-loading.md) と同様に `importlib` で動的ロードする。
2. `iq_platform/adapters/semantic/mock_adapter.py` から Manufacturing 固有の分岐をすべて削除し、コンストラクタで受け取った `relationships_module`（`get_relationships(dataset, entity_type, entity_id)` と `get_metrics(dataset)` を持つ）に委譲する汎用実装に変更する。
3. `ManufacturingLocalOrchestrator` を削除し、`iq_platform/orchestration/generic_orchestrator.py` の `GenericLocalOrchestrator` に置き換える。`GenericLocalOrchestrator` は次のみを行う。
   - manifest のロード、データセット生成、3つの Adapter の構築、MCP Backend アプリの構築（すべて manifest のパスに基づく汎用処理）。
   - `scenario_module_path` が指すプラグインの `run_scenario(dataset, adapters, invoke_tool, entity_id)` を呼び出す。
   - プラグインが返した内容（executive_summary、confirmed_facts、recommended_next_actions 等）と、`responsible_ai_path` から読み込んだ Responsible AI 通知文、共通の Mock/Simulation 開示文を組み合わせて `AgentResponse` を構築する。
4. `services/mcp-backend/mcp_backend/factory.py` の `build_manufacturing_app` を、`manifest.mcp_tools_path` を読む汎用の `build_app(dataset, pack_dir)` に置き換える。

## 影響

- 新しい Industry Pack を追加する際、`iq_platform/` 配下のコードを一切変更する必要がない（データ生成・MCP Tool・セマンティック関係・シナリオロジックはすべて Pack 内のプラグインとして提供する）。
- `responsible_ai_path` のファイル内容がそのまま `AgentResponse.responsible_ai_notice` として使われるようになり、各業界固有の注意文言（医療は「診断ではない」、金融は「自動凍結ではない」等）を型レベルで強制せずとも自然に反映できる。
- Manufacturing の既存ロジック（`_get_relationships` の分岐、`run_scenario` の実行手順）は `industry-packs/manufacturing/semantics/manufacturing_semantics.py` と `industry-packs/manufacturing/agents/scenario.py` に移動する。
- Contract テスト（`tests/contract/test_manifest_schema.py`）は新フィールドを必須として検証する。
