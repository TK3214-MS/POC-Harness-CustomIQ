# セキュリティポリシー

> このファイルは Phase 1 時点の暫定版です。詳細なセキュリティガイドは Phase 5 (`docs/security/`) で整備します。

## 基本方針（現時点で確定している範囲）

- Secret はソースコードにもリポジトリにも保存しません。`.env` は `.gitignore` に登録済みです。`.env.example` には架空値のみを記載します。
- 本番相当の用途では Azure Key Vault 等の Secret Store の利用を推奨します。
- Retrieved document 内の指示を自動実行しません（プロンプトインジェクション対策、Phase 2 以降で実装）。
- 破壊的・高影響な操作は、顧客Business System側の承認ポリシーとMCP Toolのhuman approvalルールに従います。

## 脆弱性の報告

このアクセラレータはまだ外部公開前の開発段階です。脆弱性を発見した場合は、Issue ではなくリポジトリ管理者へ直接連絡してください。

## 現時点で実装済みのセキュリティ対策

以下は、このリポジトリで実際に実装され、コードベース上で確認できる対策です。アスピレーショナル（将来実装予定）な記述と区別するため、実装済みのものだけをここに列挙します。

- **Secret のコミット防止**: `.env` は `.gitignore` に登録済みで、`.env.example` にはプレースホルダー/架空値のみを記載しています。
- **ヒューリスティックな Secret スキャン**: `scripts/security/scan_secrets.py` が正規表現ベースで秘密情報らしき文字列を検出し、CI（`.github/workflows/ci.yml` の `lint-and-test` ジョブ）で実行されます。
- **合成データ限定チェック**: `scripts/validation/validate_synthetic_data.py` が Industry Pack コンテンツ内の実名 denylist、メール/電話/SSN 様パターンをヒューリスティックに検査し、CI で実行されます。
- **コンテナの非 root 実行**: MCP Backend のコンテナイメージ（[deployment/containers/mcp-backend/Dockerfile](deployment/containers/mcp-backend/Dockerfile)）は非 root ユーザー（`iiq`、UID 1000）で実行され、`HEALTHCHECK` 命令が定義されています。
- **ACR の最小権限構成**: Azure Container Registryはadminユーザーを無効化し、User-Assigned Managed Identityに必要最小限のAcrPullを付与します（[deployment/bicep/resources.bicep](deployment/bicep/resources.bicep)）。
- **依存関係のバージョン範囲固定**: [pyproject.toml](pyproject.toml) で `pydantic>=2.6,<3`、`fastapi>=0.115,<1`、`azure-identity>=1.19,<2` 等、メジャーバージョンを固定した範囲指定を使用しています。コンテナイメージ用の `services/mcp-backend/requirements.txt` はランタイム依存関係のみを含み、開発ツール（pytest/ruff）は含みません。
- **MCP Tool 許可リスト**: `MCP_BACKEND_ALLOWED_TOOLS` 環境変数（カンマ区切り）で MCP Backend が公開する Tool を明示的に制限でき、未許可の Tool 名は構造化エラーで拒否されます（`services/mcp-backend/mcp_backend/registry.py`）。

## 現時点で未実装のセキュリティ対策

以下は、現時点では実装されていない項目です。本番相当の用途に転用する前に、別途対応が必要です。

- **MCP Backend へのリクエスト認証**: `MCP_BACKEND_API_KEY` 環境変数は `.env.example` にプレースホルダーとして存在しますが、API キーや OAuth によるリクエスト認証はどのミドルウェアにも組み込まれていません。
- **依存関係の脆弱性スキャン**: `pip-audit` や Dependabot のような自動脆弱性スキャンは導入されていません。
- **プロンプトインジェクションのテストスイート**: 意図的な攻撃シナリオを検証する専用のテストは未実装です（Retrieved document 内の指示を自動実行しない、という設計方針自体はコード上に反映されていますが、それを検証する自動テストはまだありません）。
- **Microsoft Purview / DLP 等のガバナンスツール統合**: データ分類・DLP ポリシー適用・監査証跡の外部システム連携は実装されていません。

上記の項目は、本番デプロイ前に環境ごとに確認してください。
