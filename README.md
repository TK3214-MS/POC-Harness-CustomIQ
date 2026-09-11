# Industry IQ Platform Accelerator

Fabric IQ、Foundry IQ、Work IQをMicrosoft Copilot StudioのGitHub Copilot harnessから利用する、Industry Pack対応のEnterprise Intelligence Platformアクセラレータです。

## 開始点

開発者・アーキテクトは、まず [本番環境構築ガイド](docs/Production-Environment-Setup.md) を実施してください。

このガイドでは、次の順序で環境を構成します。

1. Azure、Fabric、Copilot Studio、Work IQの前提条件と権限を確認
2. Fabric側でLakehouse、managed table、Ontology、entity type、relationship、data bindingを構成
3. Foundry/Azure AI Search側でKnowledge Source、Indexer、Knowledge Base、検索設定を構成
4. Work IQ側でテナント有効化、課金、ポリシー、検証用Microsoft 365データを準備
5. Copilot StudioでFabric IQ MCP、Foundry IQ、Work IQ (preview)を接続
6. 必要な場合だけ、本リポジトリのMCP Backendを業務ツールとして接続

## リポジトリの責務

本リポジトリが提供するものは、Industry Pack、MCP Tool契約、MCP Backend、Azureデプロイ定義、テストです。Fabric IQ、Foundry IQ、Work IQのSaaS側構成と、IQデータの取得は各SaaS管理画面およびCopilot Studioが担当します。

Local Preview、Mock/Simulated Adapter、ローカルOrchestrator、Demo CLIは本リポジトリの構成対象に含めません。

## 開発者向け確認

MCP BackendやIndustry Packを変更した場合:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
ruff check .
pytest tests/
```

MCP BackendのAzureデプロイ定義は [deployment/README.md](docs/deployment/README.md) を参照してください。

## 設計・検証記録

- [本番環境構築ガイド](docs/Production-Environment-Setup.md)
- [アーキテクチャガイド](docs/architecture/architecture-guide.md)
- [製品検証台帳](docs/decisions/product-verification.md)
- [既知の制限事項](docs/Known-Limitations.md)
- [MCP設計ガイド](docs/mcp/MCP-Design-and-Contract-Guide.md)

## ライセンス

[MIT License](LICENSE)
