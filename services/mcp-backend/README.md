# services/mcp-backend/

FastAPI で実装する MCP Backend（Integration and Action Layer）。

**状態: 実装済み（Phase 2、Manufacturing のみ）。** `mcp_backend/registry.py`（汎用 `MCPToolResponse` ラッパー）+ `mcp_backend/app.py`（FastAPI アプリ）+ `mcp_backend/factory.py`（Industry Pack の `tools/*.py` を動的ロードしてアプリを組み立てる）。

Local Orchestrator は `fastapi.testclient.TestClient` でこのアプリをプロセス内呼び出しします（実際のネットワーク越し呼び出しは Phase 4/5 で検討）。`services/mcp-backend/run_dev_server.py` で本物の HTTP サーバーとしても起動できます。

内部の Python パッケージ名は `mcp_backend`（このフォルダ名 `mcp-backend` はケバブケースのままで問題ない。理由は [ADR-0009](../../docs/decisions/0009-python-package-naming.md) を参照）。`mcp_backend` はまだ pip パッケージとしてインストールされない（テストは `pyproject.toml` の `pythonpath` 経由で解決する）。

Manufacturing 向けツールは instruction 第11章に対応: `search_quality_issues`, `get_part_traceability`, `get_supplier_history`, `get_factory_context`, `get_engineering_changes`, `recommend_quality_actions`（`industry-packs/manufacturing/tools/manufacturing_tools.py`）。残り業界のツールは Phase 3 で追加します。
