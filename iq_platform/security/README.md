# iq_platform/security/

MCP Tool allowlist、Tool 入力スキーマ検証、Retrieved content の untrusted 扱い、Human approval ゲート等の横断的セキュリティ機構。

**状態: 一部実装済み（Phase 4）。** `entra_auth.py` が `azure-identity` の `ClientSecretCredential` を使った実 Entra ID 認証を実装（Live Adapter が使用）。MCP Tool allowlist 等の他の機構は未実装（Phase 2〜以降で段階的に実装予定）。
