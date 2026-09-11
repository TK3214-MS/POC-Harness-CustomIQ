# Live Adapter 設定ガイド（Copilot Studio / Work IQ / Foundry IQ / Fabric IQ）

> **用途**: このガイドはLocal Preview内部のLive Adapterスキャフォールドを確認するためのものです。Copilot StudioのGitHub Copilot harnessからFabric IQ、Foundry IQ、Work IQへ直接接続する本番構成では、このガイドのIQ用環境変数・Adapter設定は使用しません。SaaS側の構築とCopilot Studio接続は [docs/setup/Production-SaaS-Environment-Setup-Guide.md](Production-SaaS-Environment-Setup-Guide.md) を参照してください。
>
> このガイドは [ADR-0013](../decisions/0013-live-adapter-verification-required-scaffold.md) の設計に基づき、**今すぐ実施可能な部分（Entra ID アプリ登録、環境変数設定）** と **未検証で後から埋める部分（各 Microsoft 製品固有の手順）** を明確に分離しています。

## 前提: Microsoft Entra ID アプリ登録（今すぐ実施可能）

Work IQ / Foundry IQ / Fabric IQ の Live Adapter はすべて同じ Entra ID アプリ登録（クライアントID・シークレット・テナントID）を共有します。以下は Entra ID アプリ登録自体の標準的な手順であり、Work IQ 等の製品固有仕様には依存しません。

1. **目的**: Live Adapter が Microsoft Entra ID でアプリケーション認証（クライアントクレデンシャルフロー）を行えるようにする。
2. **推定所要時間**: 未実測。設計上は10〜15分。
3. **必要なライセンスまたはSubscription**: Microsoft Entra ID テナントの管理者権限を持つアカウント（テスト用 Azure サブスクリプションに付随するテナントで可）。
4. **必要なRoleとPermission**: Entra ID の「アプリケーション管理者」相当のロール（正確なロール名は `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`）。
5. **対象Tenant、Environment、Region**: テスト用 Azure サブスクリプションに紐づくテナント（[docs/decisions/open-questions.md](../decisions/open-questions.md) Q4）。
6. **アクセスする管理画面**: Azure Portal > Microsoft Entra ID > アプリの登録（正確な画面名・パスは `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`）。

   [SCREENSHOT REQUIRED: Azure Portal > Microsoft Entra ID > App registrations > New registration]
   - 撮影する画面: 新規アプリ登録フォーム
   - 強調するボタンまたはフィールド: "New registration" ボタン、"Name" フィールド
   - マスクするTenant ID、User name、Subscription、Endpoint、Secret: テナントID、サインイン中のユーザー名
   - 期待状態: 新しいアプリ登録が作成され、Application (client) ID と Directory (tenant) ID が表示される
   - 画面が変更された場合の確認先: `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`

7. **操作手順**:
   1. Azure Portal で Microsoft Entra ID > アプリの登録 > 新規登録を開く。
   2. アプリ名（例: `industry-iq-platform-accelerator`）を入力し登録する。
   3. 「Application (client) ID」と「Directory (tenant) ID」を控える。
   4. 「証明書とシークレット」からクライアントシークレットを新規作成し、値を控える（**この値は一度しか表示されない**）。
   5. このアプリに Work IQ / Foundry IQ / Fabric IQ を利用するために必要な API アクセス許可を追加する手順は `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`（各製品のセクションを参照）。
8. **入力する設定値**: `.env` に以下を設定する（`.env.example` を参照）。
   ```
   ENTRA_TENANT_ID=<Directory (tenant) ID>
   ENTRA_CLIENT_ID=<Application (client) ID>
   ENTRA_CLIENT_SECRET=<クライアントシークレットの値>
   ```
