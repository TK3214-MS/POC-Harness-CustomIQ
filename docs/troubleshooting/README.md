# トラブルシューティング

## 構築順序

構築順序を飛ばすと、Copilot Studio側で接続できても回答が空になることがあります。まず[本番環境構築ガイド](../Production-Environment-Setup.md)のSaaS側構成を完了し、その後にCopilot Studio Toolを接続してください。

## Fabric IQ

- Ontology itemが作成できない: tenant settingの **Enable Ontology item (preview)**、capacity、workspace権限を確認する。
- インスタンスが空: Lakehouseのmanaged table、entity type key、property binding、Graph model refreshを確認する。
- Copilot StudioからToolが動かない: workspace ID、Ontology ID、ユーザーのFabric権限、接続同意を確認する。

### `Failed to translate NL query to ontology query`

このエラーは、Fabric IQ Toolの呼び出し後、自然言語をOntology queryへ変換する段階で発生する。次の順序で切り分ける。

1. Copilot StudioのFabric IQ Tool詳細で`list_ontology_entity_types`と`search_ontology`が表示されることを確認する。
2. Test paneで「Fabric IQだけを使い、利用可能なentity typeとpropertyを一覧表示してください」と質問する。一覧取得が失敗する場合は、接続先workspace/Ontology ID、接続ユーザーの権限、Ontologyの公開・利用可能状態を確認する。
3. FabricのOntology画面で対象entity typeの**Instances**を開き、実データが表示されることを確認する。表示されない場合はmanaged Lakehouse table、entity type key、property binding、列名、データアクセスを確認する。
4. Graph modelを手動更新し、上流テーブルの追加行が反映されることを確認する。
5. entity type名、property名、relationship名を業務上理解できる名前と説明にする。relationship名はOntology全体で重複させない。
6. 曖昧な質問を避け、最初はentity typeとpropertyを明示する。Manufacturing Packでは「Fabric IQの`QualityIssue`から`issue_id`、`summary`、`severity`、`status`、`detected_at`を5件表示してください」と質問する。
7. 単一entityの検索成功後に、「`QualityIssue`から`affects`で関連する`Part`を取得してください」のようにrelationshipを1つずつ追加する。
8. 「障害」のように複数の意味を持つ語は、品質不具合、設備停止、システム停止、供給障害のどれかを明示する。現在のManufacturing Ontologyで構造化されているのは`QualityIssue`であり、設備・システム停止専用のentity typeはない。
9. Activity traceで、失敗したToolがFabric IQの`search_ontology`であることを確認する。Foundry IQやWork IQが同じ質問で呼ばれなかったことは、各接続の障害を意味しない。
10. 再現する場合は、Activity trace、質問文、workspace/Ontology ID、Correlation ID、Timestamp、schema一覧の成否を保存し、Microsoftサポートへ提示する。アクセストークンや接続シークレットは保存・共有しない。

公式情報:

- [Fabric IQ Ontology MCP](https://learn.microsoft.com/en-us/microsoft-copilot-studio/mcp-fabric-iq-ontology)
- [Ontology troubleshooting](https://learn.microsoft.com/en-us/fabric/iq/ontology/resources-troubleshooting)
- [Entity type creation](https://learn.microsoft.com/en-us/fabric/iq/ontology/how-to-create-entity-types)
- [Ontology data binding](https://learn.microsoft.com/en-us/fabric/iq/ontology/how-to-bind-data)

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
