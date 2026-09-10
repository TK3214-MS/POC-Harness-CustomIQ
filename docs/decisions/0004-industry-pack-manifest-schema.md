# ADR-0004: Industry Pack manifest スキーマ

- ステータス: Accepted
- 日付: 2026-09-08

## コンテキスト

指示書 §8 は、各 Industry Pack の `manifest.yaml` に含めるべきフィールド一覧（`id`, `display_name`, `version`, ... `prohibited_actions`, `human_approval_rules`）と、JSON Schema または Pydantic model による検証を要求している。

## 決定

`iq_platform/contracts/manifest.py` の `IndustryPackManifest`（Pydantic モデル）を唯一のスキーマ定義とする。5業界すべての `manifest.yaml` は、ロード時にこのモデルで検証する（Phase 3 で実装）。`human_approval_rules` は `action` / `reason` / `required_approver_role` を持つ `HumanApprovalRule` のリストとする。

## 影響

- フィールドを追加・変更する場合は、このモデルと対応する Contract テストのみを更新すればよく、業界ごとに個別スキーマを持たない。
- JSON Schema が必要な場面（外部ツール連携等）では `IndustryPackManifest.model_json_schema()` から動的に生成する。
