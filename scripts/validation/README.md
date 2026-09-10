# scripts/validation/

Industry Pack schema 検証、合成データ検証（実名 denylist、メール/電話パターンスキャン等、instruction §23）。

**状態: 実装済み（Phase 6）。** [validate_synthetic_data.py](validate_synthetic_data.py) が `industry-packs/` 配下を実名 denylist・非予約メールドメイン・電話番号様パターン・SSN様パターンでスキャンする（CI で実行）。Industry Pack schema 検証自体は `demo-cli validate`（[apps/demo-cli/](../../apps/demo-cli/)）で実装済み。ヒューリスティックなスキャンであり、完全な保証ではない（instruction §23、手動レビューと併用）。