9. **SecretまたはSensitive Informationの扱い**: `ENTRA_CLIENT_SECRET` は `.env`（gitignore 対象）にのみ記載し、絶対にコミットしない。本番用途では Azure Key Vault を使用する（[SECURITY.md](../../SECURITY.md)）。
10. **成功時に表示される状態**: `./scripts/demo/run-demo-cli.sh health` の "Live Adapters" セクションで、各アダプターが `unavailable` から `verification_required` に変わり、メッセージが「Missing required configuration」から「OAuth scope ... has not been verified yet」に変わる。
11. **Validation Checkpoint**: `iq_platform.configuration.settings.LiveAdapterSettings.from_env().missing_entra_fields()` が空リストを返すこと。
12. **動作確認方法**: `./scripts/demo/run-demo-cli.sh health` を実行し、Live Adapters セクションを確認する。
13. **よくあるエラー**: `EntraAuthConfigurationError`(環境変数が未設定) / `EntraAuthFailedError`(認証情報が誤っている、またはテナント/クライアントの組み合わせが不正)。
14. **Troubleshootingへのリンク**: [docs/troubleshooting/](../troubleshooting/)（Phase 6 で拡充予定）。
15. **Rollbackまたは削除方法**: Azure Portal でアプリ登録を削除する、またはクライアントシークレットを失効させる。
16. **本番環境で追加すべきSecurity設定**: クライアントシークレットではなく証明書ベース認証、または Managed Identity への切り替えを検討する。シークレットのローテーション期限を設定する。
17. **Preview、GA、Unknownの明示**: Microsoft Entra ID のアプリ登録機能自体は一般提供されている想定だが、正確な GA 状態は本ガイドでは未検証（`TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`）。
18. **最終確認日**: 未実施。
19. **根拠としたMicrosoft Documentation**: `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`。

---

## Work IQ（未検証セクション）

1. **目的**: `WorkIQLiveAdapter` が実際の Work IQ ワークスペースに接続できるようにする。
2. **推定所要時間**: `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`
3. **必要なライセンスまたはSubscription**: `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`
4. **必要なRoleとPermission**: `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`
5. **対象Tenant、Environment、Region**: `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`
6. **アクセスする管理画面**: `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`
7. **操作手順**: `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`(Work IQ ワークスペースの作成/特定方法が確認でき次第記載する)
8. **入力する設定値**:
   ```
   WORK_IQ_WORKSPACE_ID=<実際のワークスペースID>
   WORK_IQ_AUTH_SCOPE=<実際に確認できた OAuth スコープ>  # 既定値の TBD プレースホルダーのままだと health check は認証を試行しない
   ```
9. **SecretまたはSensitive Informationの扱い**: ワークスペースID自体は機密情報ではない想定だが、確認まで `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`。
10. **成功時に表示される状態**: `demo-cli health` で `Work IQ (live): verification_required - Microsoft Entra ID authentication succeeded for the configured scope, but the underlying product API contract has not been verified...`
11. **Validation Checkpoint**: 上記メッセージが表示され、かつ `WorkIQLiveAdapter.health_check().healthy` は依然として `False`(API 契約自体が未検証なため、認証成功だけでは `healthy=True` にならない設計、[ADR-0013](../decisions/0013-live-adapter-verification-required-scaffold.md))。
12. **動作確認方法**: `./scripts/demo/run-demo-cli.sh health`
13. **よくあるエラー**: `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`
14. **Troubleshootingへのリンク**: [docs/troubleshooting/](../troubleshooting/)
15. **Rollbackまたは削除方法**: `.env` から該当変数を削除する。
16. **本番環境で追加すべきSecurity設定**: `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`
17. **Preview、GA、Unknownの明示**: Unknown（[docs/decisions/product-verification.md](../decisions/product-verification.md)）
18. **最終確認日**: 未実施
19. **根拠としたMicrosoft Documentation**: `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`

## Foundry IQ（未検証セクション）

1. **目的**: `FoundryIQLiveAdapter` が実際の Foundry IQ ナレッジベースに接続できるようにする。
2. **推定所要時間**: `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`
3. **必要なライセンスまたはSubscription**: `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`
4. **必要なRoleとPermission**: `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`
5. **対象Tenant、Environment、Region**: `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`
6. **アクセスする管理画面**: `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`
7. **操作手順**: `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`
8. **入力する設定値**:
   ```
   FOUNDRY_IQ_PROJECT_ENDPOINT=<実際のプロジェクトエンドポイント>
   FOUNDRY_IQ_KNOWLEDGE_BASE_ID=<実際のナレッジベースID>
   FOUNDRY_IQ_AUTH_SCOPE=<実際に確認できた OAuth スコープ>
   ```
9. **SecretまたはSensitive Informationの扱い**: `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`
10. **成功時に表示される状態**: `demo-cli health` で `Foundry IQ (live): verification_required - ...authentication succeeded...`
11. **Validation Checkpoint**: 同上（Work IQ セクション参照）。
12. **動作確認方法**: `./scripts/demo/run-demo-cli.sh health`
13. **よくあるエラー**: `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`
14. **Troubleshootingへのリンク**: [docs/troubleshooting/](../troubleshooting/)
15. **Rollbackまたは削除方法**: `.env` から該当変数を削除する。
16. **本番環境で追加すべきSecurity設定**: `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`
17. **Preview、GA、Unknownの明示**: Unknown（[docs/decisions/product-verification.md](../decisions/product-verification.md)）
18. **最終確認日**: 未実施
19. **根拠としたMicrosoft Documentation**: `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`

