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

## テストの追加方針

このリポジトリのテストは `tests/` 配下に6つのカテゴリで分かれています。変更内容に応じて、少なくとも次のいずれかにテストを追加・更新してください。

- `tests/contract/` — Pydantic 契約（Adapter、Industry Pack Manifest、MCP Tool Response、Agent Response、Capability）のスキーマ検証を変更した場合、または新しい Industry Pack の manifest を追加した場合。
- `tests/unit/` — 個別のクラス・関数（Adapter、設定読み込み、認証処理など）の単体挙動を変更・追加した場合。
- `tests/integration/` — 複数コンポーネントを組み合わせた挙動（例: MCP Backend と Industry Pack の連携）を変更した場合。
- `tests/end-to-end/` — CLI コマンドの一連の流れや、Industry Pack 切り替え時の挙動を変更した場合。
- `tests/evaluation/` — 評価エンジン（`iq_platform/evaluation/rubric_evaluator.py`）やルーブリック（`evaluations/rubric.yaml`）を変更した場合。
- `tests/security/` — Secret スキャンや合成データ検証など、セキュリティ関連スクリプトの挙動を変更した場合。

新しい Industry Pack を追加する場合は、`tests/contract/test_all_industry_packs_manifest_schema.py` と `tests/end-to-end/test_industry_pack_switching.py` に対象パックを追加する必要があります。詳細な手順は [docs/industry-packs/Industry-Pack-Guide.md](docs/industry-packs/Industry-Pack-Guide.md) を参照してください。

## 提出前の検証ループ

Pull Request を出す前に、少なくとも次のコマンドをすべてローカルで成功させてください（CI の `lint-and-test` ジョブと同等の内容です）。

```bash
ruff check .
pytest tests/ -v
python3 scripts/security/scan_secrets.py
python3 scripts/validation/validate_synthetic_data.py
```

いずれかが失敗する場合は、テストを削除・無効化して成功扱いにするのではなく、失敗の原因を修正するか、修正できない既知の制限として正直に報告してください（[docs/Known-Limitations.md](docs/Known-Limitations.md) 参照）。
