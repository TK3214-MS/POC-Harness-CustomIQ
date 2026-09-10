# scripts/security/

Secret scanning、依存関係スキャン、静的解析、プロンプトインジェクションテスト等の実行スクリプト（instruction §22.5）。

**状態: 一部実装済み(Phase 5)。** [scan_secrets.py](scan_secrets.py) はヒューリスティックな正規表現ベースの Secret 検出スクリプト(AWS キー、秘密鍵ヘッダー、接続文字列内キー等)で、CI(`.github/workflows/ci.yml`)から実行される。依存関係スキャン・静的解析(ruff は既に CI で実行中)・プロンプトインジェクションテストは未実装(Phase 4/6 で実装予定、Adapter/Orchestrator の該当コードが増えてから)。
