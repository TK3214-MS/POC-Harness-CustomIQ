# scripts/demo/

30分セルフガイドデモ用スクリプト（health check、sample data loader、Industry Pack switcher、MCP connectivity test、demo runner、reset、cleanup、synthetic data validation、sensitive information scanner、completion summary generator。instruction §18）。

**状態: 全コマンド実装済み。** [run-demo-cli.sh](run-demo-cli.sh) が `apps/demo-cli` の CLI 全10コマンド(`setup` / `health` / `validate` / `load-data` / `select-industry` / `run-demo` / `evaluate` / `generate-summary` / `reset` / `cleanup`)をラップして起動します。実行結果は `scripts/demo/output/`(gitignore 対象)に保存されます。Synthetic data validation は [scripts/validation/validate_synthetic_data.py](../validation/validate_synthetic_data.py)、Sensitive information (secret) scanner は [scripts/security/scan_secrets.py](../security/scan_secrets.py) として実装済み。

MCP connectivity test は2種類あります。

- [test_mcp_connectivity.py](test_mcp_connectivity.py) — MCP Backend の REST API(`/health`/`/tools`/`/tools/{name}/invoke`)を `fastapi.testclient.TestClient` 経由でインプロセス検証。
- [test_mcp_protocol_connectivity.py](test_mcp_protocol_connectivity.py) — 実プロトコル準拠の MCP エンドポイント(`/mcp`)を、実際に起動した `uvicorn` サーバーに対して公式 MCP クライアント SDK(`mcp.client.streamable_http` + `mcp.ClientSession`)で接続し、`initialize`→`tools/list`→`tools/call` を検証(Copilot Studio の「Add MCP server」と同種のハンドシェイク、[ADR-0016](../../docs/decisions/0016-copilot-studio-github-harness-confirmed.md) 参照)。

使い方の実例は [docs/self-guided-demo/30-Minute-Demo-Guide.md](../../docs/self-guided-demo/30-Minute-Demo-Guide.md) を参照してください。
