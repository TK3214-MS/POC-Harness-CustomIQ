# docs/security/

セキュリティガイド（instruction §24 Security Requirements の詳細版）。

Secret scanningは [scripts/security/scan_secrets.py](../../scripts/security/scan_secrets.py)で実装し、CIで実行します。Containerはnon-rootで実行します([deployment/containers/mcp-backend/Dockerfile](../../deployment/containers/mcp-backend/Dockerfile))。基本方針は[SECURITY.md](../../SECURITY.md)を参照してください。
