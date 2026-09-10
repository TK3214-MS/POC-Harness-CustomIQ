# Fabric IQ Setup（Hybrid/Full SaaS Mode 用、Local Preview では不要）

Local Preview Mode ではこの手順は不要です。`MockSemanticAdapter` + 各 Industry Pack の `semantics/*.py` プラグインが Fabric IQ の代替として動作します。

Hybrid/Full SaaS Mode で実際の Fabric IQ に接続する場合の手順は [docs/setup/live-adapters-configuration.md](../setup/live-adapters-configuration.md) の「Fabric IQ」セクションを参照してください。

現時点の状態: 製品固有の手順は `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`。Fabric IQ、Fabric Data Agent、Fabric IQ Ontology MCP は Capability Registry 上で別機能として扱われています（[ADR-0007](../decisions/0007-capability-registry-authority.md)）。Entra ID アプリ登録 + `FABRIC_WORKSPACE_ID` / `FABRIC_ONTOLOGY_ID` / `FABRIC_IQ_AUTH_SCOPE` の環境変数設定までは実施可能です。

確認コマンド:
```bash
./scripts/demo/run-demo-cli.sh health
```
"Fabric IQ (live)" 行で設定状態を確認できます。
