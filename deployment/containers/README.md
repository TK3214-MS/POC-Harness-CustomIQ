# deployment/containers/

MCP Backend 等のコンテナ構成（Dockerfile、non-root 実行設定等）。

`mcp-backend/Dockerfile`はnon-rootユーザーで実行し、ランタイム依存関係のみをインストールします。実環境またはCIでビルドを検証してください。

ビルドはリポジトリルートから実行する:

```bash
docker build -f deployment/containers/mcp-backend/Dockerfile -t iiq-mcp-backend .
```
