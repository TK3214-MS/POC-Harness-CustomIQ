# apps/demo-cli/

`setup` / `validate` / `health` / `load-data` / `select-industry` / `run-demo` / `evaluate` / `generate-summary` / `reset` / `cleanup`（instruction §28）を提供する CLI。

**状態: ほぼ全て実装済み(Phase 6)。** `health` / `validate` / `load-data` / `select-industry` / `run-demo` / `evaluate` / `generate-summary` / `reset` は5業界すべてに対応済み。`setup` / `cleanup`(デプロイ済みリソースの削除)のみ未実装で、実行すると「未実装」であることを明示するメッセージを返します。

内部の Python パッケージ名は `demo_cli`(このフォルダ名 `demo-cli` はケバブケースのままで問題ない。理由は [ADR-0009](../../docs/decisions/0009-python-package-naming.md) を参照)。`demo_cli` はまだ pip パッケージとしてインストールされないため([ADR-0010](../../docs/decisions/0010-industry-pack-plugin-loading.md) と同様の理由)、実行するには [scripts/demo/run-demo-cli.sh](../../scripts/demo/run-demo-cli.sh) を使うか、`PYTHONPATH` に `apps/demo-cli` と `services/mcp-backend` を追加してください。

```bash
./scripts/demo/run-demo-cli.sh health
./scripts/demo/run-demo-cli.sh validate
./scripts/demo/run-demo-cli.sh select-industry financial-services
./scripts/demo/run-demo-cli.sh load-data --industry retail --scale demo
./scripts/demo/run-demo-cli.sh run-demo --industry healthcare
./scripts/demo/run-demo-cli.sh reset
```