## Fabric IQ（未検証セクション）

1. **目的**: `FabricIQLiveAdapter` が実際の Fabric ワークスペース/オントロジーに接続できるようにする。
2. **推定所要時間**: `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`
3. **必要なライセンスまたはSubscription**: `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`(Microsoft Fabric capacity が必要な可能性)
4. **必要なRoleとPermission**: `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`
5. **対象Tenant、Environment、Region**: `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`
6. **アクセスする管理画面**: `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`
7. **操作手順**: `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`
8. **入力する設定値**:
   ```
   FABRIC_WORKSPACE_ID=<実際のワークスペースID>
   FABRIC_ONTOLOGY_ID=<実際のオントロジーID>
   FABRIC_IQ_AUTH_SCOPE=<実際に確認できた OAuth スコープ>
   ```
9. **SecretまたはSensitive Informationの扱い**: `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`
10. **成功時に表示される状態**: `demo-cli health` で `Fabric IQ (live): verification_required - ...authentication succeeded...`
11. **Validation Checkpoint**: 同上（Work IQ セクション参照）。
12. **動作確認方法**: `./scripts/demo/run-demo-cli.sh health`
13. **よくあるエラー**: `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`
14. **Troubleshootingへのリンク**: [docs/troubleshooting/](../troubleshooting/)
15. **Rollbackまたは削除方法**: `.env` から該当変数を削除する。
16. **本番環境で追加すべきSecurity設定**: `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`
17. **Preview、GA、Unknownの明示**: Unknown（[docs/decisions/product-verification.md](../decisions/product-verification.md)）。Fabric IQ、Fabric Data Agent、Fabric IQ Ontology MCP は別機能として扱う（[ADR-0007](../decisions/0007-capability-registry-authority.md)）。
18. **最終確認日**: 未実施
19. **根拠としたMicrosoft Documentation**: `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`

## Copilot Studio harness（未検証セクション、Adapter クラスなし）

Copilot Studio は IQ レイヤー Adapter ではなく Harness/Orchestrator そのものであるため、専用の `Adapter` クラスは実装していません（[ADR-0013](../decisions/0013-live-adapter-verification-required-scaffold.md)）。設定値の存在確認のみ `demo-cli health` に含まれます。

1. **目的**: 将来、Copilot Studio 上でこのアクセラレータの Industry Pack 設定・MCP Tool 接続を行うための前提情報を揃える。
2. **推定所要時間**: `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`
3. **必要なライセンスまたはSubscription**: `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`
4. **必要なRoleとPermission**: `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`
5. **対象Tenant、Environment、Region**: `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`
6. **アクセスする管理画面**: `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`

   [SCREENSHOT REQUIRED: Copilot Studio > Build > Tools > Add tool]
   - 撮影する画面: MCP Tool 追加画面
   - 強調するボタンまたはフィールド: "Add tool" ボタン、エンドポイントURL入力欄
   - マスクするTenant ID、User name、Subscription、Endpoint、Secret: 環境ID、テナントID
   - 期待状態: MCP Backend のツール一覧が Copilot Studio 側に表示される
   - 画面が変更された場合の確認先: `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`

7. **操作手順**: `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`
8. **入力する設定値**:
   ```
   COPILOT_STUDIO_ENVIRONMENT_ID=<実際の環境ID>
   COPILOT_STUDIO_AGENT_ID=<実際のエージェントID>
   ```
9. **SecretまたはSensitive Informationの扱い**: `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`
10. **成功時に表示される状態**: `demo-cli health` で `Copilot Studio harness: Configuration present (Verification Required)`。
11. **Validation Checkpoint**: `LiveAdapterSettings.from_env().missing_fields_for("copilot_studio")` が空リストを返すこと。
12. **動作確認方法**: `./scripts/demo/run-demo-cli.sh health`
13. **よくあるエラー**: `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`
14. **Troubleshootingへのリンク**: [docs/troubleshooting/](../troubleshooting/)
15. **Rollbackまたは削除方法**: `.env` から該当変数を削除する。
16. **本番環境で追加すべきSecurity設定**: `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`
17. **Preview、GA、Unknownの明示**: Verify Before Use（[config/capabilities.yaml](../../config/capabilities.yaml) `harness.copilot_studio`）
18. **最終確認日**: 未実施
19. **根拠としたMicrosoft Documentation**: `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`
