# 30分デモガイド（Local Preview Mode）

このタイムラインは instruction §19 の標準タイムラインに従います。各コマンドは 2026-09-10 に実際に実行し、動作を確認済みです（[Demo-Completion-Summary.md](Demo-Completion-Summary.md) 参照）。

## 0〜3分: 開始と環境確認

[Environment-Checklist.md](Environment-Checklist.md) を実施済みであることを前提とします。

```bash
./scripts/demo/run-demo-cli.sh health
```

確認項目:
- Local Preview Mode で実行していること（実 Azure/Microsoft SaaS 接続は行わない）
- Industry Pack（既定: Manufacturing）が Ready であること
- 実顧客データが含まれていないこと（[Environment-Checklist.md](Environment-Checklist.md) 参照）

## 3〜7分: Industry Pack 選択

```bash
./scripts/demo/run-demo-cli.sh validate
./scripts/demo/run-demo-cli.sh select-industry manufacturing
```

選択肢: `manufacturing`（既定） / `financial-services` / `retail` / `healthcare` / `public-sector`。詳細は [Industry-Pack-Selection.md](Industry-Pack-Selection.md)。

切り替わる内容: Ontology、Sample Data、Knowledge documents、Work Context fixtures、MCP Tools、Agent scenario ロジック、Demo Prompts、Expected Results、Evaluation Rubrics、Terminology、Responsible AI notices。共通コードは一切変更されません（[ADR-0011](../decisions/0011-generic-orchestrator-and-semantic-adapter.md)）。

## 7〜12分: アーキテクチャ確認

[Architecture-Explained.md](Architecture-Explained.md) を使って各レイヤーを説明してください。要点:

- GitHub Copilot harness の代わりに `GenericLocalOrchestrator` が動く（Local Preview Mode）
- Work IQ / Foundry IQ / Fabric IQ は Mock/Simulated Adapter（Live Adapter は verification_required、[ADR-0013](../decisions/0013-live-adapter-verification-required-scaffold.md)）
- MCP Backend は FastAPI 実装（プロセス内 TestClient 経由で呼び出し、[ADR-0012](../decisions/0012-mcp-backend-deployment-target.md)）
- コストドライバーは未実測（26〜29分のセクション参照）

## 12〜22分: E2E シナリオ実行

```bash
./scripts/demo/run-demo-cli.sh load-data --industry manufacturing --scale demo
./scripts/demo/run-demo-cli.sh run-demo --industry manufacturing
```

表示される内容（実行順）:
1. Mock/Simulation Disclosure
2. Responsible AI Notice
3. Executive Summary
4. Recommended Next Actions
5. Human-in-the-loop Requirements
6. Execution Mode と Trace/Correlation ID
7. `scripts/demo/output/last_run.json` への保存

`last_run.json` を開くと、指示書 §13 の14項目スキーマ（`AgentResponse`）全体を確認できます。デモプロンプトの詳細は [Demo-Prompts.md](Demo-Prompts.md)、期待される結果は [Expected-Results.md](Expected-Results.md) を参照。

## 22〜26分: Industry Pack 切り替え

```bash
./scripts/demo/run-demo-cli.sh select-industry retail
./scripts/demo/run-demo-cli.sh run-demo --industry retail
```

確認する変化:
- エンティティ種別が変わる（例: QualityIssue → DemandSignal）
- Knowledge document・MCP Tool・Responsible AI notice が業界固有の内容に変わる
- `GenericLocalOrchestrator`・`MockKnowledgeAdapter` 等の共通コードは一切変更されていない（[tests/end-to-end/test_industry_pack_switching.py](../../tests/end-to-end/test_industry_pack_switching.py) で自動検証済み）

## 26〜29分: コストとアーキテクチャ

このアクセラレータ自体（MCP Backend、Local Orchestrator）はローカル実行のため実コストは発生しません。実 Azure へのデプロイ時のコストドライバーは [docs/cost/](../cost/)（Phase 6 で拡充予定、現時点では価格を確定値として記載していません。§25 の通り `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`）。

最適化メッセージの例:
- Industry Pack を再利用することで業界ごとの再開発を避けている（このリポジトリ自体が実例）
- MCP Tool は汎用処理（`iq_platform/adapters/`）と業界固有処理（`industry-packs/*/tools/`）に分離済み
- 単純な処理（データ取得等）には Standard harness 相当の軽量な `GenericLocalOrchestrator` を使用（複雑な推論が必要な場面でのみ GitHub Copilot harness 相当の実装を検討）

## 29〜30分: 完了確認

```bash
./scripts/demo/run-demo-cli.sh evaluate --industry manufacturing
./scripts/demo/run-demo-cli.sh generate-summary
```

`evaluate` はそのシナリオの `evaluations/rubric.yaml` に対して自動チェックを実行します(実装範囲は [iq_platform/evaluation/rubric_evaluator.py](../../iq_platform/evaluation/rubric_evaluator.py) を参照、grounding 等一部は弱い代理指標であることを明示)。`generate-summary` は `scripts/demo/output/demo-completion-summary.md` に完了サマリーを生成します。内容は [Demo-Completion-Summary.md](Demo-Completion-Summary.md) を参照。

最後に [Reset-and-Cleanup.md](Reset-and-Cleanup.md) の手順でリセットしてください。
