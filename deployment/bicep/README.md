# deployment/bicep/

Bicep テンプレート（優先度2位、[ADR-0008](../../docs/decisions/0008-deployment-tooling-priority.md)）。

**状態: 実装済み(Phase 5)。** `main.bicep`(サブスクリプションスコープ、リソースグループ作成)+ `resources.bicep`(Log Analytics、Container Registry、User-Assigned Managed Identity、Container Apps Environment、MCP Backend 用 Container App)。設計判断は [ADR-0012](../../docs/decisions/0012-mcp-backend-deployment-target.md) を参照。

`az bicep build --file deployment/bicep/main.bicep --stdout` でコンパイル検証済み(2026-09-10)。実際のリソースへのデプロイ(`az deployment sub create` 等)は未実施。
