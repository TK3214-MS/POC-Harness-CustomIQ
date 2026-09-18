# scripts/validation/

[![日本語](https://img.shields.io/badge/%E3%81%82-%E6%97%A5%E6%9C%AC%E8%AA%9E-087F8C?style=for-the-badge)](README.md) [![English](https://img.shields.io/badge/A-English-5B6670?style=for-the-badge)](README.en.md)

Industry Pack schema 検証、合成データ検証（実名 denylist、メール/電話パターンスキャン等、instruction §23）。

**状態: 実装済み。** [validate_synthetic_data.py](validate_synthetic_data.py) が`industry-packs/`配下を実名denylist・非予約メールドメイン・電話番号様パターン・SSN様パターンでスキャンします(CIで実行)。完全な保証ではなく、ヒューリスティックな検査です。
