# Prerequisites（前提条件）

## 必須（Local Preview Mode）

- Python 3.11 以上（このリポジトリでの検証環境: Python 3.14）
- `git`
- ターミナル操作の基本知識
- リポジトリのクローン

macOS の場合、システム標準の `python3` が古い可能性があります（このリポジトリの開発環境では 3.9.6 でした）。`python3 --version` で 3.11 未満の場合は Homebrew 等で新しい Python をインストールしてください（例: `brew install python@3.12`）。

## セットアップ

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest tests/ -v
```

`pytest tests/` が全て成功することを確認してから先に進んでください（2026-09-10 時点で 64 件成功）。

## Hybrid Mode / Full SaaS Mode を試す場合（任意、Local Preview では不要）

- テスト用 Azure サブスクリプションへのアクセス
- Microsoft Entra ID テナント管理者権限（アプリ登録用）
- Copilot Studio / Work IQ / Foundry IQ / Fabric IQ へのアクセス（[docs/decisions/product-verification.md](../decisions/product-verification.md) の通り、これらの製品仕様は本リポジトリでは未検証です）

詳細は [docs/setup/live-adapters-configuration.md](../setup/live-adapters-configuration.md) を参照してください。

## 知識レベル

Microsoft 製品の深い知識は不要です。このデモは Local Preview Mode を前提としており、CLI コマンドの実行と出力の読み方が分かれば十分です。
