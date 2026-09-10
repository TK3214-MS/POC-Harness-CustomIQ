# ADR-0013: Live Adapter は「verification_required スキャフォールド」として実装する（Phase 4）

- ステータス: Accepted
- 日付: 2026-09-10

## コンテキスト

Phase 4 は Work IQ / Foundry IQ / Fabric IQ / Copilot Studio の Live Adapter 実装を予定しているが、これらの Microsoft 製品の存在・API 仕様・認証スコープは [docs/decisions/product-verification.md](product-verification.md) の通り未検証である。指示書 §27 は「Microsoft製品仕様を推測しない」ことを明確に求めており、実 API のリクエスト/レスポンス形状を推測して実装することは許されない。

一方で、テスト用 Azure サブスクリプションが将来利用可能になる（[docs/decisions/open-questions.md](open-questions.md) Q3/Q4）ことを見越し、実際に検証可能な部分（環境変数によるコンフィグレーション、Microsoft Entra ID 認証）は今のうちに実装しておくことには価値がある。

## 決定

Work IQ / Foundry IQ / Fabric IQ の Live Adapter を、次の性質を持つ「検証待ちスキャフォールド」として実装する。

1. **`mode` は `live` に絶対に到達しない。** 必要な環境変数（`WORK_IQ_WORKSPACE_ID` 等）が揃っていれば `verification_required`、揃っていなければ `unavailable` を返す。
2. **Microsoft Entra ID 認証は実装で行う**（`azure-identity` の `ClientSecretCredential` を使用、[iq_platform/security/entra_auth.py](../../iq_platform/security/entra_auth.py)）。これは製品固有の API 仕様ではなく、Microsoft Entra ID 自体の標準的な認証パターンであるため実装が正当化できる。
3. **OAuth スコープも「未検証」を明示的に扱う。** 各製品が実際にどの認証スコープを要求するかは不明なため、`WORK_IQ_AUTH_SCOPE` 等の環境変数の既定値は `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION` とし、この値のままでは認証テストを試行せず、その旨を `health_check()` で明示する。Microsoft Graph の `.default` 等、それらしいスコープを勝手に補完しない。
4. **`query()` は常に `LiveAdapterNotYetVerifiedError` を送出する。** 認証に成功しても、製品 API のリクエスト/レスポンス形状が未検証である限り、実際のエンドポイントには一切アクセスしない。
5. Copilot Studio については、専用の Adapter クラスは作らない（Harness/Orchestrator であり IQ レイヤー Adapter ではないため）。設定値の存在確認のみ Demo CLI の `health` コマンドに追加する。

## 検証状況

- `iq_platform/adapters/live_base.py` を継承する3つの Live Adapter（`WorkIQLiveAdapter`, `FoundryIQLiveAdapter`, `FabricIQLiveAdapter`）を実装。
- `tests/unit/test_live_adapters.py` で、設定欠如時の `unavailable`、設定完了時でもスコープ未設定なら認証を試行しないこと、スコープ設定済みで認証成功/失敗した場合の挙動、`query()` が常に例外を送出することを検証（Entra ID のトークン取得はモック化し、実ネットワーク呼び出しは一切行わない）。
- 実際の Microsoft Entra ID テナントに対する認証テストは実施していない（本開発環境に実テナント/クライアントシークレットがないため）。テスト用 Azure サブスクリプションが利用可能になった時点で、[docs/setup/live-adapters-configuration.md](../setup/live-adapters-configuration.md) の手順に従って `.env` に実値を設定し、`demo-cli health` で確認できる。

## 影響

- Capability Registry (`config/capabilities.yaml`) の `work_iq` / `foundry_iq` / `fabric_iq` / `harness.copilot_studio` エントリの `status` は引き続き `Unknown` / `Verify Before Use` のまま変更しない（[ADR-0007](0007-capability-registry-authority.md) の検証済みステータス強制ルールに従う）。
- 将来、実際の API 仕様が確認できた時点で、`BaseLiveAdapter.query()` をオーバーライドして実際のリクエスト/レスポンス処理を実装し、`mode` を `live` に昇格させる変更を行う。その際は必ず [docs/decisions/product-verification.md](product-verification.md) を更新し、`last_verified_date` と実際のドキュメント参照を記録すること。
