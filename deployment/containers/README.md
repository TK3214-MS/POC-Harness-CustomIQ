# deployment/containers/

MCP Backend 等のコンテナ構成（Dockerfile、non-root 実行設定等）。

**状態: 実装済み(Phase 5)、ビルド未検証。** [mcp-backend/Dockerfile](mcp-backend/Dockerfile) は non-root ユーザーで実行し、`services/mcp-backend/requirements.txt`(ランタイム専用の固定バージョン依存関係)のみをインストールする。この開発環境に Docker がインストールされていないため `docker build` によるローカル検証は未実施(CI で検証、[ADR-0012](../../docs/decisions/0012-mcp-backend-deployment-target.md))。

ビルドはリポジトリルートから実行する:

```bash
docker build -f deployment/containers/mcp-backend/Dockerfile -t iiq-mcp-backend .
```
