# Demo Completion Summary（完了サマリーの読み方・生成方法）

## 生成方法

```bash
./scripts/demo/run-demo-cli.sh run-demo --industry <ID>
./scripts/demo/run-demo-cli.sh evaluate --industry <ID>
./scripts/demo/run-demo-cli.sh generate-summary
```

`generate-summary` は直前の `run-demo`（`scripts/demo/output/last_run.json`）と、あれば直前の `evaluate`（`scripts/demo/output/evaluation_result.json`）を読み込み、`scripts/demo/output/demo-completion-summary.md` を生成します（実装: [apps/demo-cli/demo_cli/cli.py](../../apps/demo-cli/demo_cli/cli.py) の `_cmd_generate_summary`）。

## 含まれる項目（instruction §19 準拠）

- Execution Mode / Industry Pack / Executed Prompt（Executive Summary）
- IQ Layers Used / Tools Invoked
- Features Verified / Features Not Verified
- Mock or Simulated Components（開示文そのもの）
- Unfinished Items
- Production Recommendations
- Security Considerations
- （評価結果があれば）Evaluation Rubric Results

## 実例（2026-09-10、Manufacturing、実際に生成）

```markdown
# Demo Completion Summary

- Execution Mode: local_preview
- Industry Pack: Manufacturing (manufacturing)
- Default Scenario: quality-issue-investigation
...
## Features Not Verified

- Live Adapters (Work IQ / Foundry IQ / Fabric IQ / Copilot Studio) - verification_required scaffold only, no real Microsoft product connectivity
- Actual Azure deployment of the MCP Backend ('azd up' not executed against a real subscription)
```

（全文は実際に `generate-summary` を実行して確認してください。ファイル自体は `scripts/demo/output/` に生成され gitignore 対象のため、リポジトリには実行結果そのものはコミットされません。恒久的なサンプルは [docs/architecture/sample-outputs/](../architecture/sample-outputs/) を参照。）

## 保存・共有する場合の注意

`demo-completion-summary.md` を社外・顧客と共有する前に、以下を確認してください。

- `scripts/security/scan_secrets.py` と `scripts/validation/validate_synthetic_data.py` を実行し、問題がないことを確認
- Mock/Simulation の開示と Responsible AI Notice が含まれていることを確認
- 実測していない所要時間・性能を「実測」と書いていないか確認
