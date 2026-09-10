# 開発者向け構成ステップバイステップガイド(実 Azure 環境へのデプロイ)

> **対象読者**: このリポジトリを実際の Azure サブスクリプションにデプロイしようとしている開発者。
> **対象範囲**: MCP Backend(`services/mcp-backend/`)を Azure Container Apps にデプロイする手順のみ。Work IQ / Foundry IQ / Fabric IQ / Copilot Studio の実 API 統合はこのガイドの範囲外です(理由は [§7](#7-live-adapter-を実サービスに接続したい場合任意) を参照)。
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

## 7. Live Adapter を実サービスに接続したい場合(任意)

MCP Backend のデプロイと、Work IQ / Foundry IQ / Fabric IQ の Live Adapter 接続は独立した関心事です。Live Adapter は現状 `query()` が常に `LiveAdapterNotYetVerifiedError` を送出するため([ADR-0013](../decisions/0013-live-adapter-verification-required-scaffold.md))、実際の業務データ取得には使えません。それでも Entra ID 認証部分だけを実タイテナントで検証したい場合は、[docs/setup/live-adapters-configuration.md](../setup/live-adapters-configuration.md) の手順に従い `.env` に `ENTRA_TENANT_ID` / `ENTRA_CLIENT_ID` / `ENTRA_CLIENT_SECRET` 等を設定し、`./scripts/demo/run-demo-cli.sh health` の Live Adapters セクションが `unavailable` から `verification_required` に変わることを確認してください。

## 8. 実 Microsoft 製品仕様が検証できた後の対応

Work IQ / Foundry IQ / Fabric IQ / Copilot Studio の実際の API 仕様・認証スコープ・ライセンス条件が検証できた時点で、次の順序で更新してください([docs/decisions/product-verification.md](../decisions/product-verification.md) の Process 節参照):

1. `docs/decisions/product-verification.md` の該当行を、検証者名・日付・参照元 URL・結果とともに更新する。
2. `config/capabilities.yaml` の対応する `capability_id` の `status` / `last_verified_date` / `documentation_reference` 等を、検証済みの実際の値に更新する(`iq_platform.contracts.capability.Capability` の validator が GA/Preview/Private Preview ステータスには実日付と非 TBD の参照を要求する)。
3. 該当する Live Adapter(`iq_platform/adapters/*/live_adapter.py`)の `query()` を、検証済みの実 API 呼び出しに置き換える。この時点で初めて `mode` が `live` に到達しうるようになる。
4. 関連するテスト(`tests/unit/test_live_adapters.py` 等)を実 API 呼び出しに対応する形で更新・追加する。

## 9. ロールバック・削除

デプロイしたリソースをすべて削除するには、このリポジトリの CLI から呼び出してください(誤操作防止のため、現在選択中の azd 環境名の入力確認が必須です):

```bash
./scripts/demo/run-demo-cli.sh cleanup
```

内部的には [scripts/cleanup/cleanup-azure.sh](../../scripts/cleanup/cleanup-azure.sh) が `azd env get-values` で現在の環境名を取得し、入力された環境名と一致した場合のみ `azd down --purge --force` を実行します。一致しない場合、または azd 環境が存在しない場合は何も削除せず安全に中断します(2026-09-10 に azd 環境が存在しない状態で実行し、中断することを確認済み)。

## 10. トラブルシューティング

デプロイ関連の問題は [docs/troubleshooting/README.md](../troubleshooting/README.md) を参照してください。それでも解決しない場合は、遭遇した実際のエラーメッセージを添えて本ガイドまたはトラブルシューティングガイドに追記してください(推測での「解決策らしきもの」を書き足さないこと)。

## 11. 最終チェックリスト(このガイドを使う前に)

- [ ] [docs/cost/README.md](../cost/README.md) を読み、コスト管理方針を決めた
- [ ] [docs/governance/README.md](../governance/README.md) と [docs/security/README.md](../security/README.md) を読み、ガバナンス・セキュリティ上の未実装事項(MCP Backend の認証がないこと等)を理解した
- [ ] テスト用・使い捨て可能な Azure サブスクリプションを用意した
- [ ] ローカルの Local Preview Mode デモが正常に動作することを確認した(`./scripts/demo/run-demo-cli.sh health`)
- [ ] 本ガイドの手順が「設計上想定される手順であり実行結果は未実測」であることを理解した
