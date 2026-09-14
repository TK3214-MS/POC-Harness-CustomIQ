# セキュリティドキュメント

このページはセキュリティ文書の索引です。一般的なrepository方針と脆弱性報告は[SECURITY.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/SECURITY.md)、MCP Backend固有の管理策は[MCPセキュリティガイド](../mcp/MCP-Security-Guide.md)を正本とします。

Secret scanningは[scan_secrets.py](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/scripts/security/scan_secrets.py)で実装し、CIで実行します。Containerはnon-rootで実行します（[Dockerfile](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/deployment/containers/mcp-backend/Dockerfile)）。基本方針は[SECURITY.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/SECURITY.md)を参照してください。
