# Troubleshooting（トラブルシューティング）

## `pip install -e ".[dev]"` が失敗する / SSL エラーが出る

サンドボックス環境やプロキシ制限がある場合、pip のネットワークアクセスがブロックされていることがあります。ネットワークアクセスを許可した端末で再実行してください。

## `python3 --version` が 3.11 未満

システム標準の Python が古い可能性があります。`brew install python@3.12`（macOS）等で新しい Python をインストールし、そのインタプリタで venv を作り直してください:

```bash
/opt/homebrew/bin/python3.12 -m venv .venv
```

## `./scripts/demo/run-demo-cli.sh` が `ModuleNotFoundError: No module named 'iq_platform'` 等で失敗する

`.venv` を activate せずに実行している可能性があります。`source .venv/bin/activate` を先に実行してください。

## `run-demo` の途中で `KeyError` や `AttributeError` が出る

Industry Pack のプラグインモジュール（`data/generator.py`, `tools/*.py`, `semantics/*.py`, `agents/scenario.py`）のいずれかが壊れている可能性があります。`./scripts/demo/run-demo-cli.sh validate` で該当パックのパス欠落がないか確認してください。

## Live Adapters セクションが常に `unavailable`

Local Preview Mode では正常な状態です。`.env` に Entra ID 認証情報等を設定していない限り `unavailable` のままです（[docs/setup/live-adapters-configuration.md](../setup/live-adapters-configuration.md) 参照）。

## `evaluate` で `FAIL` が出た

該当する criterion の `detail` を確認してください。もし Industry Pack のシナリオロジック（`agents/scenario.py`）を変更した直後であれば、`recommended_next_actions` に禁止フレーズ（例: "automatically freeze"）が混入していないか確認してください。

## テストが失敗する

```bash
pytest tests/ -v
```
で失敗したテスト名を確認し、直近の変更箇所（`industry-packs/`, `iq_platform/`, `services/mcp-backend/`）を疑ってください。失敗したテストを削除・無効化して成功扱いにしないでください（[.github/copilot-instructions.md](../../.github/copilot-instructions.md)）。

## その他

このセクションは Phase 6 時点の初版です。実際のデモ実施で新たに発生した問題は、このファイルに追記してください（Single Source of Truth、既存ファイルへの追記を優先）。
