# scripts/setup/

[![日本語](https://img.shields.io/badge/%E3%81%82-%E6%97%A5%E6%9C%AC%E8%AA%9E-087F8C?style=for-the-badge)](README.md) [![English](https://img.shields.io/badge/A-English-5B6670?style=for-the-badge)](README.en.md)

環境セットアップ用スクリプト（`setup` コマンド、instruction §28）。

**状態: 実装済み。** [setup.sh](setup.sh) は`.venv`の作成、`pip install -e ".[dev]"`、`ruff check .`、`pytest tests/ -q`を実行します。`PYTHON_BIN`でPython実行ファイルを指定できます。ネットワーク接続が必要です。
