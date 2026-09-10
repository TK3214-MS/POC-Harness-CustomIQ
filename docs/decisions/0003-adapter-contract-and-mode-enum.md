# ADR-0003: Adapter contract と mode enum

- ステータス: Accepted
- 日付: 2026-09-08

## コンテキスト

指示書 §6.1 は、全 IQ レイヤー Adapter（Work Context / Knowledge / Semantic / MCP Tool）が共通インターフェース (`health_check`, `capabilities`, `mode`, `query`, `validate_configuration`, `get_diagnostics`) を持つことを要求している。また mode は `live` / `mock` / `simulated` / `unavailable` / `verification_required` の5値のいずれかとされている。

## 決定

`iq_platform/contracts/adapter.py` に抽象基底クラス `Adapter`（Python `abc.ABC`）を定義し、上記6メソッド（`mode` はプロパティ）を抽象メソッドとする。mode は `iq_platform/contracts/capability.py` に定義する共有 Enum `AdapterMode` とし、Capability Registry (`Capability.supported_modes`) と Adapter 実装の両方から同じ Enum を参照する。

Adapter は認証エラー等が発生しても mode を実行時に無言で変更しない。呼び出し側が `health_check()` / `get_diagnostics()` を見て理由を判断する。

## 影響

- 6つのメソッドをすべて実装しない具象クラスは、Python の ABC の仕組みにより `TypeError` でインスタンス化できない（`tests/contract/test_adapter_contract.py` で検証）。
- 新しい Adapter（例: Phase 4 の Live Adapter）を追加する際は、必ずこの ABC を継承する。
