# Expected Results（実行結果として何が表示されるべきか）

各業界の詳細な期待結果は `industry-packs/<ID>/expected-results/*.md` にあります。ここでは全業界共通で確認すべき項目をまとめます。

## `run-demo` の出力に必ず含まれるべきもの

- **Mock/Simulation Disclosure**: "synthetic" と "mock"/"simulated" の両方の語を含む
- **Responsible AI Notice**: 対象業界の `responsible-ai/notice.md` の内容がそのまま表示される
- **Executive Summary**: 具体的なエンティティID（例: `QI-00001`, `FC-00001`）を含む
- **Recommended Next Actions**: 1件以上、かつ禁止アクション（自動凍結・自動承認・自動診断等）を含まない
- **Human-in-the-loop Requirements**: 1件以上
- **Execution Mode**: `local_preview`
- **Trace/Correlation ID**: UUID形式の一意なID

## `scripts/demo/output/last_run.json` の構造

`iq_platform.contracts.agent_response.AgentResponse`（14項目、instruction §13）に準拠した JSON です。主なフィールド:

```
executive_summary, confirmed_facts, data_sources_used, documents_and_citations,
entities_and_relationships, mcp_tool_results, uncertainty_and_conflicts,
recommended_next_actions, human_in_the_loop_requirements, iq_layers_used,
execution_mode, mock_or_simulation_disclosure, responsible_ai_notice,
trace_or_correlation_id
```

## `evaluate` コマンドの出力

各業界の `evaluations/rubric.yaml` に定義された基準（criteria）ごとに `PASS` / `FAIL` / `MANUAL REVIEW NEEDED` が表示されます。`MANUAL REVIEW NEEDED` は自動チェックが未実装の基準（例: 詳細な grounding 検証）を意味し、失敗ではありません。2026-09-10 時点で5業界すべてが自身のルーブリックに対して全基準 `PASS`（自動チェック対象分）することを確認済みです（[tests/evaluation/test_rubric_evaluator.py](../../tests/evaluation/test_rubric_evaluator.py)）。

## 実在データが含まれていないことの確認

`python3 scripts/validation/validate_synthetic_data.py` が `No denylisted names...` を返すこと。
