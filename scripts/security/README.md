# scripts/security/

Secret scanningなど、security validation用スクリプトを配置します。

**実装済み:** [scan_secrets.py](scan_secrets.py)はヒューリスティックな正規表現ベースのSecret検出スクリプトで、CIから実行されます。

**未実装:** 依存関係の脆弱性スキャンとプロンプトインジェクション専用テスト。静的解析はRuffをCIで実行します。
