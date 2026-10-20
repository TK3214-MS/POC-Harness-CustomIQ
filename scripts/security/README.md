# scripts/security/

[![日本語](https://img.shields.io/badge/%E3%81%82-%E6%97%A5%E6%9C%AC%E8%AA%9E-087F8C?style=for-the-badge)](README.md) [![English](https://img.shields.io/badge/A-English-5B6670?style=for-the-badge)](README.en.md)

Secret scanningなど、security validation用スクリプトを配置します。

**実装済み:** [scan_secrets.py](scan_secrets.py)はヒューリスティックな正規表現ベースのSecret検出スクリプトで、CIから実行されます。

**実装済み:** [check_private_demo.py](check_private_demo.py)は顧客固有デモのパスと既知の同一内容コピーを検査します。
クローンごとに `python3 scripts/security/check_private_demo.py --install` を実行し、
pre-commitとpre-pushを有効にしてください。`--staged` はindex、
`--history HEAD` は到達可能な全コミットを検査します。
フックの意図的な解除や編集済みコピーは防げません。
運用と保護範囲は[本番環境構築ガイド](../../docs/Production-Environment-Setup.md#顧客固有デモデータの公開防止)を参照してください。

**未実装:** 依存関係の脆弱性スキャンとプロンプトインジェクション専用テスト。静的解析はRuffをCIで実行します。
