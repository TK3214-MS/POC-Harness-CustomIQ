# scripts/security/

[![日本語](https://img.shields.io/badge/%E3%81%82-%E6%97%A5%E6%9C%AC%E8%AA%9E-087F8C?style=for-the-badge)](README.md) [![English](https://img.shields.io/badge/A-English-5B6670?style=for-the-badge)](README.en.md)

Secret scanningなど、security validation用スクリプトを配置します。

**実装済み:** [scan_secrets.py](scan_secrets.py)はヒューリスティックな正規表現ベースのSecret検出スクリプトで、CIから実行されます。

**未実装:** 依存関係の脆弱性スキャンとプロンプトインジェクション専用テスト。静的解析はRuffをCIで実行します。
