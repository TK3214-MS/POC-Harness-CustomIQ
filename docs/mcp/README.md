# MCP Backend ドキュメント インデックス

このフォルダは、本アクセラレータの MCP（Model Context Protocol 相当の内部呼称。実際の MCP プロトコル仕様との対応関係は `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`、[docs/decisions/product-verification.md](../decisions/product-verification.md) 参照）Backend（`services/mcp-backend/`）に関するドキュメントの入口です。MCP Backend は、外部システム・業務データ・業務アクションを標準化された Tool として公開する Integration and Action Layer であり、FastAPI で実装されています（[アーキテクチャガイド §2.3](../architecture/architecture-guide.md)）。

## ドキュメント一覧

- [MCP-Design-and-Contract-Guide.md](MCP-Design-and-Contract-Guide.md) — `MCPToolResponse` 契約、`ToolRegistry` の設計、Industry Pack ごとの Tool 宣言方法、`/health`・`/tools`・`/tools/{tool_name}/invoke` エンドポイントの挙動。
- [MCP-Security-Guide.md](MCP-Security-Guide.md) — `MCP_BACKEND_ALLOWED_TOOLS` 許可リスト、非 root コンテナ実行、既定で内部限定の Ingress、未実装のセキュリティ管理策一覧。

## 関連ドキュメント

- [ADR-0006: MCP Tool response contract](../decisions/0006-mcp-tool-response-contract.md)
- [ADR-0010: Industry Pack はプラグインとして動的ロードする](../decisions/0010-industry-pack-plugin-loading.md)
- [ADR-0012: MCP Backend のデプロイターゲット](../decisions/0012-mcp-backend-deployment-target.md)
- [本番環境構築ガイド](../Production-Environment-Setup.md) — Industry Pack ToolをCopilot Studioへ接続する手順
