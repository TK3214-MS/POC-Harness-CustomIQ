# コントリビューションガイド

> このファイルは Phase 1 時点の暫定版です。CI/レビュー体制が固まり次第、詳細化します。

## 開発の進め方

1. 大きな設計判断は [docs/decisions/](docs/decisions/) に ADR として記録してください（テンプレートは既存の ADR ファイルを参照）。
2. 前提や未解決事項は、新しく作らず [docs/decisions/assumptions.md](docs/decisions/assumptions.md) / [docs/decisions/open-questions.md](docs/decisions/open-questions.md) に追記してください。
3. Microsoft 製品の仕様・ライセンス・価格・リージョン・GA/Preview 状態を推測で確定情報として書かないでください。不明な場合は `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION` と明記し、[docs/decisions/product-verification.md](docs/decisions/product-verification.md) に追記してください。
4. Mock/Simulated な実装には、コード・ログ・回答のいずれにも Mock であることが分かる表示を必ず含めてください。
5. 実装していない機能を README やドキュメントで完成済みと記載しないでください。
6. コミット前に該当するテストを実行し、失敗したテストを削除・無効化して成功扱いにしないでください。

## セットアップ

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
ruff check .
pytest
```

## コーディング規約

- 実装言語は Python 3.11+ に統一します（[ADR-0002](docs/decisions/0002-python-primary-language.md)）。
- パッケージ命名規則は [ADR-0009](docs/decisions/0009-python-package-naming.md) に従ってください（標準ライブラリの `platform` と衝突する名前を避ける）。
- Lint は `ruff` を使用します。
