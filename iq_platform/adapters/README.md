# iq_platform/adapters/

Work Context / Knowledge / Semantic の各 Adapter 実装(`iq_platform.contracts.adapter.Adapter` を継承)。

**状態: Mock/Simulated は Phase 2 で実装済み。Live は Phase 4 で verification_required スキャフォールドとして実装済み([ADR-0013](../../docs/decisions/0013-live-adapter-verification-required-scaffold.md))。**

- `work_context/simulated_adapter.py` / `knowledge/mock_adapter.py` / `semantic/mock_adapter.py` — Mock/Simulated（実装済み）
- `work_context/live_adapter.py` / `knowledge/live_adapter.py` / `semantic/live_adapter.py` — Live（`live_base.py` の `BaseLiveAdapter` を継承。実 Entra ID 認証は実装済みだが、`mode` は決して `live` にはならず、`query()` は常に例外を送出する（製品 API 仕様が未検証のため）
