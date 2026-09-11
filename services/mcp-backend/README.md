# services/mcp-backend/

FastAPI で実装する MCP Backend（Integration and Action Layer）。

**状態: 実装済み。** `mcp_backend/registry.py`（汎用 `MCPToolResponse` ラッパー）+ `mcp_backend/app.py`（FastAPIアプリ）+ `mcp_backend/factory.py`（Industry Packの`tools/*.py`を動的ロードしてアプリを組み立てる）で構成します。

`services/mcp-backend/run_dev_server.py`でサンプルdatasetを使ったHTTPサーバーとして起動できます。Azureデプロイ後はCopilot Studioの汎用MCP Toolから`/mcp`へ接続します。

内部の Python パッケージ名は `mcp_backend`（このフォルダ名 `mcp-backend` はケバブケースのままで問題ない。理由は [ADR-0009](../../docs/decisions/0009-python-package-naming.md) を参照）。`mcp_backend` はまだ pip パッケージとしてインストールされない（テストは `pyproject.toml` の `pythonpath` 経由で解決する）。

5業界のIndustry Packがそれぞれ独自の業務Toolを公開します。Toolの追加は各Packの`manifest.yaml`と`tools/*.py`で行い、Backend本体は変更しません。
