# セキュリティドキュメント

[![日本語](https://img.shields.io/badge/%E3%81%82-%E6%97%A5%E6%9C%AC%E8%AA%9E-087F8C?style=for-the-badge)](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/docs/security/README.md) [![English](https://img.shields.io/badge/A-English-5B6670?style=for-the-badge)](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/docs/security/README.en.md)

このページはセキュリティ文書の索引です。一般的なrepository方針と脆弱性報告は[SECURITY.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/SECURITY.md)、MCP Backend固有の管理策は[MCPセキュリティガイド](../mcp/MCP-Security-Guide.md)を正本とします。

Secret scanningは[scan_secrets.py](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/scripts/security/scan_secrets.py)で実装し、CIで実行します。Containerはnon-rootで実行します（[Dockerfile](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/deployment/containers/mcp-backend/Dockerfile)）。基本方針は[SECURITY.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/SECURITY.md)を参照してください。
