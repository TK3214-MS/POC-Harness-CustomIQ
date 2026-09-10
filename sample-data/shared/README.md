# sample-data/shared/

全 Industry Pack 共通で使うサンプルデータ生成ロジック・共通フィクスチャ。

**状態: 未実装（Phase 2 で実装予定）**

[docs/decisions/assumptions.md](../../docs/decisions/assumptions.md) の A11 の通り、各エンティティ種別ごとに数千件規模の合成データを生成する方針です。合成データ検証（実在企業名・実在人物名等の denylist スキャン等）は instruction §23 に従い、`scripts/validation/` で実施します。
