# docs/deployment/

デプロイガイド（azd / Bicep / Terraform、[ADR-0008](../decisions/0008-deployment-tooling-priority.md)）。

**状態: 基礎実装済み(Phase 5)。** MCP Backend を Azure Container Apps にデプロイする azd/Bicep 構成を [deployment/azd/](../../deployment/azd/)、[deployment/bicep/](../../deployment/bicep/)、[deployment/containers/](../../deployment/containers/) に実装。設計判断は [ADR-0012](../decisions/0012-mcp-backend-deployment-target.md) を参照。

**重要**: Bicep は `az bicep build` でコンパイル検証済みだが、実際の Azure への `azd up` は未実施(テスト用 Azure サブスクリプションの接続情報が必要)。Work IQ / Foundry IQ / Fabric IQ Live Adapter 用のインフラ(Phase 4)は未実装。詳細なガイド化(Setup Guide 形式)は Phase 6 で作成予定。
