# ADR-0007: Capability Registry を Microsoft 製品状態の唯一の真実の情報源とする

- ステータス: Accepted
- 日付: 2026-09-08

## コンテキスト

指示書 §7 は Capability Registry (`config/capabilities.yaml`) を Microsoft 機能の状態管理の場として要求している。また §27 の運用ルールは「不明な内容を確定情報として書かない」ことを求めている。実際の運用では、誰かが十分な確認をせずに `status` を `GA` に書き換えてしまうリスクがある。

## 決定

`config/capabilities.yaml` を Capability Registry の実体とし、`iq_platform.contracts.capability.CapabilityRegistry` / `Capability`（Pydantic モデル）で検証する。`Capability` に `model_validator` を実装し、`status` が `GA` / `Preview` / `Private Preview` の場合は次を必須とする。

- `last_verified_date` が `null` でないこと
- `documentation_reference` に `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION` という文字列を含まないこと

満たさない場合はロード時に `ValidationError` を送出する。

## 影響

- 未検証のまま `status` を昇格させても、スキーマ検証で機械的に弾かれる（`tests/contract/test_capability_registry_schema.py` で検証）。
- 検証プロセス自体は [docs/decisions/product-verification.md](../decisions/product-verification.md) に従う。
- Fabric IQ / Fabric Data Agent / Fabric IQ Ontology MCP のような類似機能は、指示書 §5.4 の指示通り、別々の `capability_id` として登録し、1つの機能にまとめない。
