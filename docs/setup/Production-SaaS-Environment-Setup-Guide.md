# Fabric IQ / Foundry IQ / Work IQ 本番接続環境構築ガイド

> **状態**: このガイドは 2026-09-10 に実在する Microsoft 公式ドキュメント(Microsoft Learn)を直接調査して作成したものです。各手順には出典 URL を明記しています。**このリポジトリの開発環境では実際にこの手順を最後まで実行した実績はありません**(実 Azure/Microsoft 365 テナントへのアクセスがないため)。手順通りに進めても想定外の挙動に遭遇した場合は、本ガイドを実測結果で更新してください。
>
> **対象読者**: [docs/deployment/Step-by-Step-Deployment-Guide.md](../deployment/Step-by-Step-Deployment-Guide.md) のステップ6〜11(Entra ID 登録・Work IQ/Foundry IQ/Fabric IQ 設定・Copilot Studio harness 設定)を終えた後、実際に Fabric IQ・Foundry IQ・Work IQ を**実データで動作する状態**まで構築したい開発者・管理者。
>
> **前提**: オーケストレーション層は Microsoft Copilot Studio の GitHub Copilot Harness です([ADR-0014](../decisions/0014-local-orchestrator-is-not-a-harness-replacement.md)、[ADR-0016](../decisions/0016-copilot-studio-github-harness-confirmed.md))。Foundry IQ・Fabric IQ は Copilot Studio に**一次機能(Tool)として直接接続**します。Work IQ は **MCP(Model Context Protocol)をプロトコルとして公式にサポート**しており([Microsoft Work IQ API](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/work-iq/api-overview) — A2A・Local MCP・Remote MCP・REST の4プロトコルに対応)、Copilot Studio は汎用の「Add MCP server」フローで任意の MCP サーバーを追加できるため、原理上は Work IQ の Remote MCP サーバーを直接 Tool として追加できる可能性があります。ただし **Copilot Studio 向けの具体的な Remote MCP 接続エンドポイント URL・認証設定手順は本調査では確認できていません**(未確認、断定しません)。確認できている経路は、Foundry IQ の Knowledge Base に Work IQ Knowledge Source として組み込む間接接続です(詳細は Part C)。

## 0. 全体像

```mermaid
flowchart TB
    User["利用者"] --> Agent["Copilot Studio エージェント<br/>(GitHub Copilot Harness)"]
    Agent -- "Tool: Foundry IQ" --> KB["Azure AI Search<br/>Knowledge Base"]
    Agent -- "Tool: Fabric IQ" --> Fab["Fabric IQ アイテム<br/>(Ontology / Data Agent / semantic model)"]
    KB -- "Knowledge Source" --> Blob["サンプルデータ<br/>(Blob Storage)"]
    KB -- "Knowledge Source (任意)" --> WorkIQKS["Work IQ Knowledge Source"]
    WorkIQKS -- "OBO トークン" --> WorkIQ["Work IQ<br/>(Microsoft 365 データ)"]
    Fab -- "データバインド" --> Lakehouse["Fabric Lakehouse<br/>(サンプルデータ)"]
    Agent -- "Tool: MCP server" --> MCPBackend["本リポジトリの MCP Backend<br/>(/mcp)"]
```

この図は本ガイドの手順が構築する構成の要約です。個々の矢印の詳細と出典は各 Part を参照してください。

## 1. 全体の前提条件チェックリスト

