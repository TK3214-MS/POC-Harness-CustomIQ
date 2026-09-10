# トラブルシューティングガイド (リポジトリ全体)

このガイドはリポジトリ全体（セットアップ、CLI、テスト、Live Adapter、デプロイ）を対象とした汎用トラブルシューティングです。30分セルフガイドデモの実施中に発生する問題は、こちらではなく [docs/self-guided-demo/Troubleshooting.md](../self-guided-demo/Troubleshooting.md) を参照してください（デモの各ステップに沿った個別の問題を扱っています）。

## セットアップ関連

### `python3 --version` が 3.11 未満

`pyproject.toml` は `requires-python = ">=3.11"` を宣言しており、Python 3.11 未満では `pip install -e ".[dev]"` に失敗します。[scripts/setup/setup.sh](../../scripts/setup/setup.sh) は実行前にバージョンを確認し、古い場合はエラーで停止します。`PYTHON_BIN` 環境変数で新しいインタプリタを明示してください。

```bash
PYTHON_BIN=/opt/homebrew/bin/python3.12 ./scripts/setup/setup.sh
```

### `pip install` がネットワーク/SSL エラーで失敗する

サンドボックス環境やプロキシ制限のある環境では、pip の外部ネットワークアクセスがブロックされていることがあります。ネットワークアクセスが許可された端末・CI 環境（[.github/workflows/ci.yml](../../.github/workflows/ci.yml)）で再実行してください。回避策として社内ミラー等の PyPI インデックスを使う場合も、`pip install` のエラーメッセージ（SSL/証明書エラーか、名前解決エラーかなど）をまず確認してください。

## CLI の `PYTHONPATH` 関連

`apps/demo-cli` と `services/mcp-backend` はフォルダ名がケバブケース（`demo-cli` / `mcp-backend`）であり、`pip install` される Python パッケージとしては提供されていません（[ADR-0009](../decisions/0009-python-package-naming.md)、[ADR-0010](../decisions/0010-industry-pack-plugin-loading.md)）。そのため、直接 `python3 -m demo_cli.cli` を実行すると `ModuleNotFoundError: No module named 'demo_cli'` になります。

- Demo CLI は必ず [scripts/demo/run-demo-cli.sh](../../scripts/demo/run-demo-cli.sh) 経由で実行してください。このスクリプトが `PYTHONPATH` にリポジトリルート・`apps/demo-cli`・`services/mcp-backend` を追加してから起動します。
- pytest 経由のテストでは `pyproject.toml` の `[tool.pytest.ini_options]` にある `pythonpath = [".", "apps/demo-cli", "services/mcp-backend"]` が同じ役割を果たすため、追加設定は不要です。
- 手動で Python REPL やスクリプトから `demo_cli` / `mcp_backend` を import したい場合は、同様に `PYTHONPATH` を設定してください。

## `ruff check .` でエラーが出る

```bash
ruff check .          # 検出のみ
ruff check . --fix    # 自動修正可能なものを修正
```

`pyproject.toml` の `[tool.ruff]`（`line-length = 110`, `target-version = "py311"`）に従います。自動修正できないルール違反（未使用変数の意図的な残存など）は手動で修正してください。`ruff` は [scripts/setup/setup.sh](../../scripts/setup/setup.sh) と CI（[.github/workflows/ci.yml](../../.github/workflows/ci.yml)）の両方で実行されます。

## `pytest` が失敗する

```bash
pytest tests/ -v
```

失敗したテスト名とトレースバックから、直近の変更箇所（`iq_platform/`、`industry-packs/*/`、`services/mcp-backend/`、`apps/demo-cli/`）を疑ってください。カテゴリ別に絞り込んで実行することもできます。

```bash
pytest tests/contract -v
pytest tests/unit -v
pytest tests/integration -v
pytest tests/security -v
pytest tests/end-to-end -v
pytest tests/evaluation -v
```

**テストを削除・無効化して成功扱いにしないでください**（[.github/copilot-instructions.md](../../.github/copilot-instructions.md)）。失敗は失敗のまま報告するのが本リポジトリの規律です。

