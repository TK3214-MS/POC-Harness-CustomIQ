# deployment/containers/

[![日本語](https://img.shields.io/badge/%E3%81%82-%E6%97%A5%E6%9C%AC%E8%AA%9E-087F8C?style=for-the-badge)](README.md) [![English](https://img.shields.io/badge/A-English-5B6670?style=for-the-badge)](README.en.md)

MCP Backend 等のコンテナ構成（Dockerfile、non-root 実行設定等）。

`mcp-backend/Dockerfile`はnon-rootユーザーで実行し、ランタイム依存関係のみをインストールします。実環境またはCIでビルドを検証してください。

ビルドはリポジトリルートから実行する:

```bash
docker build -f deployment/containers/mcp-backend/Dockerfile -t iiq-mcp-backend .
```
