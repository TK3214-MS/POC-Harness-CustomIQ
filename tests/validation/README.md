# tests/validation/

[![日本語](https://img.shields.io/badge/%E3%81%82-%E6%97%A5%E6%9C%AC%E8%AA%9E-087F8C?style=for-the-badge)](README.md) [![English](https://img.shields.io/badge/A-English-5B6670?style=for-the-badge)](README.en.md)

ドキュメント間のリンク整合性検証テスト。`scripts/validation/check_doc_links.py`（リポジトリ内の全 Markdown ファイルから相対リンクを抽出し、リンク先が実在するかを検証するスクリプト）をラップして、通常のテストスイート・CI からも実行されるようにする。

**状態: 実装済み。** `pytest tests/validation/ -v` で実行可能。
