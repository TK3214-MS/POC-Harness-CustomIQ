# tests/security/

Secret scanning、依存関係ピン留め検証、Container security（non-root/HEALTHCHECK/ACR admin無効化）、MCP Tool allowlist、ログのシークレット非漏洩、合成データ検証等（instruction §22.5）。

**状態: 実装済み。** 依存関係の脆弱性スキャン(pip-audit等)とプロンプトインジェクションテストは未実装です。本番投入前にMCP BackendとSaaS側のセキュリティ設定を確認してください。
