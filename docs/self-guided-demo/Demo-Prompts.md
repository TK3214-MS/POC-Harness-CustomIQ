# Demo Prompts（デモプロンプト一覧）

各業界の `prompts/demo_prompts.yaml` に定義されているプロンプトです。Local Preview Mode では、これらのプロンプトの「意図」を `run-demo` コマンドが実行します（自然言語プロンプトそのものを解釈する自由入力インターフェースは未実装、CLI 引数で対象エンティティを指定する形式です）。

## Manufacturing

- "Investigate the most recent quality issue and recommend next actions."
- 実行: `./scripts/demo/run-demo-cli.sh run-demo --industry manufacturing`
- 特定の issue を指定: `./scripts/demo/run-demo-cli.sh run-demo --industry manufacturing --entity-id QI-00003`

## Financial Services

- "Investigate the most recent fraud case and recommend next steps."
- 実行: `./scripts/demo/run-demo-cli.sh run-demo --industry financial-services`

## Retail

- "Investigate the most recent demand signal and recommend inventory actions."
- 実行: `./scripts/demo/run-demo-cli.sh run-demo --industry retail`

## Healthcare

- "Review the case history for the first synthetic patient and identify any documentation gaps."
- 実行: `./scripts/demo/run-demo-cli.sh run-demo --industry healthcare`
- 診断・治療方法・薬剤を一切推奨しないことを確認してください（[industry-packs/healthcare/responsible-ai/notice.md](../../industry-packs/healthcare/responsible-ai/notice.md)）。

## Public Sector

- "Investigate the most recent case and recommend next review steps."
- 実行: `./scripts/demo/run-demo-cli.sh run-demo --industry public-sector`

## 共通オプション

- `--scale demo|realistic`（既定 `demo`）: `realistic` は数千件規模の合成データを生成します（[docs/decisions/open-questions.md](../decisions/open-questions.md) Q10）。
- `--seed <int>`（既定 `42`）: データ生成の乱数シード。同じ seed なら同じデータセットが再現されます。
- `--entity-id <ID>`: 投資対象のエンティティを明示的に指定（省略時は生成データの先頭エンティティ）。
