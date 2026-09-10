# MCP Backend Setup（デモでの起動方法）

## Local Preview Mode（既定、追加作業不要）

`run-demo` / `evaluate` を実行すると、`GenericLocalOrchestrator` が `fastapi.testclient.TestClient` 経由でプロセス内に MCP Backend アプリを組み立てて呼び出します。別プロセスの起動は不要です。

## スタンドアロン HTTP サーバーとして起動する場合（任意、動作確認用）

```bash
PYTHONPATH=".:apps/demo-cli:services/mcp-backend" python3 services/mcp-backend/server.py
```

環境変数（既定値あり）:
- `IIQ_INDUSTRY_PACK`（既定 `manufacturing`）
- `IIQ_DATA_SCALE`（既定 `demo`）
- `IIQ_DATA_SEED`（既定 `42`）
- `PORT`（既定 `8000`）

起動後、別ターミナルから:
```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/tools
```

## コンテナとして起動する場合（Docker が必要、この開発環境では未検証）

```bash
docker build -f deployment/containers/mcp-backend/Dockerfile -t iiq-mcp-backend .
docker run -p 8000:8000 -e IIQ_INDUSTRY_PACK=retail iiq-mcp-backend
```

詳細は [deployment/containers/README.md](../../deployment/containers/README.md) と [ADR-0012](../decisions/0012-mcp-backend-deployment-target.md) を参照してください。
