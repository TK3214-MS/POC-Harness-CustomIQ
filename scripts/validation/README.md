# scripts/validation/

Industry Pack schema 検証、合成データ検証（実名 denylist、メール/電話パターンスキャン等、instruction §23）。

**状態: 実装済み。** [validate_synthetic_data.py](validate_synthetic_data.py) が`industry-packs/`配下を実名denylist・非予約メールドメイン・電話番号様パターン・SSN様パターンでスキャンします(CIで実行)。完全な保証ではなく、ヒューリスティックな検査です。
