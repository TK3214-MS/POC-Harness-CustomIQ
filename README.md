# Industry IQ Platform Accelerator

Fabric IQ、Foundry IQ、Work IQをMicrosoft Copilot StudioのGitHub Copilot harnessから利用する、Industry Pack対応のEnterprise Intelligence Platformアクセラレータです。

## 開始点

ハンズオンで構成を確認する場合は、[Industry IQ Platform Labs](docs/index.md)から開始してください。開発者・アーキテクトが本番構成を確認する場合は、[本番環境構築ガイド](docs/Production-Environment-Setup.md)を参照してください。

このガイドでは、次の順序で環境を構成します。

1. Azure、Fabric、Copilot Studio、Work IQの前提条件と権限を確認
2. Fabric側でLakehouse、managed table、Ontology、entity type、relationship、data bindingを構成
3. Foundry/Azure AI Search側でKnowledge Source、Indexer、Knowledge Base、検索設定を構成
4. Work IQ側でテナント有効化、課金、ポリシー、検証用Microsoft 365データを準備
5. Copilot StudioでFabric IQ MCP、Foundry IQ、Work IQ (preview)を接続
6. 必要な場合だけ、本リポジトリのMCP Backendを業務ツールとして接続

## リポジトリの責務

本リポジトリが提供するものは、Industry Pack、MCP Tool契約、MCP Backend、Azureデプロイ定義、テストです。Fabric IQ、Foundry IQ、Work IQのSaaS側構成と、IQデータの取得は各SaaS管理画面およびCopilot Studioが担当します。

## 開発者向け確認

MCP BackendやIndustry Packを変更した場合:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
ruff check .
pytest tests/
```

MCP BackendのAzureデプロイ定義は [本番環境構築ガイド](docs/Production-Environment-Setup.md) と [Bicep README](deployment/bicep/README.md) を参照してください。

## 設計・検証記録

- [ラボポータル](docs/index.md)
- [本番環境構築ガイド](docs/Production-Environment-Setup.md)
- [実顧客データ向けOntology設計・構築ガイド](docs/Customer-Data-Ontology-Design-Guide.md)
- [IQデモデータ投入・再構成ランブック](docs/evaluation/Demo-Data-Deployment-Runbook.md)
- [Copilot Studio IQレイヤー別テスト質問集](docs/evaluation/Copilot-Studio-IQ-Layer-Test-Catalog.md)
- [トラブルシューティング](docs/troubleshooting/README.md)
- [MCP Backendドキュメント](docs/mcp/README.md)
- [セキュリティポリシー](SECURITY.md)

## ラボサイトのローカル確認

```bash
source .venv/bin/activate
mkdocs serve
```

GitHub Pagesへの公開方法は[公開手順](docs/labs/publishing.md)を参照してください。

## ライセンス

[MIT License](LICENSE)
