# docs/deployment/

デプロイガイド（azd / Bicep / Terraform、[ADR-0008](../decisions/0008-deployment-tooling-priority.md)）。

**状態: 基礎実装済み。** MCP Backend を Azure Container Apps にデプロイする azd/Bicep 構成を [deployment/azd/](../../deployment/azd/)、[deployment/bicep/](../../deployment/bicep/)、[deployment/containers/](../../deployment/containers/) に実装。設計判断は [ADR-0012](../decisions/0012-mcp-backend-deployment-target.md) を参照。

**実際に Azure へデプロイする手順は [Step-by-Step-Deployment-Guide.md](Step-by-Step-Deployment-Guide.md) にまとめました。** 前提条件・`azd up` の実行手順・デプロイ後の検証・ロールバック(`cleanup`)までを一通り記載しています。

**重要**: Bicep は `az bicep build` でコンパイル検証済み、Docker イメージのビルドは CI([.github/workflows/ci.yml](../../.github/workflows/ci.yml) の `validate-deployment` ジョブ)で検証済みだが、実際の Azure への `azd up` はこのリポジトリの開発環境では未実施(テスト用 Azure サブスクリプションへの接続が必要)。Work IQ / Foundry IQ / Fabric IQ Live Adapter 用のインフラは実装していない(製品 API 仕様が未検証のため、[ADR-0013](../decisions/0013-live-adapter-verification-required-scaffold.md) 参照)。Terraform([deployment/terraform/](../../deployment/terraform/))は README のみで未実装([ADR-0008](../decisions/0008-deployment-tooling-priority.md) の優先順位により最低優先度)。
