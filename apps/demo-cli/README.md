# apps/demo-cli/

`setup` / `validate` / `health` / `load-data` / `select-industry` / `run-demo` / `evaluate` / `generate-summary` / `reset` / `cleanup`（instruction §28）を提供する CLI。

**状態: 全コマンド実装済み。** `setup` / `health` / `validate` / `load-data` / `select-industry` / `run-demo` / `evaluate` / `generate-summary` / `reset` / `cleanup` の10コマンドすべてが実装済みで、`health` 以下8コマンドは5業界すべてに対応しています。`setup` は [scripts/setup/setup.sh](../../scripts/setup/setup.sh) を、`cleanup` は [scripts/cleanup/cleanup-azure.sh](../../scripts/cleanup/cleanup-azure.sh)（実 Azure リソースの削除。環境名の手入力確認必須。実 azd 環境が存在しない場合は安全に中断する）をそれぞれ呼び出します。

内部の Python パッケージ名は `demo_cli`(このフォルダ名 `demo-cli` はケバブケースのままで問題ない。理由は [ADR-0009](../../docs/decisions/0009-python-package-naming.md) を参照)。`demo_cli` はまだ pip パッケージとしてインストールされないため([ADR-0010](../../docs/decisions/0010-industry-pack-plugin-loading.md) と同様の理由)、実行するには [scripts/demo/run-demo-cli.sh](../../scripts/demo/run-demo-cli.sh) を使うか、`PYTHONPATH` に `apps/demo-cli` と `services/mcp-backend` を追加してください。

```bash
./scripts/demo/run-demo-cli.sh health
./scripts/demo/run-demo-cli.sh validate
./scripts/demo/run-demo-cli.sh select-industry financial-services
./scripts/demo/run-demo-cli.sh load-data --industry retail --scale demo
./scripts/demo/run-demo-cli.sh run-demo --industry healthcare
./scripts/demo/run-demo-cli.sh reset
```
