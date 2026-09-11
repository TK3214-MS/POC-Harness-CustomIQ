# Microsoft製品検証台帳

この台帳は、Copilot StudioからFabric IQ、Foundry IQ、Work IQへ接続する前提となる公式情報の参照先をまとめます。製品のPreview、価格、ライセンス、リージョン、課金条件は変更されるため、実環境を構成する日付の公式ドキュメントを再確認してください。

| 製品/機能 | 確認済みの接続モデル | 主要な公式ソース | 未確認・要実環境確認 |
|---|---|---|---|
| Copilot Studio GitHub Copilot harness | 本番オーケストレーション層。IQ ToolとMCP Toolを追加する | [Harnesses in Copilot Studio](https://learn.microsoft.com/en-us/microsoft-copilot-studio/harnesses-overview) | Preview/GA、価格・リージョン |
| Fabric IQ / Ontology | Fabric側でOntologyを作成し、Copilot Studioの**Fabric IQ MCP (Preview)**でworkspace IDとOntology IDを指定 | [Create an Ontology Agent with Copilot Studio](https://learn.microsoft.com/en-us/fabric/iq/ontology/how-to-create-agent-copilot-studio) | 実テナントの権限・Preview提供 |
| Foundry IQ | Azure AI SearchのKnowledge SourceとKnowledge Baseを先に作成し、Copilot StudioのFoundry IQ Toolで既存Knowledge Baseを選択 | [Copilot Studio and Azure repository](https://github.com/Azure/Copilot-Studio-and-Azure)、[Create a Knowledge Base](https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-how-to-create-knowledge-base) | 実テナントのRBAC・モデル・リージョン |
| Work IQ | Work IQテナントを有効化し、Copilot Studioの**Tools > Add Tool > Model Context Protocol > Work IQ (preview)**から専用接続を作成 | [Work IQ in Copilot Studio](https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-work-iq) | Preview提供、spending policy、価格・リージョン |
| 本リポジトリ MCP Backend | HTTPSの`/mcp`をCopilot Studioの汎用MCP Toolとして追加 | [MCP server tool](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/tools-add-mcp-server)、[MCP Backend設計](../mcp/MCP-Design-and-Contract-Guide.md) | 実Copilot Studioからの接続、受信認証 |

## 方針

- IQのSaaS接続に本リポジトリのAdapterや`LiveAdapterSettings`は使用しない。
- Fabric、Foundry、Work IQのSaaS側データ・権限・Knowledge/Ontology構成は[本番環境構築ガイド](../Production-Environment-Setup.md)で管理する。
- Microsoft製品の仕様を推測で補完しない。不明な点は `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION` として実環境確認を行う。
