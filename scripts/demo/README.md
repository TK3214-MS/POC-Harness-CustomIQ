# scripts/demo/

30分セルフガイドデモ用スクリプト（health check、sample data loader、Industry Pack switcher、MCP connectivity test、demo runner、reset、cleanup、synthetic data validation、sensitive information scanner、completion summary generator。instruction §18）。

**状態: ほぼ全て実装済み(Phase 6)。** [run-demo-cli.sh](run-demo-cli.sh) が `apps/demo-cli` の CLI (`health` / `validate` / `load-data` / `select-industry` / `run-demo` / `evaluate` / `generate-summary` / `reset`) をラップして起動します。実行結果は `scripts/demo/output/`(gitignore 対象)に保存されます。Synthetic data validation は [scripts/validation/validate_synthetic_data.py](../validation/validate_synthetic_data.py)、Sensitive information (secret) scanner は [scripts/security/scan_secrets.py](../security/scan_secrets.py) として実装済み。MCP connectivity test は `health` コマンドに含まれる(专用スクリプトは未実装)。`setup` コマンド自体は未実装(venv/pip install で代用)。

使い方の実例は [docs/self-guided-demo/30-Minute-Demo-Guide.md](../../docs/self-guided-demo/30-Minute-Demo-Guide.md) を参照してください。
