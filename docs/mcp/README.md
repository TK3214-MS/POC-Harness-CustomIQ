# MCP Backend ドキュメント インデックス

[![日本語](https://img.shields.io/badge/%E3%81%82-%E6%97%A5%E6%9C%AC%E8%AA%9E-087F8C?style=for-the-badge)](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/docs/mcp/README.md) [![English](https://img.shields.io/badge/A-English-5B6670?style=for-the-badge)](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/docs/mcp/README.en.md)

このフォルダは、`services/mcp-backend/`のMCP Backendに関するドキュメントです。MCP Backendは顧客Business Systemを標準化されたToolとして公開するIntegration Layerであり、FastAPIと公式MCP SDKで実装されています。

## ドキュメント一覧

- [MCP-Design-and-Contract-Guide.md](MCP-Design-and-Contract-Guide.md) — `MCPToolResponse` 契約、`ToolRegistry` の設計、Industry Pack ごとの Tool 宣言方法、`/health`・`/tools`・`/tools/{tool_name}/invoke` エンドポイントの挙動。
- [MCP-Security-Guide.md](MCP-Security-Guide.md) — `MCP_BACKEND_ALLOWED_TOOLS` 許可リスト、非 root コンテナ実行、既定で内部限定の Ingress、未実装のセキュリティ管理策一覧。

## 関連ドキュメント

- [本番環境構築ガイド](../Production-Environment-Setup.md) — Industry Pack ToolをCopilot Studioへ接続する手順
- [トラブルシューティング](../troubleshooting/README.md) — `tools/list`、Tool実行、接続失敗の切り分け
