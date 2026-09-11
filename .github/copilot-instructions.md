# GitHub Copilot 向けリポジトリ指示書

このファイルはこのリポジトリで作業する GitHub Copilot（開発ツールとしての Copilot。Microsoft Copilot Studio 上の "GitHub Copilot harness" とは別物）に向けた永続的な作業ルールです。

## プロジェクトの一言要約

複数業界へ Industry Pack の差し替えだけで展開できる Enterprise Intelligence Platform アクセラレータ。詳細: [README.md](../README.md)、[docs/architecture/architecture-guide.md](../docs/architecture/architecture-guide.md)。

## 絶対に守ること

1. **Microsoft 製品の仕様・ライセンス・価格・リージョン・GA/Preview 状態を推測で確定情報として書かない。** 不明な場合は `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION` と書き、[docs/decisions/product-verification.md](../docs/decisions/product-verification.md) に追記する。
2. **Mock/Simulated/Live の状態を必ず明示する。** コード・ログ・回答スキーマのどこかで隠れて Live として扱わない。
3. **未実装の機能を完成済みとして README やドキュメントに書かない。**
4. **テストを削除・無効化して成功扱いにしない。** 失敗したテストはそのまま報告する。
5. **大きな設計判断は ADR ([docs/decisions/](../docs/decisions/)) に記録する。**
6. **未解決事項は新しいファイルを作らず、既存の [open-questions.md](../docs/decisions/open-questions.md) に追記する。製品仕様は [product-verification.md](../docs/decisions/product-verification.md) に追記する。**
7. **一度に大規模な変更をせず、フェーズ単位（Phase 0〜6、[docs/decisions](../docs/decisions/) 参照）で実装する。**
8. **ドキュメントは日本語で書く**（[Q1 の回答](../docs/decisions/open-questions.md) により確定）。

## 技術的な規約

- 実装言語は Python 3.11+ に統一（[ADR-0002](../docs/decisions/0002-python-primary-language.md)）。
- トップレベル Python パッケージ名は `platform` ではなく `iq_platform` を使う。標準ライブラリの `platform` モジュールと衝突するため（[ADR-0009](../docs/decisions/0009-python-package-naming.md)）。
- 全 Industry Pack の `manifest.yaml` は `iq_platform.contracts.manifest.IndustryPackManifest` で検証する（[ADR-0004](../docs/decisions/0004-industry-pack-manifest-schema.md)）。
- 全 MCP Tool レスポンスは `iq_platform.contracts.mcp_tool.MCPToolResponse` を使う（[ADR-0006](../docs/decisions/0006-mcp-tool-response-contract.md)）。
- Capability Registry (`config/capabilities.yaml`) が Microsoft 製品状態の唯一の真実の情報源（[ADR-0007](../docs/decisions/0007-capability-registry-authority.md)）。

## テスト

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
ruff check .
pytest
```

コードを変更したら、関連する `tests/contract/` のテストを実行してから完了と報告すること。
