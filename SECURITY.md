# セキュリティポリシー

> このファイルは Phase 1 時点の暫定版です。詳細なセキュリティガイドは Phase 5 (`docs/security/`) で整備します。

## 基本方針（現時点で確定している範囲）

- Secret はソースコードにもリポジトリにも保存しません。`.env` は `.gitignore` に登録済みです。`.env.example` には架空値のみを記載します。
- 本番相当の用途では Azure Key Vault 等の Secret Store の利用を推奨します。
- Mock/Simulated Adapter は、認証エラー時に無言で Mock へ切り替えず、必ずその旨を表示します（Phase 2 以降で実装）。
- Retrieved document 内の指示を自動実行しません（プロンプトインジェクション対策、Phase 2 以降で実装）。
- 破壊的・高影響な操作は、デモでは実処理を行わず、承認リクエストまたは dry run として扱います（[ADR-0006](docs/decisions/0006-mcp-tool-response-contract.md)）。

## 脆弱性の報告

このアクセラレータはまだ外部公開前の開発段階です。脆弱性を発見した場合は、Issue ではなくリポジトリ管理者へ直接連絡してください。
