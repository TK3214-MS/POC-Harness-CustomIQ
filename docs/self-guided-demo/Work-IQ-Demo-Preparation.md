# Work IQ Demo Preparation（Hybrid/Full SaaS Mode 用、Local Preview では不要）

Local Preview Mode ではこの手順は不要です。`SimulatedWorkContextAdapter`（`industry-packs/<ID>/work-context/fixtures.json` を読み込む）が Work IQ の代替として動作します。Simulated Work IQ は実際の Microsoft 365 データへアクセスしません。

Hybrid/Full SaaS Mode で実際の Work IQ に接続する場合の手順は [docs/setup/live-adapters-configuration.md](../setup/live-adapters-configuration.md) の「Work IQ」セクションを参照してください。

現時点の状態: 製品固有の手順は `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`。Entra ID アプリ登録 + `WORK_IQ_WORKSPACE_ID` / `WORK_IQ_AUTH_SCOPE` の環境変数設定までは実施可能です。

確認コマンド:
```bash
./scripts/demo/run-demo-cli.sh health
```
"Work IQ (live)" 行で設定状態を確認できます。
