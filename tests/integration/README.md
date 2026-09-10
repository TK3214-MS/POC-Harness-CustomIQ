# tests/integration/

Orchestrator ⇄ Adapter、Adapter ⇄ mock data、MCP client ⇄ FastAPI server、Industry Pack 切り替え等の統合テスト（instruction §22.3）。

**状態: 実装済み。** MCP Backend の health/tools/invoke エンドポイント、Industry Pack の動的ロード（generator/tools/semantics/scenario プラグイン）、correlation_id ロギング、human-in-the-loop フローを5業界すべてで検証。