## Live Adapter の `mode` が `unavailable` のまま/`verification_required` に進まない

Live Adapter（Work IQ / Foundry IQ / Fabric IQ / Copilot Studio）の `mode` は次のように遷移します（[ADR-0013](../decisions/0013-live-adapter-verification-required-scaffold.md)）。

| `mode` | 意味 |
|---|---|
| `unavailable` | 必要な環境変数（Entra ID 共通3項目 + Adapter 固有項目、[docs/configuration/README.md](../configuration/README.md) 参照）が不足している。`missing_fields_for()` が不足項目を返す状態 |
| `verification_required` | 必要な環境変数はすべて設定済みで、`azure-identity` による実 Entra ID 認証まで到達可能。ただし製品 API 仕様自体が未検証のため、`query()` は常に `LiveAdapterNotYetVerifiedError` を送出する |
| `live` | **現状どの Live Adapter もこの状態には到達しません。** 製品仕様が検証され、`query()` が実装されるまで意図的に到達不可にしています |

`unavailable` → `verification_required` に進めるには、[docs/setup/live-adapters-configuration.md](../setup/live-adapters-configuration.md) の手順に従って `.env` に該当 Adapter の環境変数（例: Work IQ なら `ENTRA_TENANT_ID` / `ENTRA_CLIENT_ID` / `ENTRA_CLIENT_SECRET` / `WORK_IQ_WORKSPACE_ID`）を設定し、`./scripts/demo/run-demo-cli.sh health` で状態を再確認してください。`verification_required` から `live` に進める作業（製品 API 統合）はこのリポジトリではまだ行われていません。

## `azd`/Bicep デプロイのトラブルシューティング

MCP Backend の Azure Container Apps デプロイ（[deployment/azd/](../../deployment/azd/)、[deployment/bicep/](../../deployment/bicep/)）に関する詳細な手順・トラブルシューティングは、専用ガイド **docs/deployment/Step-by-Step-Deployment-Guide.md**（作成中）が正とする予定です。それまでの暫定的な参照先は [docs/deployment/README.md](../deployment/README.md) と [ADR-0012](../decisions/0012-mcp-backend-deployment-target.md) です。

現時点で判明している既知の制約:

- Bicep は `az bicep build` によるコンパイル検証のみ完了しており、実際の Azure サブスクリプションへの `azd up`/`azd provision` は一度も実行されていません。
- コンテナイメージは既定でプレースホルダー（`mcr.microsoft.com/azuredocs/containerapps-helloworld:latest`）のままです。実イメージをビルド・push しない限り、実際の MCP Backend は動作しません。
- Ingress は既定で内部限定（`external: false`）です。外部公開する場合は明示的な承認と設定変更が必要です。

## `cleanup` コマンドを実 azd 環境なしで安全に試す

[scripts/cleanup/cleanup-azure.sh](../../scripts/cleanup/cleanup-azure.sh)（`demo-cli cleanup` から呼び出される）は、実行前に `azd env get-values` で現在の azd 環境名を取得しようとします。

- azd 環境が一つも作成されていない場合、`azd env get-values` は何も返さず、スクリプトは「現在の azd 環境を特定できませんでした」と表示して**何も削除せずに中断（exit 1）**します。これは意図した安全側の挙動であり、実 Azure リソースが存在しない状態でこのコマンドを試すこと自体は安全です。
- 実際にリソースを削除する場合のみ、確認プロンプトで azd 環境名の入力を求められ、入力が一致しない場合も中断します。
- したがって、`azd` 自体をインストールしていない、またはログインしていない環境でも `./scripts/demo/run-demo-cli.sh cleanup` を実行して「安全に中断されること」を確認できます（ただし `azd` コマンド自体が存在しない場合は `command not found` になります。事前に `azd version` で確認してください）。

## その他

このドキュメントに載っていない問題に遭遇した場合は、新しいファイルを作らず、このファイルまたは [docs/self-guided-demo/Troubleshooting.md](../self-guided-demo/Troubleshooting.md) に追記してください（Single Source of Truth の原則、[.github/copilot-instructions.md](../../.github/copilot-instructions.md)）。
