# docs/security/

セキュリティガイド（instruction §24 Security Requirements の詳細版）。

**状態: 一部実装済み。** Secret scanningは [scripts/security/scan_secrets.py](../../scripts/security/scan_secrets.py) として実装し、CI で実行する。Container は non-root 実行([deployment/containers/mcp-backend/Dockerfile](../../deployment/containers/mcp-backend/Dockerfile))。Managed Identity + 最小権限(AcrPull のみ)は [ADR-0012](../decisions/0012-mcp-backend-deployment-target.md) を参照。依存関係スキャン・プロンプトインジェクションテストは未実装。現時点の基本方針は [SECURITY.md](../../SECURITY.md) を参照してください。