| # | 項目 | 出典 |
|---|---|---|
| 1 | Azure サブスクリプション(Foundry / Azure AI Search / Storage 用) | 各 Part 参照 |
| 2 | Microsoft Fabric が有効な容量(F2 以上、または Fabric 有効化済み Power BI Premium P1 以上) | [Fabric data agent 前提条件](https://learn.microsoft.com/en-us/fabric/data-science/how-to-create-data-agent) |
| 3 | Microsoft Copilot Studio の使用量ベース課金プラン(Azure サブスクリプション + リソースグループを割り当て済み) | [Work IQ を有効化する](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/work-iq/enable-work-iq) |
| 4 | Microsoft Entra ID Global Administrator ロール(Work IQ 有効化・管理者同意用、一時的な PIM 昇格を推奨) | 同上、および [Fabric IQ 認証設定](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/fabric-iq) |
| 5 | Azure AI Search サービス(agentic retrieval 対応リージョン) | [Foundry IQ Knowledge Base 作成](https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-how-to-create-knowledge-base) |
| 6 | (LLM を使う場合)Azure OpenAI in Foundry Models のモデルデプロイ | 同上 |

**コストに関する注記**: このガイドで作成するリソース(Azure AI Search、Fabric 容量、Azure OpenAI 等)には課金が発生します。金額は本ガイドでは一切確定しません。[docs/cost/README.md](../cost/README.md) の方針に従い、実行前に Azure Pricing Calculator 等で見積もりを確認し、`docs/decisions/product-verification.md` にその結果を追記してください。

---

## Part A: Fabric IQ(Ontology / Fabric Data Agent)の構築

### A-1. Fabric ワークスペースの準備

Fabric IQ の Ontology(プレビュー)アイテムを使うには、Fabric ワークスペースにテナント設定「Ontology item (preview)」が有効になっている必要があります([Bind Data 前提条件](https://learn.microsoft.com/en-us/fabric/iq/ontology/how-to-bind-data) より、詳細な有効化手順は `overview-tenant-settings#ontology-item-preview` を参照 — このリポジトリでは未確認、Fabric 管理センターで確認してください)。

### A-2. Lakehouse の作成とサンプルデータの投入

1. Fabric ワークスペースを開き、**+ New item** → **Lakehouse** を選択します。名前はアルファベットで始まり、英数字とアンダースコアのみ(123文字以内)。([Create a lakehouse](https://learn.microsoft.com/en-us/fabric/data-engineering/create-lakehouse))
2. サンプルデータの投入方法(いずれか):
   - **パイプラインでのコピー**: **+ New item** → **Pipeline** → **Copy data** アクティビティで、任意のソース(Azure Blob 等)から Lakehouse の `Files` 配下にコピーします。([Lakehouse tutorial - Ingest data](https://learn.microsoft.com/en-us/fabric/data-engineering/tutorial-lakehouse-data-ingestion) — このチュートリアルは Microsoft 提供の公開サンプルデータ `https://fabrictutorialdata.blob.core.windows.net/sampledata/`(Wide World Importers)を使う例で、匿名認証で接続可能です。本リポジトリの合成データ(`industry-packs/*/sample-data/` 生成物)を使う場合は、まず任意の Blob Storage コンテナーにアップロードしてから同様にコピーしてください)。
   - **直接アップロード**: Lakehouse Explorer の **Files** に直接ファイルをアップロードし、テーブルとして読み込む方法もあります(具体的なクリック手順は [Load data into a lakehouse](https://learn.microsoft.com/en-us/fabric/data-engineering/load-data-lakehouse) を参照 — このリポジトリでは未確認、`TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`)。
3. Ontology のデータバインドは **managed** な Lakehouse テーブル(OneLake セキュリティ無効・列マッピング無効)のみサポートされるため([Bind Data の制限事項](https://learn.microsoft.com/en-us/fabric/iq/ontology/how-to-bind-data#limitations-and-troubleshooting))、生ファイルのままではなく **テーブルとして読み込む** 必要があります。

### A-3. Ontology(プレビュー)アイテムの作成とエンティティ型の定義

**確認できた事実**: Ontology アイテムは *entity types*(実体の型、例: Product・Order)・*properties*(プロパティ)・*relationships*(関係)・*data binding*(データ結合)から構成されます([What Is Ontology (Preview)?](https://learn.microsoft.com/en-us/fabric/iq/ontology/overview))。

**Ontology アイテムの新規作成(前提設定含む)**:

1. Fabric 管理者は、管理ポータルの [テナント設定](https://learn.microsoft.com/en-us/fabric/iq/ontology/overview-tenant-settings) で **Enable Ontology item (preview)** を有効化する(未設定の場合、新規 Ontology アイテム作成時にエラーになります)。Fabric Data Agent と組み合わせる場合は [Fabric data agent のテナント設定](https://learn.microsoft.com/en-us/fabric/data-science/data-agent-tenant-settings) も併せて有効化してください。
2. Fabric ワークスペースを開き、**+ New item** から Ontology アイテムを作成する。

   > `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`: **+ New item** ギャラリー内の正確な項目名・アイコン表記までは、Ontology 専用の作成手順ページ(quickstart 相当)が本調査では見つからなかったため確認できていません(`fabric/iq/ontology/quickstart` は404)。ただし、Lakehouse 等の他の Fabric アイテムと同じ **+ New item** ギャラリーの作成パターンに従うことは、[Create Entity Types](https://learn.microsoft.com/en-us/fabric/iq/ontology/how-to-create-entity-types) の前提条件(「An ontology (preview) item.」がエンティティ型作成の前提として記載)から強く示唆されます。実際の Fabric ポータルで確認してください。

**エンティティ型の作成**(確認済み、[Create Entity Types](https://learn.microsoft.com/en-us/fabric/iq/ontology/how-to-create-entity-types)):

1. Ontology アイテムの Home 設定キャンバスで、トップリボンまたはキャンバス中央の **Add entity type** を選択。
2. エンティティ型名を入力し(1〜26文字、英数字・ハイフン・アンダースコアのみ、先頭/末尾は英数字)、**Add Entity Type** を選択。キャンバスに新しいエンティティ型が表示されます。
3. **プロパティの追加**(データバインドと同時でも、事前でも可): エンティティ型名を選択 → 上部リボンの **View entity type details** → **Configure** タブ → **Manage property bindings** を展開 → **Add properties** を選択。各プロパティに名前と型(または型を指定せず `Define at binding` を選び、データバインド時に型を確定する「型なしプロパティ」)を設定して **Save**。
   - プロパティ名は同一エンティティ型内で重複不可・1〜26文字の制約あり。異なるエンティティ型間では同名でも型が同じなら重複可。
4. 必要に応じて、いずれかのプロパティを **display name property**(下流の表示名)として指定。
5. エンティティ型の削除は Explorer 上で **... > Delete entity type** から行う(関連する entity type key・relationship type の設定も連動して削除される点に注意)。

データバインドの手順(確認済み、[Bind Data](https://learn.microsoft.com/en-us/fabric/iq/ontology/how-to-bind-data)):

1. Ontology の Home 設定キャンバスまたは entity type の **Configure** タブから **Bind data** を選択。
2. **Add data binding** で OneLake のデータソース種別を選び、対象テーブルを選択。
3. **Entity type key**(一意キーとなる列)と **Properties**(列→プロパティのマッピング)を設定して保存(静的データバインド)。
4. 必要に応じて時系列データ(Eventhouse または Lakehouse)を追加バインド(静的バインド完了後のみ可能)。
5. 上流データの更新はグラフモデルへ自動反映されないため、[refresh the graph model](https://learn.microsoft.com/en-us/fabric/iq/ontology/how-to-view-entity-type-details) の手順で手動更新が必要です。

サポートされるプロパティ型・制限事項(managed テーブルのみ、1エンティティ型につき静的バインドは1ソースのみ 等)は上記ページの表を参照してください。

### A-4. (任意)Fabric Data Agent の作成

Ontology の代わり、または加えて、会話型 Q&A を提供する Fabric Data Agent を作成できます([Create a Fabric data agent](https://learn.microsoft.com/en-us/fabric/data-science/how-to-create-data-agent)、[概念ページ](https://learn.microsoft.com/en-us/fabric/data-science/concept-data-agent))。

1. ワークスペースで **+ New Item** → **Fabric data agent** を選択し、名前を入力。
2. データソースを最大5個(組み合わせ自由: Lakehouse・Warehouse・Power BI semantic model・KQL データベース・Ontology・Microsoft Graph)追加し、使用するテーブルを選択。
3. **Data agent instructions**(最大15,000文字)と **Example queries** で挙動を調整(任意)。
4. **Publish** で公開。公開時に入力する説明文は、外部オーケストレーター(Copilot Studio 等)がこの Data Agent をいつ呼び出すべきか判断する材料になります。
5. 認証は不要(Fabric がユーザーの Entra ID 資格情報とワークスペース権限で動作、Microsoft 管理の Azure OpenAI Assistant を使用)。読み取り専用(SQL/DAX/KQL の生成・実行はすべて読み取りクエリのみ)。

**ガバナンス**: Microsoft Purview の DLP・アクセス制限ポリシーが設定されている場合、Fabric Data Agent はそのポリシーに従います([Governance and security](https://learn.microsoft.com/en-us/fabric/data-science/concept-data-agent#governance-and-security))。

### A-5. Copilot Studio エージェントへの Fabric IQ 接続

確認済み手順([Connect to Fabric IQ from an agent (preview) - Microsoft Copilot Studio](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/fabric-iq-connect)):

1. Copilot Studio でエージェントを開き、**Build** タブ → **+ Add tool** を選択。
2. **Fabric IQ** を選択し、Tool 追加の標準フローに従う(接続対象の Fabric ワークスペース・アイテムへのアクセス権限が前提)。
3. **Save**。

**未確認の詳細**: この Copilot Studio ネイティブフローにおける具体的な認証プロンプト(サインイン画面の内容等)は、Copilot Studio 側のドキュメントには詳述されていません。[Azure Foundry Agent Service 経由での接続ページ](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/fabric-iq#authentication-and-security)には、Ontology 用に「Entra アプリ登録(委任 `Item.Execute.All`/`Item.Read.All` 権限、または Data Agent 用 `DataAgent.Execute.All`)+ 管理者の同意」という詳細な手順がありますが、**これは Foundry Agent Service(Azure AI Foundry のエージェントホスト)向けの手順であり、Copilot Studio のネイティブ Tool 追加フローと同一かどうかは確認できていません**。実際に接続する際は、Copilot Studio の画面上の指示に従ってください。

---

## Part B: Foundry IQ(Azure AI Search Knowledge Base)の構築

### B-1. 前提条件

- Agentic retrieval に対応するリージョンの Azure AI Search サービス(managed identity を使う場合は Basic 以上のティア)。
- Knowledge Source の種類によっては Azure OpenAI in Foundry Models のモデルデプロイが必要(LLM を使う answer synthesis 等)。
- ロール: **Search Service Contributor**(Knowledge Base/Source 作成用)、LLM を使う場合は検索サービスのマネージド ID に **Cognitive Services User**(Foundry リソース側)。
([Create a Knowledge Base](https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-how-to-create-knowledge-base))

### B-2. サンプルデータの投入(Blob Knowledge Source、推奨)

合成データ(このリポジトリの `industry-packs/*/knowledge/*.md` 等)を最も簡単に投入する方法は **Blob Knowledge Source** です([Create a Blob Knowledge Source](https://learn.microsoft.com/en-us/azure/search/agentic-knowledge-source-how-to-blob)):

1. Azure Blob Storage アカウント・コンテナーを作成し、サンプルデータファイル(対応形式は [blob indexer のドキュメント](https://learn.microsoft.com/en-us/azure/search/search-how-to-index-azure-blob-storage#supported-document-formats)参照)をアップロードする。
2. Azure AI Search の管理 ID に、対象ストレージアカウントで **Storage Blob Data Reader** ロールを付与する。
3. `AzureBlobKnowledgeSource` を作成する(REST 例):

   ```http
   PUT {{search-endpoint}}/knowledgesources/my-blob-ks?api-version=2026-04-01
   Authorization: Bearer {{search-access-token}}
   Content-Type: application/json

   {
     "name": "my-blob-ks",
     "kind": "azureBlob",
     "description": "合成サンプルデータのナレッジソース",
     "azureBlobParameters": {
       "connectionString": "ResourceId=<storage-resource-id>",
       "containerName": "<blob-container-name>",
       "isADLSGen2": false,
       "ingestionParameters": {
         "chatCompletionModel": { "kind": "azureOpenAI", "azureOpenAIParameters": { "resourceUri": "{{aoai-endpoint}}", "deploymentId": "{{aoai-gpt-deployment}}", "modelName": "{{aoai-gpt-model}}" } },
         "embeddingModel": { "kind": "azureOpenAI", "azureOpenAIParameters": { "resourceUri": "{{aoai-endpoint}}", "deploymentId": "{{aoai-embedding-deployment}}", "modelName": "{{aoai-embedding-model}}" } }
       }
     }
   }
   ```

   これにより、データソース・スキルセット(チャンク化・ベクトル化)・インデックス・インデクサーが自動生成されます。作成後、`GET {{search-endpoint}}/knowledgesources/my-blob-ks/status` で取り込み状況(`itemUpdatesProcessed`/`itemsUpdatesFailed`)を確認できます。

他の Knowledge Source 種別(Azure SQL・File・OneLake・SharePoint・Fabric Data Agent・Fabric Ontology・MCP server・Web)も同じ仕組みでサポートされています([What is a Knowledge Source?](https://learn.microsoft.com/en-us/azure/search/agentic-knowledge-source-overview) の一覧表参照)。**Fabric Data Agent / Fabric Ontology を Knowledge Source として Foundry IQ に取り込むことも可能**です(Part A で作成したアイテムをここに接続する代替経路)。

### B-3. Knowledge Base の作成

```http
PUT {{search-endpoint}}/knowledgebases/my-kb?api-version=2026-04-01
Authorization: Bearer {{search-access-token}}
Content-Type: application/json

{
    "name" : "my-kb",
    "description": "Industry IQ Platform Accelerator 用ナレッジベース",
    "knowledgeSources": [ { "name": "my-blob-ks" } ],
    "encryptionKey": null
}
```

([Create a Knowledge Base](https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-how-to-create-knowledge-base)。`2026-04-01` は一般提供(GA)版 REST API。プレビュー機能(query planning・answer synthesis 等)が必要な場合は `2026-08-01-preview` を使用)

### B-4. Copilot Studio エージェントへの Foundry IQ 接続

確認済み手順([Connect to Foundry IQ from an agent - Microsoft Copilot Studio](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/foundry-iq-connect)):

1. Copilot Studio でエージェントを開き、**Build** タブ → コンポーネントパネルの **Tools** → **Foundry IQ** を選択。
2. **Create new connection** を選び、**Authentication type** を選択(**API key** / **Client Certificate Auth** / **Service principal (Microsoft Entra ID application)** / **Microsoft Entra ID Integrated** のいずれか)。
   - API Key の場合: Azure AI Search サービスのエンドポイント + API キーを入力。
   - Service principal の場合: エンドポイント + テナント ID + クライアント ID + クライアントシークレットを入力。
3. 接続作成後、**Knowledge Base**(B-3で作成したもの)を選択し、**Add to agent**。
4. **Save**。Tool の名前・説明を分かりやすく編集する(説明文がオーケストレーションの精度に影響)。
5. **Preview** タブでテスト質問を送り、Activity trace で Foundry IQ の取得ステップが記録されていることを確認する。

**注意**: 1エージェントにつき Foundry IQ 接続は1つのみです。複数の Knowledge Base を使い分けたい場合は、Knowledge Base 側で複数の Knowledge Source を束ねる設計にしてください。

---

## Part C: Work IQ の有効化と Copilot Studio 接続

### C-1. テナントの Work IQ 有効化(一度きり)

前提([Enable your tenant for Work IQ](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/work-iq/enable-work-iq)):

- Copilot Studio に Azure サブスクリプション・リソースグループを割り当てた使用量ベース課金プランが設定済み。
- Global Administrator ロールを持つユーザー(一度きりのテナント設定)。

有効化手順(いずれか、所要時間約5分・組織につき一度きり):

- **Graph Explorer**: POST `https://graph.microsoft.com/v1.0/servicePrincipals`、リクエストボディ `{"appId": "fdcc1f02-fc51-4226-8753-f668596af7f7"}`。`201 Created` で成功、既存なら競合エラー。
- **Azure CLI**: `az ad sp create --id fdcc1f02-fc51-4226-8753-f668596af7f7`

### C-2. Work IQ MCP サーバー(確認済み: Work IQ 自体が MCP を公式サポート)

**確認できた事実**([Microsoft Work IQ API](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/work-iq/api-overview)、[Work IQ MCP overview](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/work-iq/mcp/overview)、[Work IQ MCP tool reference](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/work-iq/mcp/tool-reference)):

- Work IQ は **Local MCP** と **Remote MCP** の2種類の MCP プロトコルを公式サポートしています(A2A・REST と合わせて計4プロトコル)。
- MCP サーバーは 10個の汎用ツール(`fetch`/`fetch_blob`/`create_entity`/`update_entity`/`delete_entity`/`do_action`/`call_function`/`ask`/`list_agents`/`get_schema`/`search_paths`)を公開し、相対リソースパス(例: `fetch /me/messages`)でツールの対象を指定します。新しいワークロードが追加されてもツール数(10個)は変わらず、パスが増える設計です。
- 認証は Microsoft Entra ID の委任認証のみ(アプリケーション専用認証は非サポート)。MCP クライアントは `/.well-known/oauth-protected-resource` エンドポイントで認証設定を自動検出します。
- **既定では書き込み系操作(create/update/delete/action)はテナントポリシーでブロックされています**。管理者が Microsoft 365 管理センターの **Agents > Tools > Work IQ MCP > Policy** タブで明示的に許可する必要があります([Policy governance for Work IQ MCP](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/work-iq/mcp/policy-governance-mcp))。
- **Local MCP** はローカル開発環境(IDE・CLI)向けで、[Work IQ CLI](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/work-iq/api-overview) をインストールし、以下のように stdio 型 MCP サーバーとして設定します:

  ```json
  {
    "workiq": {
      "type": "stdio",
      "command": "workiq",
      "args": ["mcp"]
    }
  }
  ```

**未確認の事項(断定しません)**: **Remote MCP** サーバーの実際の接続エンドポイント URL、および Copilot Studio の汎用「Add MCP server」フロー(Server URL + Authentication を入力する画面、[Add a Model Context Protocol (MCP) server to your agent as a tool (preview)](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/tools-add-mcp-server))で Work IQ の Remote MCP サーバーを直接追加できるかどうかの具体的な手順は、本調査で参照した公式ページには明記されていませんでした。Copilot Studio がこの汎用フローで任意の MCP サーバーを追加できる以上、原理上は可能と考えられますが、`TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION` として、実際の Copilot Studio 画面・Work IQ 管理者向けドキュメントで確認してください。

### C-3. Foundry IQ Knowledge Base に Work IQ を組み込む(確認済みの代替経路)

**Work IQ は Azure AI Search の Knowledge Source の1種類としても明確にサポートされています**([What is a Knowledge Source?](https://learn.microsoft.com/en-us/azure/search/agentic-knowledge-source-overview) の一覧表、[Create a Work IQ Knowledge Source](https://learn.microsoft.com/en-us/azure/search/agentic-knowledge-source-how-to-work-iq))。C-2 の Remote MCP 経路の Copilot Studio 対応が未確認である一方、この経路は Foundry IQ の Knowledge Base 経由での間接接続として確認できています。Part B で作成した Foundry IQ の Knowledge Base に Work IQ Knowledge Source を追加すれば、Copilot Studio の「Foundry IQ」Tool 経由で間接的に Work IQ のデータにも到達できる可能性があります(**この間接経路の実際の動作は本リポジトリでは未検証**、C-4 参照)。

手順(`2026-08-01-preview` API 版が必要、GA 版では未対応):

1. **カスタム所有の Entra アプリ登録**を作成(サポート対象アカウント種別: 自組織のみ)。
2. アプリの **Expose an API** で、**厳密に `access_as_user`** という名前の委任スコープを追加(他の名前不可)。
3. アプリの **API permissions** で「APIs my organization uses」から Work IQ(アプリケーション ID `fdcc1f02-fc51-4226-8753-f668596af7f7`)を検索し、**Delegated permissions** → **WorkIQAgent.Ask** を追加。
4. 管理者が **Grant admin consent** を実行。
5. Azure AI Search サービスに **system-assigned managed identity** を有効化し、その **Object (principal) ID** とテナント ID を控える。
6. `credential.json` を作成し、federated credential を Azure CLI で作成:
   ```json
   {
     "name": "<search-service-name>-identity",
     "issuer": "https://login.microsoftonline.com/<search-service-tenant-id>/v2.0",
     "subject": "<search-service-principal-id>",
     "audiences": ["api://AzureADTokenExchange"]
   }
   ```
   ```bash
   az login --tenant <app-tenant-id> --allow-no-subscriptions
   az ad app federated-credential create --id <application-client-id> --parameters credential.json --query id --output tsv
   ```
7. クライアントアプリ(利用者にサインインさせるアプリ)にも、Work IQ アプリの `access_as_user` 権限を追加・同意させる。
8. Work IQ Knowledge Source を作成:
   ```http
   PUT {{search-endpoint}}/knowledgesources/my-workiq-ks?api-version=2026-08-01-preview
   Authorization: Bearer {{search-access-token}}
   Content-Type: application/json

   {
     "name": "my-workiq-ks",
     "kind": "workIQ",
     "workIQParameters": {
       "entraAppAuthentication": {
         "applicationId": "<application-client-id>",
         "federatedCredentialId": "<federated-credential-id>"
       }
     }
   }
   ```
9. Knowledge Base(B-3)にこの Knowledge Source を追加する。
10. クエリ時は、`x-ms-query-work-iq-source-authorization` ヘッダーにサインイン中ユーザーのアサーション(`api://<application-client-id>/access_as_user` スコープの MSAL PKCE トークン)を渡す必要がある(通常の `x-ms-query-source-authorization` とは別ヘッダー)。**Work IQ の応答には40〜60秒以上かかることがあるため、`maxRuntimeInSeconds` を120以上に設定すること。**

### C-4. 未確認事項(断定しないこと)

- Work IQ の Remote MCP サーバーを Copilot Studio の汎用「Add MCP server」フローで直接追加できるかどうか、その際の接続エンドポイント URL・認証設定の具体的な手順は **未確認** です(C-2 参照)。
- Copilot Studio の「Foundry IQ」ネイティブ Tool 接続が、Work IQ Knowledge Source 経由の場合に必要となる固有ヘッダー(`x-ms-query-work-iq-source-authorization`)を自動的に転送するかどうかは **未確認** です。Copilot Studio 側のドキュメントにこの詳細は記載されていません。実際に構築した際は、Activity trace で Work IQ からの応答が実際に返っているかを確認してください。
- Work IQ 自体がデータ取得だけでなくアクション実行も行いうる(プレビュー機能・既定でブロック)ため、信頼できるアプリケーション・利用者に限定し、権限・ガバナンス設定(C-2 のポリシー層、[Create a Work IQ Knowledge Source](https://learn.microsoft.com/en-us/azure/search/agentic-knowledge-source-how-to-work-iq) の Warning)を事前にレビューしてください。
- データガバナンス: Work IQ はリクエストごとに Microsoft 365 の権限を適用し、署名したユーザーがアクセス可能な組織データのみを返します。プロンプト・応答・Microsoft Graph 経由でアクセスしたデータは基盤言語モデルの学習に使用されません。

---

## Part D: Copilot Studio エージェントの作成

1. Copilot Studio ホームページで、テキストボックスに自然言語で作りたいものを記述するか、**Other ways to build** から選択してエージェントを作成する([Start building](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/authoring-first-bot))。ホームページのカードから作成したエージェントは既定で GitHub Copilot Harness で動作します。
2. Part A/B/C で構築した Tool(Fabric IQ・Foundry IQ)を **Build** タブから追加する。
3. 本リポジトリの MCP Backend を Tool として追加する手順は [docs/deployment/Step-by-Step-Deployment-Guide.md](../deployment/Step-by-Step-Deployment-Guide.md) の11.1を参照(実 MCP プロトコル準拠サーバー実装済み)。
4. エージェントの指示(instructions)は、各 Industry Pack の `agent_instructions_path`(例: [industry-packs/manufacturing/agents/investigation_agent_instructions.md](../../industry-packs/manufacturing/agents/investigation_agent_instructions.md))の内容を反映させることを推奨します。
5. **Preview** タブでテスト質問を送り、Activity trace で各 Tool(Fabric IQ / Foundry IQ / MCP server)がどのように呼び出されたかを確認します。

---

## 2. 検証チェックリスト

| 項目 | 確認方法 | 出典 |
|---|---|---|
| Fabric Ontology のデータバインド成功 | entity type details 画面でグラフが表示される | [How to view entity type details](https://learn.microsoft.com/en-us/fabric/iq/ontology/how-to-view-entity-type-details) |
| Fabric Data Agent の応答 | Fabric ポータルでテスト質問を送り、SQL/DAX/KQL 生成結果が返る | [Create a Fabric data agent](https://learn.microsoft.com/en-us/fabric/data-science/how-to-create-data-agent) |
| Foundry IQ Knowledge Source の取り込み状況 | `GET /knowledgesources/{name}/status` で `itemsUpdatesFailed` が 0 | [Create a Blob Knowledge Source](https://learn.microsoft.com/en-us/azure/search/agentic-knowledge-source-how-to-blob) |
| Copilot Studio 側の Fabric IQ / Foundry IQ 接続 | Preview タブでの Activity trace に該当 Tool の呼び出しが記録される | [Foundry IQ 接続ガイド](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/foundry-iq-connect)、[Fabric IQ 接続ガイド](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/fabric-iq-connect) |
| Work IQ MCP サーバーの直接応答(Local/Remote MCP) | `tools/call` の応答に `structuredContent`/`text` が返る(例: `ask` ツールで `response`/`conversationId`) | [Work IQ MCP tool reference](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/work-iq/mcp/tool-reference) |
| Work IQ 経由データの取得(Foundry IQ 間接経路) | Knowledge Base retrieve レスポンスの `references` に `type: "workIQ"` のエントリがある | [Create a Work IQ Knowledge Source](https://learn.microsoft.com/en-us/azure/search/agentic-knowledge-source-how-to-work-iq) |
| MCP Backend の接続 | `docs/deployment/Step-by-Step-Deployment-Guide.md` ステップ12参照 | 本リポジトリ実装・検証済み |

---

## 3. 本リポジトリ側で今後更新が必要な箇所

このガイドの手順が実際の環境で検証され次第、以下を更新してください。

1. [docs/decisions/product-verification.md](../decisions/product-verification.md) — 各手順の実行結果(成功/失敗・所要時間・遭遇したエラー)を追記。
2. [config/capabilities.yaml](../../config/capabilities.yaml) — `work_iq`/`foundry_iq`/`fabric_iq`/`harness.copilot_studio` の `status`/`last_verified_date` を実測結果で更新(GA/Preview 昇格には実日付と非 TBD の参照が必須、[ADR-0007](../decisions/0007-capability-registry-authority.md))。
3. `iq_platform/adapters/*/live_adapter.py` の `query()` — 実際に検証された API 呼び出し(または MCP クライアント接続)に置き換える([ADR-0015](../decisions/0015-mcp-native-iq-layer-integration.md) の対応手順参照)。
4. 本ガイド自体 — 「A-3 Ontology アイテムの新規作成」の **+ New item** ギャラリー項目名、「C-2 Work IQ Remote MCP」の接続エンドポイント・Copilot Studio 対応可否等、未確認と明記した箇所を実際の画面操作で確認し、確定情報に更新する。

## 4. 出典一覧(2026-09-10 取得)

- [What is Fabric IQ?](https://learn.microsoft.com/en-us/fabric/iq/overview)
- [What Is Ontology (Preview)?](https://learn.microsoft.com/en-us/fabric/iq/ontology/overview)
- [Bind Data (Ontology)](https://learn.microsoft.com/en-us/fabric/iq/ontology/how-to-bind-data)
- [Create a lakehouse in Microsoft Fabric](https://learn.microsoft.com/en-us/fabric/data-engineering/create-lakehouse)
- [Lakehouse tutorial - Ingest data into the lakehouse](https://learn.microsoft.com/en-us/fabric/data-engineering/tutorial-lakehouse-data-ingestion)
- [Fabric data agent creation (concept)](https://learn.microsoft.com/en-us/fabric/data-science/concept-data-agent)
- [Create a Fabric data agent (how-to)](https://learn.microsoft.com/en-us/fabric/data-science/how-to-create-data-agent)
- [Connect agents to Microsoft Fabric with Fabric IQ (preview) - Foundry Agent Service](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/fabric-iq)
- [Connect to Fabric IQ from an agent (preview) - Microsoft Copilot Studio](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/fabric-iq-connect)
- [Connect Agents to Foundry IQ Knowledge Bases - Foundry Agent Service](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/foundry-iq-connect)
- [Connect to Foundry IQ from an agent - Microsoft Copilot Studio](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/foundry-iq-connect)
- [Create a Knowledge Base - Azure AI Search](https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-how-to-create-knowledge-base)
- [What is a Knowledge Source? - Azure AI Search](https://learn.microsoft.com/en-us/azure/search/agentic-knowledge-source-overview)
- [Create a Blob Knowledge Source for Agentic Retrieval](https://learn.microsoft.com/en-us/azure/search/agentic-knowledge-source-how-to-blob)
- [Create a Work IQ Knowledge Source](https://learn.microsoft.com/en-us/azure/search/agentic-knowledge-source-how-to-work-iq)
- [Enable your tenant for Work IQ](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/work-iq/enable-work-iq)
- [Microsoft Work IQ API (protocol overview: A2A/MCP/REST)](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/work-iq/api-overview)
- [Work IQ MCP overview](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/work-iq/mcp/overview)
- [Work IQ MCP tool reference](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/work-iq/mcp/tool-reference)
- [Policy governance for Work IQ MCP](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/work-iq/mcp/policy-governance-mcp)
- [Create Entity Types (Ontology preview)](https://learn.microsoft.com/en-us/fabric/iq/ontology/how-to-create-entity-types)
- [Ontology (Preview) Required Tenant Settings](https://learn.microsoft.com/en-us/fabric/iq/ontology/overview-tenant-settings)
- [View Entity Type Details (Ontology preview)](https://learn.microsoft.com/en-us/fabric/iq/ontology/how-to-view-entity-type-details)
- [Harnesses in Copilot Studio](https://learn.microsoft.com/en-us/microsoft-copilot-studio/harnesses-overview)
- [Start building - Microsoft Copilot Studio](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/authoring-first-bot)
- [Available tools for agents - Microsoft Copilot Studio](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/tools-available)
- [Tools overview for agents - Microsoft Copilot Studio](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/tools-overview)
- [Add a Model Context Protocol (MCP) server to your agent as a tool (preview)](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/tools-add-mcp-server)
- [Available knowledge sources for agents - Microsoft Copilot Studio](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/knowledge-sources-overview)
- [Foundry IQ is now in Copilot Studio (Tech Community blog)](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/foundry-iq-is-now-in-copilot-studio-bring-your-enterprise-data-to-every-agent-co/4534635)
