# tests/validation/

ドキュメント間のリンク整合性検証テスト。`scripts/validation/check_doc_links.py`（リポジトリ内の全 Markdown ファイルから相対リンクを抽出し、リンク先が実在するかを検証するスクリプト）をラップして、通常のテストスイート・CI からも実行されるようにする。

**状態: 実装済み。** `pytest tests/validation/ -v` で実行可能。
