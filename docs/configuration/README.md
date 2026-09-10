# 設定ガイド (Configuration Guide)

このリポジトリの設定は、大きく分けて (1) 環境変数（`.env`）、(2) Capability Registry（`config/capabilities.yaml`）、(3) Industry Pack の選択、の3つの仕組みから成ります。いずれも「未設定・未検証は安全側（`unavailable` や `verification_required`）に倒す」という方針で統一されています（[docs/architecture/architecture-guide.md](../architecture/architecture-guide.md) 3節）。

## 1. 環境変数（`.env`）

実体は [.env.example](../../.env.example) です。次の手順でコピーして使います。

```bash
cp .env.example .env
# .env を編集し、自分のテスト用テナント/サブスクリプションの値を設定する
```

- `.env` は `.gitignore` 済みでコミットされません。
- GUID/URL の例はすべてダミー値（架空テナント・架空サブスクリプション・`example.com`）です。
- 本番運用では `.env` ではなく Azure Key Vault 等の管理されたシークレットストアを使うべきです（この点についての実装済みガイドは本リポジトリにはまだありません）。

### 1.1 変数一覧（グループ別）

| グループ | 変数名 | 用途 | 実装状況 |
|---|---|---|---|
| 実行モード | `IIQ_EXECUTION_MODE` | `local_preview` / `hybrid` / `full_saas` のいずれかを宣言する目的で `.env.example` に定義 | **未実装** — 現状どのコードもこの変数を読み取りません。読み取り先は `demo-cli health` の Live Adapter 状態表示です |
| 実行モード | `IIQ_DEFAULT_INDUSTRY_PACK` | 既定 Industry Pack を宣言する目的で `.env.example` に定義 | **未実装** — Demo CLI の既定値はハードコードされた `manufacturing`（`apps/demo-cli/demo_cli/cli.py` の `DEFAULT_PACK_ID`）で、この環境変数は読み取られません |
| Azure | `AZURE_TENANT_ID` / `AZURE_SUBSCRIPTION_ID` / `AZURE_RESOURCE_GROUP` / `AZURE_LOCATION` | `azd`/Bicep デプロイ時の対象環境（[docs/decisions/open-questions.md](../decisions/open-questions.md) Q4 のテスト用サブスクリプション） | Bicep 側は `azd` の環境変数機構経由で消費（実デプロイ未検証） |
| Microsoft Entra ID | `ENTRA_TENANT_ID` / `ENTRA_CLIENT_ID` / `ENTRA_CLIENT_SECRET` | Live Adapter 共通の `azure-identity` `ClientSecretCredential` 認証情報 | 実装済み・単体テスト済み（`iq_platform/security/entra_auth.py`）。実テナントでの検証は未実施 |
| Copilot Studio | `COPILOT_STUDIO_ENVIRONMENT_ID` / `COPILOT_STUDIO_AGENT_ID` / `COPILOT_STUDIO_AUTH_SCOPE` | GitHub Copilot harness の設定値プレースホルダー | 製品名・仕様自体が未検証（[docs/decisions/product-verification.md](../decisions/product-verification.md)）。`COPILOT_STUDIO_AGENT_ID`/`COPILOT_STUDIO_AUTH_SCOPE` は既定で `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION` |
| Work IQ | `WORK_IQ_WORKSPACE_ID` / `WORK_IQ_AUTH_SCOPE` | Work IQ Live Adapter 設定値 | 同上（verification_required スキャフォールド、[ADR-0013](../decisions/0013-live-adapter-verification-required-scaffold.md)） |
| Foundry IQ | `FOUNDRY_IQ_PROJECT_ENDPOINT` / `FOUNDRY_IQ_KNOWLEDGE_BASE_ID` / `FOUNDRY_IQ_AUTH_SCOPE` | Foundry IQ Live Adapter 設定値 | 同上 |
| Fabric IQ | `FABRIC_WORKSPACE_ID` / `FABRIC_ONTOLOGY_ID` / `FABRIC_IQ_AUTH_SCOPE` | Fabric IQ Live Adapter 設定値 | 同上 |
| MCP Backend | `MCP_BACKEND_BASE_URL` / `MCP_BACKEND_API_KEY` | MCP Backend 呼び出し先/認証 | `MCP_BACKEND_API_KEY` は現状スキャフォールドのみ |
| MCP Backend | `MCP_BACKEND_ALLOWED_TOOLS` | Tool 名の許可リスト（後述 3節） | 実装済み・単体/統合テスト済み（`services/mcp-backend/mcp_backend/registry.py`） |
| 観測性 | `APPLICATIONINSIGHTS_CONNECTION_STRING` | Application Insights 接続文字列のプレースホルダー | **未実装** — `iq_platform/observability/logging_config.py` は標準出力への構造化ログのみで、Application Insights への送信は行いません |

`*_AUTH_SCOPE` の値が `TBD-VERIFY-AGAINST-CURRENT-MICROSOFT-DOCUMENTATION`（`iq_platform.configuration.settings.TBD_AUTH_SCOPE_PLACEHOLDER` と一致する文字列）のままの場合、`LiveAdapterSettings.auth_scope_for()` は `None` を返し、該当 Adapter は「まだ実スコープが設定されていない」ものとして扱われます。正しいスコープ自体が製品ごとに未検証のため、既定値を推測することは意図的に避けています。

## 2. Capability Registry（`config/capabilities.yaml`）

