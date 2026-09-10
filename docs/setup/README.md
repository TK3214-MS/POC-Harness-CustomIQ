# セットアップガイド

このガイドは、このリポジトリを自分の環境で動かし始めるための最小手順をまとめたものです。ここに書かれている手順は Local Preview Mode（Mock/Simulated Adapter のみを使い、Microsoft SaaS サービスには一切接続しない）を対象としています。

## 前提条件

- **Python 3.11 以上**（[ADR-0002](../decisions/0002-python-primary-language.md)）。`python3 --version` で確認してください。システムの `python3` が古い場合は、`PYTHON_BIN` 環境変数で別のインタープリタを指定できます（後述）。
- **git**（リポジトリの取得に使用）。
- Azure サブスクリプションや Microsoft 365 テナントは **不要**です（Local Preview Mode のみを試す場合）。実 Azure へのデプロイや Live Adapter の設定を行う場合は、それぞれ後述のリンク先を参照してください。

## クローンとセットアップ

### 方法1: `setup` コマンドを使う（推奨）

```bash
git clone <このリポジトリの URL>
cd POC-Harness-CustomIQ
./scripts/demo/run-demo-cli.sh setup
```

`setup` サブコマンドは内部で [scripts/setup/setup.sh](../../scripts/setup/setup.sh) を呼び出します。このスクリプトは次の処理を行います。

1. `.venv` が存在しなければ作成する（既に存在する場合はそのまま再利用するため、**何度実行しても安全**です）。
2. `pip install -e ".[dev]"` で本リポジトリを editable モードでインストールする。
3. `ruff check .` と `pytest tests/ -q` を実行し、環境が正しくセットアップされたことを確認する。

デフォルトの Python インタープリタは `python3` です。システムの `python3` が 3.11 未満の場合はエラーになるため、その場合は次のように別のインタープリタを指定してください。

```bash
PYTHON_BIN=/opt/homebrew/bin/python3.12 ./scripts/demo/run-demo-cli.sh setup
```

セットアップ完了後は、新しいシェルでは次のコマンドで仮想環境を再度有効化してください。

```bash
source .venv/bin/activate
```

### 方法2: 手動セットアップ

```bash
git clone <このリポジトリの URL>
cd POC-Harness-CustomIQ
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
ruff check .
pytest tests/ -v
```

両方の方法は最終的に同じ状態になります。CI（`.github/workflows/ci.yml` の `lint-and-test` ジョブ）でも同じ `ruff check .` / `pytest tests/ -v` の手順を実行しています。

## セットアップが成功したことを確認する（`health` コマンド）

```bash
./scripts/demo/run-demo-cli.sh health
```

`health` コマンドは次の情報を表示します。

- **Industry Pack**: 現在選択中の Industry Pack（デフォルトは `manufacturing`）の manifest が正しく読み込めているか（`Ready` / `NOT READY`）。
- **Work IQ (simulated)** / **Foundry IQ (mock)** / **Fabric IQ (mock)** / **MCP Backend**: Local Preview Mode で使用する Mock/Simulated Adapter の状態。すべて `Ready` と表示されればセットアップは成功です。
- **Live Adapters** セクション: Work IQ / Foundry IQ / Fabric IQ（live）と Copilot Studio harness の設定状態。`.env` を用意していない状態では `unavailable`（`Missing required configuration: [...]`）と表示されるのが正常です。これは失敗ではなく、Live Adapter 用の環境変数を設定していないことを示しているだけです。

`health` の出力末尾には、Local Preview Mode が Microsoft SaaS サービスの可用性・挙動・セキュリティ・ライセンス・パフォーマンスを検証するものではないこと、Live Adapter がこのリポジトリでは `live` モードに到達しないことが明記されます（詳細は [ADR-0013](../decisions/0013-live-adapter-verification-required-scaffold.md)）。

続けて、5業界すべての manifest とプラグインパスの存在を検証するには次を実行します。

```bash
./scripts/demo/run-demo-cli.sh validate
```

## Industry Pack の選び方

このリポジトリには5つの Industry Pack が同梱されています。

- `manufacturing`（デフォルト）
- `financial-services`
- `retail`
- `healthcare`
- `public-sector`

Industry Pack の切り替えは、プラットフォームのコード（`iq_platform/`）を一切変更せずに行えます。切り替え方法は2通りあります。

1. **`select-industry` コマンドで永続的に切り替える**（以後の `load-data` / `run-demo` 等が対象を省略した場合にこの選択を使う）:
   ```bash
   ./scripts/demo/run-demo-cli.sh select-industry retail
   ./scripts/demo/run-demo-cli.sh run-demo
   ```
2. **各コマンドの `--industry` フラグでその場だけ切り替える**（選択状態は変更されない）:
   ```bash
   ./scripts/demo/run-demo-cli.sh run-demo --industry healthcare
   ```

その他の代表的なコマンドの流れは次のとおりです（詳細は各コマンドの `--help` を参照してください）。

```bash
./scripts/demo/run-demo-cli.sh load-data --industry financial-services --scale demo
./scripts/demo/run-demo-cli.sh run-demo --industry financial-services
./scripts/demo/run-demo-cli.sh evaluate --industry financial-services
./scripts/demo/run-demo-cli.sh generate-summary
./scripts/demo/run-demo-cli.sh reset
```

30分のセルフガイドデモとしてこれらのコマンドを一通り体験したい場合は、[docs/self-guided-demo/README.md](../self-guided-demo/README.md) から開始してください。

## この先に進みたい場合

- **Live Adapter（Work IQ / Foundry IQ / Fabric IQ / Copilot Studio）を設定したい**場合は、[docs/setup/live-adapters-configuration.md](live-adapters-configuration.md) を参照してください。Microsoft Entra ID アプリ登録の手順は今すぐ実施可能ですが、各製品固有の手順の多くは製品仕様が未検証のため `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION` のままです。Live Adapter は設定を完了しても `verification_required` までしか到達せず、`query()` は常に例外を送出します（実 API 統合は未実装、[ADR-0013](../decisions/0013-live-adapter-verification-required-scaffold.md)）。
- **実際に Azure へデプロイしたい**場合は、[docs/deployment/Step-by-Step-Deployment-Guide.md](../deployment/Step-by-Step-Deployment-Guide.md) を参照してください。MCP Backend 用の azd/Bicep 構成は用意されていますが、実 Azure サブスクリプションに対する `azd up` の実行自体はまだ検証されていません。
- 動作しなかった場合や既知の制限事項を確認したい場合は、[docs/FAQ.md](../FAQ.md) と [docs/Known-Limitations.md](../Known-Limitations.md) を参照してください。
