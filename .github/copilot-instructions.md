# GitHub Copilot 向けリポジトリ指示書

このファイルはこのリポジトリで作業する GitHub Copilot（開発ツールとしての Copilot。Microsoft Copilot Studio 上の "GitHub Copilot harness" とは別物）に向けた永続的な作業ルールです。

## プロジェクトの一言要約

複数業界へIndustry Packを差し替えて展開できるEnterprise Intelligence Platformアクセラレータ。詳細は[README.md](../README.md)と[本番環境構築ガイド](../docs/Production-Environment-Setup.md)を参照する。

## 絶対に守ること

1. **Microsoft 製品の仕様・ライセンス・価格・リージョン・GA/Preview 状態を推測で確定情報として書かない。** 不明な場合は `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION` と書く。
2. **SaaS側の構成とCopilot Studio側の接続を本番環境構築ガイドに反映する。**
3. **未実装の機能を完成済みとして README やドキュメントに書かない。**
4. **テストを削除・無効化して成功扱いにしない。** 失敗したテストはそのまま報告する。
5. **大きな設計判断と未解決事項は、本番環境構築ガイドまたは関連する現行文書に記録する。**
6. **ドキュメントは日本語で書く。**

## 技術的な規約

- 実装言語はPython 3.11+に統一する。
- 全Industry Packの`manifest.yaml`は`IndustryPackManifest`で検証する。
- 全MCP Toolレスポンスは`MCPToolResponse`を使う。
- Capability Registry (`config/capabilities.yaml`)をMicrosoft製品状態の記録として更新する。

## テスト

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
ruff check .
pytest
```

コードを変更したら、関連する `tests/contract/` のテストを実行してから完了と報告すること。
