# 開発者向け構成ステップバイステップガイド(実 Azure 環境へのデプロイ)

> **対象読者**: 何もない状態から、このリポジトリを実環境(Azure サブスクリプション + Microsoft Entra ID テナント)に構成し、エージェント(GitHub Copilot Harness)と IQ レイヤー(Work IQ / Foundry IQ / Fabric IQ)までを一通り設定・動作確認したい開発者。
> **対象範囲**: (1) MCP Backend(`services/mcp-backend/`)を Azure Container Apps にデプロイする手順、(2) Microsoft Entra ID アプリ登録と Work IQ / Foundry IQ / Fabric IQ の環境変数設定手順、(3) Copilot Studio harness 側の設定に必要な前提情報、(4) 現時点で実際に検証可能な範囲と、まだ検証できない範囲の明示、をすべて含みます。**このガイドだけで「実際の Microsoft 365/Copilot データに接続したエージェントが動く」という状態にはなりません** — Work IQ / Foundry IQ / Fabric IQ / Copilot Studio harness の製品 API 仕様自体が[未検証](../decisions/product-verification.md)のためです。これはガイドの不備ではなく、リポジトリ全体の現在の実装状況です([ADR-0013](../decisions/0013-live-adapter-verification-required-scaffold.md)、[ADR-0014](../decisions/0014-local-orchestrator-is-not-a-harness-replacement.md))。何が今日検証可能で何がまだ不可能かは [ステップ12](#12-ステップ11-全体の動作確認-何が検証可能で何が検証不可能か) で正直に一覧化しています。
> **現在の検証状態**: `az bicep build` によるコンパイル検証(2026-09-10)と CI 上での Docker イメージビルド検証([.github/workflows/ci.yml](../../.github/workflows/ci.yml) の `validate-deployment` ジョブ)は完了しています。**しかし `azd up` を実 Azure サブスクリプションに対して実行した実績はこのリポジトリにはありません。** このガイドの手順自体は [ADR-0012](../decisions/0012-mcp-backend-deployment-target.md) の設計に基づく「実行可能なはずの手順」であり、実行結果を実測したものではないことを明記します。実行して問題が見つかった場合は、本ガイドと [docs/troubleshooting/README.md](../troubleshooting/README.md) を更新してください。

## 0. 前提として理解しておくべきこと

- このリポジトリは **Local Preview Mode**(合成データ・Mock/Simulated Adapter のみ)では完全に動作確認済みです([README.md](../../README.md) のチェックリスト参照)。実 Azure デプロイは Local Preview Mode の CLI デモとは別物です。
- デプロイしても「Microsoft 製品(Work IQ/Foundry IQ/Fabric IQ/Copilot Studio)と実際に繋がる」わけではありません。デプロイ対象は **MCP Backend(このリポジトリ自身が実装した FastAPI サービス)のみ**です。
- 本ガイドの手順は破壊的操作(Azure 課金が発生するリソースの作成)を含みます。必ずテスト用・使い捨て可能な Azure サブスクリプションで実行してください。
- 料金は一切確定していません。実行前に必ず [docs/cost/README.md](../cost/README.md) を読み、コスト管理(予算アラート等)を自身の判断で設定してください。

## 1. 事前準備チェックリスト

| # | 項目 | 確認方法 |
|---|---|---|
| 1 | Azure サブスクリプションへの Owner または Contributor + User Access Administrator 相当の権限 | `az account show` でサブスクリプションを確認 |
| 2 | Azure CLI (`az`) がインストール済み | `az version` |
| 3 | Azure Developer CLI (`azd`) がインストール済み | `azd version` |
| 4 | Docker がローカルにインストール済み、または `az acr build` によるリモートビルドを使う準備がある | `docker version`(未インストールの場合は下記 [3.3](#33-イメージビルドに関する注意) 参照) |
| 5 | このリポジトリの Local Preview Mode が手元で動作確認済み | `./scripts/demo/run-demo-cli.sh setup && ./scripts/demo/run-demo-cli.sh health` が成功する |

**注記**: このリポジトリの開発環境ではローカルに Docker がインストールされておらず、Docker イメージビルドの動作確認は [.github/workflows/ci.yml](../../.github/workflows/ci.yml) の CI(GitHub Actions)でのみ行われています。ローカルで `azd up` を実行する場合、Docker が必要になる可能性があります(`azd` のコンテナビルド方式は環境により異なるため、`TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION` — azd の最新ドキュメントで ACR リモートビルド対応状況を確認してください)。

## 2. ステップ1: ローカル環境のセットアップと健全性確認

```bash
git clone <このリポジトリの URL>
cd POC-Harness-CustomIQ
./scripts/demo/run-demo-cli.sh setup
./scripts/demo/run-demo-cli.sh health
```

`health` の出力で `Industry Pack: Manufacturing - Ready` 等が表示され、`ruff check .` / `pytest tests/ -v` がエラーなく完了していれば、ローカル環境は正常です(2026-09-10 時点で137件のテストがすべて成功することを確認済み)。

## 3. ステップ2: Bicep テンプレートの構文検証(任意、既に実施済み)

実 Azure に触れる前に、テンプレートが構文的に正しいことをローカルで再確認できます。

```bash
az bicep build --file deployment/bicep/main.bicep --stdout > /dev/null && echo "Bicep OK"
```

このコマンドは2026-09-10時点で実行済み・成功確認済みです([deployment/bicep/README.md](../../deployment/bicep/README.md))。

### 3.3 イメージビルドに関する注意

`azure.yaml` は `services.mcp-backend.docker.path` に [deployment/containers/mcp-backend/Dockerfile](../../deployment/containers/mcp-backend/Dockerfile) を指定しています。`azd up` / `azd deploy` はこの Dockerfile からイメージをビルドしてプッシュしようとします。ローカルに Docker がない場合、事前に以下のいずれかを行ってください(具体的な設定手順は `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION` — azd の最新ドキュメントを確認):

- Docker Desktop 等をインストールする、または
- Azure Container Registry のリモートビルド機能(`az acr build`)を使うよう `azd` の設定を調整する。

## 4. ステップ3: Azure へのログインと azd 環境の作成

```bash
azd auth login
azd env new <環境名>          # 例: iiq-dev
azd env set AZURE_SUBSCRIPTION_ID <サブスクリプションID>
azd env set AZURE_LOCATION <リージョン名>   # 例: japaneast (リージョンの実際の提供状況は各自 Azure Portal で確認)
```

`<環境名>` は [scripts/cleanup/cleanup-azure.sh](../../scripts/cleanup/cleanup-azure.sh) による削除時にも使う識別子になるため、覚えやすく他の環境と衝突しない名前にしてください。

## 5. ステップ4: プロビジョニングとデプロイ(`azd up`)

```bash
azd up
```

このコマンドは内部的に次を行います(`azure.yaml` / [deployment/bicep/main.bicep](../../deployment/bicep/main.bicep) / [deployment/bicep/resources.bicep](../../deployment/bicep/resources.bicep) の定義に基づく):

1. サブスクリプションスコープで新しいリソースグループ `rg-<環境名>` を作成
2. リソースグループ内に以下を作成:
   - Log Analytics ワークスペース(`PerGB2018`, 保持期間30日)
   - Azure Container Registry(Basic SKU、**Admin ユーザー無効**)
   - User-Assigned Managed Identity(ACR への `AcrPull` ロールのみ付与、最小権限)
   - Container Apps Environment
   - Container App `ca-mcp-backend-<トークン>`(初期状態ではプレースホルダーイメージ `mcr.microsoft.com/azuredocs/containerapps-helloworld:latest`、0.5 vCPU / 1Gi メモリ、0〜2 レプリカでスケール、**Ingress は内部限定(`external: false`)**)
3. `services/mcp-backend` のコードから実イメージをビルドし、作成した ACR にプッシュ
4. Container App のイメージをプレースホルダーから実イメージに更新

**実行結果はこのリポジトリでは実測されていません。** 実行して成功/失敗した場合は、その結果(コマンド出力、要した時間、遭遇したエラー)を本ガイドまたは [docs/troubleshooting/README.md](../troubleshooting/README.md) に追記することを強く推奨します。

## 6. ステップ5: デプロイ後の検証

Ingress が内部限定(`external: false`)のため、外部から直接 `curl` することはできません。検証方法の候補:

```bash
# コンテナアプリの状態確認
az containerapp show --name ca-mcp-backend-<トークン> --resource-group rg-<環境名> --query "properties.runningStatus"

# ログの確認
az containerapp logs show --name ca-mcp-backend-<トークン> --resource-group rg-<環境名> --follow

# コンテナ内部からの疎通確認(コンテナ内に curl 等がある前提)
az containerapp exec --name ca-mcp-backend-<トークン> --resource-group rg-<環境名> --command "curl -s http://localhost:8000/health"
```

外部からアクセス可能にしたい場合は `resources.bicep` の `ingress.external` を `true` に変更する必要がありますが、これは公開範囲を広げるセキュリティ上の判断であり、必ずチーム内でレビューしてから行ってください([docs/mcp/MCP-Security-Guide.md](../mcp/MCP-Security-Guide.md) 参照。**MCP Backend にはリクエスト認証機能が未実装**であるため、外部公開する場合は別途 API Gateway や認証層を用意することを強く推奨します)。

## 7. ステップ6: Microsoft Entra ID アプリ登録(Work IQ / Foundry IQ / Fabric IQ / Copilot Studio 共通)

Work IQ / Foundry IQ / Fabric IQ の Live Adapter と Copilot Studio harness はすべて同じ Entra ID アプリ登録(クライアントID・シークレット・テナントID)を共有します。実施手順は [docs/setup/live-adapters-configuration.md](../setup/live-adapters-configuration.md) の「前提: Microsoft Entra ID アプリ登録(今すぐ実施可能)」節に全手順(目的・必要権限・操作手順・失敗時のエラー・Rollback 方法含む)がまとまっています。このステップは**任意ではなく、Work IQ/Foundry IQ/Fabric IQ/Copilot Studio のいずれかを設定する前に必ず完了させてください**。

完了後の `.env` 設定例:
```
ENTRA_TENANT_ID=<Directory (tenant) ID>
ENTRA_CLIENT_ID=<Application (client) ID>
ENTRA_CLIENT_SECRET=<クライアントシークレットの値>
```

確認: `./scripts/demo/run-demo-cli.sh health` で Live Adapters の各行が `unavailable` から変化する(他の必須値が未設定なら `Missing required configuration` のまま)。

## 8. ステップ7: Work IQ の設定

[docs/setup/live-adapters-configuration.md](../setup/live-adapters-configuration.md) の「Work IQ(未検証セクション)」節に従って、以下を `.env` に設定します。
```
WORK_IQ_WORKSPACE_ID=<実際のワークスペースID>
WORK_IQ_AUTH_SCOPE=<実際に確認できた OAuth スコープ>  # 未設定(TBD プレースホルダー)のままだと health check は認証を試行しない
```
ワークスペースIDの具体的な取得方法や必要な API アクセス許可は `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`(製品仕様未検証のため)。確認: `./scripts/demo/run-demo-cli.sh health` で `Work IQ (live): verification_required` に変わる。

## 9. ステップ8: Foundry IQ の設定

[docs/setup/live-adapters-configuration.md](../setup/live-adapters-configuration.md) の「Foundry IQ(未検証セクション)」節に従って、以下を `.env` に設定します。
```
FOUNDRY_IQ_PROJECT_ENDPOINT=<実際のプロジェクトエンドポイント>
FOUNDRY_IQ_KNOWLEDGE_BASE_ID=<実際のナレッジベースID>
FOUNDRY_IQ_AUTH_SCOPE=<実際に確認できた OAuth スコープ>
```
確認: `./scripts/demo/run-demo-cli.sh health` で `Foundry IQ (live): verification_required` に変わる。

## 10. ステップ9: Fabric IQ の設定

[docs/setup/live-adapters-configuration.md](../setup/live-adapters-configuration.md) の「Fabric IQ(未検証セクション)」節に従って、以下を `.env` に設定します。
```
FABRIC_WORKSPACE_ID=<実際のワークスペースID>
FABRIC_ONTOLOGY_ID=<実際のオントロジーID>
FABRIC_IQ_AUTH_SCOPE=<実際に確認できた OAuth スコープ>
```
確認: `./scripts/demo/run-demo-cli.sh health` で `Fabric IQ (live): verification_required` に変わる。

## 11. ステップ10: Copilot Studio harness(エージェント/オーケストレーション層)の設定

**これがエージェント層自体の設定です。** [ADR-0014](../decisions/0014-local-orchestrator-is-not-a-harness-replacement.md)・[ADR-0016](../decisions/0016-copilot-studio-github-harness-confirmed.md) の通り、本番でのオーケストレーション層は `GenericLocalOrchestrator`(Local Preview 専用の代替)ではなく、Microsoft Copilot Studio の GitHub Copilot harness で作成したエージェントです。この点は 2026-09-10 に実際の Microsoft Learn ドキュメントで確認済みです。

**11.1 このリポジトリの MCP Backend を Copilot Studio エージェントの Tool として追加する(実装済み・このリポジトリで検証済み)**

MCP Backend は [ADR-0016](../decisions/0016-copilot-studio-github-harness-confirmed.md) に基づき、公式 MCP Python SDK で実プロトコル準拠の MCP サーバーを `/mcp` に公開しています(詳細は [docs/mcp/MCP-Design-and-Contract-Guide.md](../mcp/MCP-Design-and-Contract-Guide.md) セクション5)。Copilot Studio 側では次の手順で追加します(Microsoft Learn [Add a Model Context Protocol (MCP) server to your agent as a tool](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/tools-add-mcp-server) で確認済みの手順、ただし実際の Copilot Studio 環境での実行はこのリポジトリでは未実施):

1. Copilot Studio でエージェントを開き、Build タブ → Tools → 「Add」→「Model Context Protocol (MCP)」を選択する。
2. Name / Description を入力し、Server URL に `https://<デプロイ先の FQDN>/mcp/` を入力する(末尾の `/` を含める。ステップ4でデプロイした Container App の URL を使う)。
3. Authentication を選択する(現状 MCP Backend にはリクエスト認証が実装されていないため、[docs/mcp/Authentication-and-Error-Handling-Guide.md](../mcp/Authentication-and-Error-Handling-Guide.md) を参照し、外部公開前に必ず認証層を追加すること)。
4. 「Add」を選択すると、Copilot Studio がプロトコルハンドシェイクを行い、選択中の Industry Pack が公開する Tool 一覧を取得する。
5. `MCP_BACKEND_ALLOWED_HOSTS` 環境変数に、デプロイ先の実際のホスト名を追加しておくこと(未設定だと `localhost`/`127.0.0.1`/`testserver` 以外からのリクエストは `421 Misdirected Request` で拒否される。[docs/mcp/MCP-Security-Guide.md](../mcp/MCP-Security-Guide.md) 参照)。

**11.2 Foundry IQ / Fabric IQ をエージェントに接続する(Copilot Studio がネイティブに提供、このリポジトリのコードは関与しない)**

Foundry IQ・Fabric IQ は Copilot Studio の GitHub Copilot harness エージェントに、Copilot Studio 自身が提供する専用の Tool 追加フローで直接接続できることが確認されています(このリポジトリの独自コードは一切不要)。**SaaS 側(Fabric ワークスペース・Lakehouse・Ontology・Azure AI Search Knowledge Base・Work IQ テナント有効化)を実際に構築してサンプルデータで動かす詳細手順は [docs/setup/Production-SaaS-Environment-Setup-Guide.md](../setup/Production-SaaS-Environment-Setup-Guide.md) にまとめています。**

- Foundry IQ: Build タブ → Tools →「Foundry IQ」→ 接続作成(API キー / クライアント証明書 / サービスプリンシパル / Entra ID 統合のいずれか)→ Knowledge Base を選択。([Connect to Foundry IQ from an agent](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/foundry-iq-connect))
- Fabric IQ(プレビュー): Build タブ →「+ Add tool」→「Fabric IQ」→ 標準の Tool 追加フローに従う。([Connect to Fabric IQ from an agent (preview)](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/fabric-iq-connect))
- Work IQ: Copilot Studio からの一次機能としての利用可否は確認できていません(**未確認、断定しない**)。Work IQ 自体は標準的な MCP サーバーを公開しているため([docs/decisions/product-verification.md](../decisions/product-verification.md))、上記11.1と同じ「Add MCP server」の汎用フローで手動接続できる可能性がありますが、未検証です。

**11.3 環境変数(参考、`.env` での存在確認のみ)**

`demo-cli health` で設定値の存在確認のみ行う場合は、[docs/setup/live-adapters-configuration.md](../setup/live-adapters-configuration.md) の「Copilot Studio harness」節に従って、以下を `.env` に設定します。
```
COPILOT_STUDIO_ENVIRONMENT_ID=<実際の環境ID>
COPILOT_STUDIO_AGENT_ID=<実際のエージェントID>
```
確認: `./scripts/demo/run-demo-cli.sh health` で `Copilot Studio harness: Configuration present (Verification Required)` に変わる。

**重要**: 11.3 の環境変数はあくまで `demo-cli health` による設定値の存在確認のみを目的としたものです。実際に Copilot Studio 上でこのリポジトリの MCP Backend を Tool として登録する手順は 11.1 に記載した通り実装・検証済みですが、Foundry IQ/Fabric IQ の接続(11.2)は Copilot Studio 自身の機能であり、このリポジトリのコードは一切関与しません。

## 12. ステップ11: 全体の動作確認 — 何が検証可能で何が検証不可能か

ステップ6〜10をすべて完了した後でも、「エージェントが実際の業務データで回答する」という意味でのエンドツーエンド動作確認はできません。以下を正直に切り分けます。

### 今日検証可能なこと

| 項目 | 確認方法 | 期待される結果 |
|---|---|---|
| Entra ID 認証(各 IQ レイヤー共通) | `./scripts/demo/run-demo-cli.sh health` | 各アダプターが `verification_required` になり、「認証は成功したが製品 API 契約は未検証」と表示される |
| MCP Backend の健全性 | `az containerapp show`/`logs`/`exec`(ステップ5参照) | Container App が `Running` で `/health` が 200 を返す |
| MCP Backend の Tool 一覧・実行 | `GET /tools` / `POST /tools/{name}/invoke` | 選択した Industry Pack の Tool 一覧が返り、合成データでの実行結果が返る |
| 実 MCP プロトコルハンドシェイク(`/mcp`) | [scripts/demo/test_mcp_protocol_connectivity.py](../../scripts/demo/test_mcp_protocol_connectivity.py)(公式 MCP クライアント SDK 使用) | `initialize` → `tools/list` → `tools/call` が成功する(Copilot Studio の「Add MCP server」が行うのと同種のハンドシェイク) |
| Local Preview Mode でのエージェント応答形式 | `./scripts/demo/run-demo-cli.sh run-demo` | `AgentResponse`(14項目)の実際の出力例を確認できる(合成データ) |

### まだ検証できないこと(製品仕様未検証のため)

- Work IQ / Foundry IQ / Fabric IQ の `query()` は常に `LiveAdapterNotYetVerifiedError` を送出します。実際の業務データ取得はできません([ADR-0013](../decisions/0013-live-adapter-verification-required-scaffold.md))。
- **本リポジトリの MCP Backend を実 Copilot Studio 環境から呼び出す統合は、実プロトコル準拠のサーバー実装(11.1、[ADR-0016](../decisions/0016-copilot-studio-github-harness-confirmed.md))自体は完了していますが、実際の Copilot Studio 環境に接続して検証したことはまだありません。** 検証済みなのは、公式 MCP クライアント SDK が正しくハンドシェイクできること([tests/integration/test_mcp_protocol_server.py](../../tests/integration/test_mcp_protocol_server.py)、[scripts/demo/test_mcp_protocol_connectivity.py](../../scripts/demo/test_mcp_protocol_connectivity.py))のみです。
- したがって、「エージェントに自然言語で問い合わせて実業務データを伴う回答を得る」という意味でのエンドツーエンド検証は、現時点で Local Preview Mode(合成データ)でしかできません。`./scripts/demo/run-demo-cli.sh run-demo` がこの代替検証手段です。

製品仕様が検証でき次第、上記の「検証できないこと」を「検証済み」に更新するための作業は [ステップ13](#13-実-microsoft-製品仕様が検証できた後の対応) に記載しています。

## 13. 実 Microsoft 製品仕様が検証できた後の対応

Work IQ / Foundry IQ / Fabric IQ / Copilot Studio の実際の API 仕様・認証スコープ・ライセンス条件が検証できた時点で、次の順序で更新してください([docs/decisions/product-verification.md](../decisions/product-verification.md) の Process 節参照):

1. `docs/decisions/product-verification.md` の該当行を、検証者名・日付・参照元 URL・結果とともに更新する。
2. `config/capabilities.yaml` の対応する `capability_id` の `status` / `last_verified_date` / `documentation_reference` 等を、検証済みの実際の値に更新する(`iq_platform.contracts.capability.Capability` の validator が GA/Preview/Private Preview ステータスには実日付と非 TBD の参照を要求する)。
3. 該当する Live Adapter(`iq_platform/adapters/*/live_adapter.py`)の `query()` を、検証済みの実 API 呼び出しに置き換える。この時点で初めて `mode` が `live` に到達しうるようになる。
4. コピロットスタジオ上で MCP Backend を Tool として登録し、エージェントの指示(`agent_instructions_path`)を反映する。
5. 関連するテスト(`tests/unit/test_live_adapters.py` 等)を実 API 呼び出しに対応する形で更新・追加する。

## 14. ロールバック・削除

デプロイしたリソースをすべて削除するには、このリポジトリの CLI から呼び出してください(誤操作防止のため、現在選択中の azd 環境名の入力確認が必須です):

```bash
./scripts/demo/run-demo-cli.sh cleanup
```

内部的には [scripts/cleanup/cleanup-azure.sh](../../scripts/cleanup/cleanup-azure.sh) が `azd env get-values` で現在の環境名を取得し、入力された環境名と一致した場合のみ `azd down --purge --force` を実行します。一致しない場合、または azd 環境が存在しない場合は何も削除せず安全に中断します(2026-09-10 に azd 環境が存在しない状態で実行し、中断することを確認済み)。

## 15. トラブルシューティング

デプロイ関連の問題は [docs/troubleshooting/README.md](../troubleshooting/README.md) を参照してください。それでも解決しない場合は、遭遇した実際のエラーメッセージを添えて本ガイドまたはトラブルシューティングガイドに追記してください(推測での「解決策らしきもの」を書き足さないこと)。

## 16. 最終チェックリスト(このガイドを使う前に)

- [ ] [docs/cost/README.md](../cost/README.md) を読み、コスト管理方針を決めた
- [ ] [docs/governance/README.md](../governance/README.md) と [docs/security/README.md](../security/README.md) を読み、ガバナンス・セキュリティ上の未実装事項(MCP Backend の認証がないこと等)を理解した
- [ ] テスト用・使い捨て可能な Azure サブスクリプションを用意した
- [ ] ローカルの Local Preview Mode デモが正常に動作することを確認した(`./scripts/demo/run-demo-cli.sh health`)
- [ ] Work IQ / Foundry IQ / Fabric IQ / Copilot Studio の設定手順(ステップ6〜10)はすべて Entra ID 認証までしか検証できず、製品 API 接続自体は未実装であることを理解した(ステップ12)
- [ ] 本ガイドの手順が「設計上想定される手順であり実行結果は未実測」であることを理解した
