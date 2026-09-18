# コントリビューションガイド

[![日本語](https://img.shields.io/badge/%E3%81%82-%E6%97%A5%E6%9C%AC%E8%AA%9E-087F8C?style=for-the-badge)](CONTRIBUTING.md) [![English](https://img.shields.io/badge/A-English-5B6670?style=for-the-badge)](CONTRIBUTING.en.md)

## 開発の進め方

1. 大きな設計判断は、変更対象のドキュメントまたはコードの近くに記録してください。
2. Microsoft製品の仕様・ライセンス・価格・リージョン・GA/Preview状態を推測で確定情報として書かないでください。不明な場合は `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION` と明記してください。
3. 未解決事項は、本番環境構築ガイドの対象手順に追記してください。
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

- 実装言語は Python 3.11+ に統一します。
- Pythonパッケージ名は標準ライブラリの`platform`と衝突しない名前を使用します。
- Lint は `ruff` を使用します。

## テストの追加方針

このリポジトリのテストは`tests/`配下に5つのカテゴリで分かれています。変更内容に応じて、少なくとも次のいずれかにテストを追加・更新してください。

- `tests/contract/` — Industry Pack Manifest、MCP Tool Response、Capability Registry、ラボ用データとエージェント指示の契約を変更した場合。
- `tests/unit/` — 個別のクラス・関数（現在はIndustry Pack loaderなど）の単体挙動を変更・追加した場合。
- `tests/integration/` — 複数コンポーネントを組み合わせた挙動（例: MCP Backend と Industry Pack の連携）を変更した場合。
- `tests/security/` — Secret スキャンや合成データ検証など、セキュリティ関連スクリプトの挙動を変更した場合。
- `tests/validation/` — Markdownリンクなどrepository全体の静的検証を変更した場合。

新しい Industry Pack を追加する場合は、`manifest.yaml`、`mcp_tools_path`、Tool契約、関連する契約テストを追加してください。実際の利用・接続手順は[本番環境構築ガイド](docs/Production-Environment-Setup.md)を参照してください。

## 提出前の検証ループ

Pull Request を出す前に、少なくとも次のコマンドをすべてローカルで成功させてください（CI の `lint-and-test` ジョブと同等の内容です）。

```bash
ruff check .
pytest tests/ -v
python3 scripts/security/scan_secrets.py
python3 scripts/validation/validate_synthetic_data.py
```

いずれかが失敗する場合は、テストを削除・無効化して成功扱いにせず、失敗の原因を修正するか、回答で正直に報告してください。
