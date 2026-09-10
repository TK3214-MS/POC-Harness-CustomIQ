# scripts/setup/

環境セットアップ用スクリプト（`setup` コマンド、instruction §28）。

**状態: 実装済み。** [setup.sh](setup.sh) は `.venv` の作成（存在すれば再利用）、`pip install -e ".[dev]"`、`ruff check .`、`pytest tests/ -q` を順に実行し、成功時は次のコマンド例を表示します。`PYTHON_BIN` 環境変数で使用する Python 実行ファイルを上書きできます（システムの `python3` が 3.11 未満の場合に使用）。`apps/demo-cli` の `setup` コマンドから呼び出されます。ネットワーク接続が必要です（PyPI へのアクセス）。
