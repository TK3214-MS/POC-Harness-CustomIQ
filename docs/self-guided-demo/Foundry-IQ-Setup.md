# Foundry IQ Setup（Hybrid/Full SaaS Mode 用、Local Preview では不要）

Local Preview Mode ではこの手順は不要です。`MockKnowledgeAdapter`（`industry-packs/<ID>/knowledge/*.md` を読み込む）が Foundry IQ の代替として動作します。

Hybrid/Full SaaS Mode で実際の Foundry IQ に接続する場合の手順は [docs/setup/live-adapters-configuration.md](../setup/live-adapters-configuration.md) の「Foundry IQ」セクションを参照してください。

現時点の状態: 製品固有の手順は `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`。Entra ID アプリ登録 + `FOUNDRY_IQ_PROJECT_ENDPOINT` / `FOUNDRY_IQ_KNOWLEDGE_BASE_ID` / `FOUNDRY_IQ_AUTH_SCOPE` の環境変数設定までは実施可能です（[.env.example](../../.env.example)）。

確認コマンド:
```bash
./scripts/demo/run-demo-cli.sh health
```
"Foundry IQ (live)" 行で `unavailable` → `verification_required` への遷移を確認できます。
