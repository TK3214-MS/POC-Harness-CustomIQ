# ADR-0002: 実装言語は Python に統一する

- ステータス: Accepted
- 日付: 2026-09-08

## コンテキスト

MCP Backend は指示書で FastAPI（Python）が明示されている。Orchestrator / Adapters / CLI / テストスイートの言語は明示されていなかったため、[docs/decisions/open-questions.md](../decisions/open-questions.md) の Q2 としてステークホルダーに確認した。回答: 「全て Python でお願いします」（2026-09-08）。

## 決定

`iq_platform/`（契約・Capability Registry）、`services/mcp-backend/`（MCP Backend）、`tests/`をPython 3.11+で実装する。

## 影響

- 単一言語のため、契約（Pydantic モデル）を Python 側でのみ真実の情報源として保持できる。
- 依存関係管理は `pyproject.toml` に一本化する。
- パッケージ命名の詳細（標準ライブラリとの衝突回避）は [ADR-0009](0009-python-package-naming.md) を参照。