[config/capabilities.yaml](../../config/capabilities.yaml) は、プラットフォーム/Microsoft 製品の状態に関する**唯一の真実の情報源**です（[ADR-0007](../decisions/0007-capability-registry-authority.md)）。スキーマは `iq_platform.contracts.capability.Capability`（Pydantic モデル）で検証され、各エントリは次のフィールドを持ちます。

- `capability_id` / `display_name` / `product`
- `status`（例: `Mock Only`、`Verify Before Use`、`Unknown`）
- `last_verified_date` — 実際に人間が確認した日付以外を設定してはいけません
- `documentation_reference` — 参照した一次情報のパス/URL
- `required_license` / `required_role` / `required_admin_setting` / `regional_availability`
- `supported_modes`（`live` / `mock` / `simulated` / `unavailable` / `verification_required` の組み合わせ）
- `fallback_adapter`
- `known_limitations`（既知の制約の配列）
- `customer_facing_disclosure`

**強制ルール**: `status` が GA/Preview/Private Preview 系の値の場合、`last_verified_date` と非 TBD の `documentation_reference` が必須であることをスキーマの validator レベルで強制しています。現時点では `config/capabilities.yaml` 内のほぼすべての Microsoft 製品エントリが `Unknown` または `Verify Before Use` のままであり、これは [docs/decisions/product-verification.md](../decisions/product-verification.md) に記載の通り、実際に検証が完了していないことを正直に反映したものです。新しい Capability を追加・更新する場合は、必ず `product-verification.md` の該当行も同時に更新してください。

## 3. Industry Pack の選択

Industry Pack の切り替えは、プラットフォームコード（`iq_platform/`）を一切変更せずに行います（設計の中心原則、[README.md](../../README.md)）。

```bash
./scripts/demo/run-demo-cli.sh select-industry financial-services
./scripts/demo/run-demo-cli.sh run-demo
```

- `select-industry <name>` は選択結果を `scripts/demo/output/selected_industry_pack.json` に保存します（`apps/demo-cli/demo_cli/cli.py` の `STATE_FILE`）。以降 `--industry` を省略したコマンドはこのファイルを参照します。ファイルが存在しない場合の既定値は `manufacturing` です。
- 各 Industry Pack のルートには `manifest.yaml` があり、`iq_platform.contracts.manifest.IndustryPackManifest` で検証されます（[ADR-0004](../decisions/0004-industry-pack-manifest-schema.md)）。`id` / `default_scenario` / 各種 `*_path`（ontology・knowledge・MCP tools・semantics・scenario・evaluation 等）を宣言します。実例: [industry-packs/manufacturing/manifest.yaml](../../industry-packs/manufacturing/manifest.yaml)。
- 現在実装済みの5業界と既定シナリオ:
  | Industry Pack (`id`) | 既定シナリオ (`default_scenario`) |
  |---|---|
  | `manufacturing` | `quality-issue-investigation` |
  | `financial-services` | `fraud-investigation` |
  | `retail` | `demand-and-inventory-analysis` |
  | `healthcare` | `case-history-search` |
  | `public-sector` | `case-investigation` |
- MCP Backend 側の Industry Pack 選択は別経路です。環境変数 `IIQ_INDUSTRY_PACK`（既定 `manufacturing`）と `IIQ_DATA_SCALE`（既定 `demo`）を `services/mcp-backend/server.py` が読み取り、`build_app()` に渡します。Demo CLI の状態ファイルとは連動しないため、両方を独立に設定する必要がある点に注意してください。

## 4. `MCP_BACKEND_ALLOWED_TOOLS` 許可リスト

MCP Backend の `ToolRegistry`（[services/mcp-backend/mcp_backend/registry.py](../../services/mcp-backend/mcp_backend/registry.py)）は、Industry Pack が宣言した Tool 群に対する多層防御（defense-in-depth）の許可リストを持ちます。

- 未設定（既定）: 選択中の Industry Pack が宣言する全 Tool を許可します。
- `MCP_BACKEND_ALLOWED_TOOLS=tool_a,tool_b` のようにカンマ区切りで指定すると、そのリストに含まれない Tool 名は構造化エラーで拒否されます。
- Industry Pack 自体の `TOOL_FUNCTIONS` 辞書がすでに閉じた集合であるため、この許可リストは「特定の Tool をデプロイ環境ごとにさらに絞り込みたい」場合にのみ有効です（Tool を追加することはできません）。

## 5. `iq_platform/configuration/settings.py` との対応

Live Adapter が読み取る設定はすべて [iq_platform/configuration/settings.py](../../iq_platform/configuration/settings.py) の `LiveAdapterSettings` に集約されています。

- `LiveAdapterSettings.from_env()` が `.env`（プロセス環境変数）から上記1節の Entra ID / Copilot Studio / Work IQ / Foundry IQ / Fabric IQ 系の値を読み込みます。値が空文字列の場合は `None` として扱われます。
- `missing_entra_fields()` は Entra ID 3変数（`ENTRA_TENANT_ID` / `ENTRA_CLIENT_ID` / `ENTRA_CLIENT_SECRET`）のうち未設定のものを返します。
- `missing_fields_for(adapter_name)` は指定した Adapter（`work_iq` / `foundry_iq` / `fabric_iq` / `copilot_studio`）に必要な追加変数の不足分を返します。
- `auth_scope_for(adapter_name)` は、TBD プレースホルダーのままのスコープを `None` として扱い、`query()` を安易に実行しないようにします。

この設定と Live Adapter の `mode` 遷移（`unavailable` → `verification_required`）の関係は [docs/setup/live-adapters-configuration.md](../setup/live-adapters-configuration.md) と [docs/architecture/architecture-guide.md](../architecture/architecture-guide.md) 9.1節を参照してください。
