# Copilot Studio Setup（Hybrid/Full SaaS Mode 用、Local Preview では不要）

Local Preview Mode ではこの手順は不要です。`GenericLocalOrchestrator` が Copilot Studio の代替として動作します。

Hybrid/Full SaaS Mode で実際に Copilot Studio に接続する場合の手順は [docs/setup/live-adapters-configuration.md](../setup/live-adapters-configuration.md) の「Copilot Studio harness」セクションを参照してください（Single Source of Truth、重複記載を避けるためここには詳細を書きません）。

現時点の状態: 製品固有の手順は `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`（[docs/decisions/product-verification.md](../decisions/product-verification.md)）。Entra ID アプリ登録部分のみ実施可能です。

確認コマンド:
```bash
./scripts/demo/run-demo-cli.sh health
```
出力の "Copilot Studio harness" 行で設定状態を確認できます。
