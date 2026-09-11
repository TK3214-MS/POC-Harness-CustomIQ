# scripts/setup/

環境セットアップ用スクリプト（`setup` コマンド、instruction §28）。

**状態: 実装済み。** [setup.sh](setup.sh) は`.venv`の作成、`pip install -e ".[dev]"`、`ruff check .`、`pytest tests/ -q`を実行します。`PYTHON_BIN`でPython実行ファイルを指定できます。ネットワーク接続が必要です。
