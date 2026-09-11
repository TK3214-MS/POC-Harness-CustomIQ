# トラブルシューティング

## 構築順序

構築順序を飛ばすと、Copilot Studio側で接続できても回答が空になることがあります。まず[本番環境構築ガイド](../Production-Environment-Setup.md)のSaaS側構成を完了し、その後にCopilot Studio Toolを接続してください。

## Fabric IQ

- Ontology itemが作成できない: tenant settingの **Enable Ontology item (preview)**、capacity、workspace権限を確認する。
- インスタンスが空: Lakehouseのmanaged table、entity type key、property binding、Graph model refreshを確認する。
- Copilot StudioからToolが動かない: workspace ID、Ontology ID、ユーザーのFabric権限、接続同意を確認する。

## Foundry IQ

- Knowledge Baseが空: Knowledge Sourceの取り込み状態、Indexer、Index、Storage Blob Data Readerを確認する。
- 回答に引用がない: Knowledge BaseのKnowledge Source、retrieval instructions、answer設定、モデル権限を確認する。
- Copilot Studioで選択できない: Foundry/Azure AI Search側でKnowledge Baseを作成済みか、対象ユーザーにアクセス権があるか確認する。

## Work IQ

- Work IQ (preview)がToolsに表示されない: GitHub Copilot harness、Preview提供、Work IQテナント有効化、Copilot Credits課金、spending policyを確認する。
- データが返らない: テストユーザーがExchange、Teams、SharePoint、OneDriveの対象データを通常のM365権限で参照できるか確認する。
- 書き込みが失敗する: Work IQは読み取り専用が既定。Microsoft 365 admin centerのWork IQ MCP policyとspending policyを確認する。

## MCP Backend

- `tools/list`が失敗する: HTTPS endpoint、`/mcp`パス、ingress、認証、`MCP_BACKEND_ALLOWED_HOSTS`を確認する。
- Toolが表示されない: `MCP_BACKEND_ALLOWED_TOOLS`、Industry Packのmanifest、MCP Backendログを確認する。
- Tool実行が失敗する: Activity trace、MCP Backendのcorrelation ID、Tool入力スキーマ、業務Toolのエラーを確認する。

本リポジトリはSaaS側の管理画面や顧客Business System内部の障害を直接診断しません。各サービスの管理者向けログとActivity traceを確認してください。
