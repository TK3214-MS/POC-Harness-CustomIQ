# Observability ガイド

本アクセラレータにおける Observability（可観測性）の現在の実装状況をまとめます。横断的関心事としての Observability の位置づけは [アーキテクチャガイド §2.4](../architecture/architecture-guide.md) を参照してください。

## 1. 実装済み: correlation_id 付き構造化ロギング

`iq_platform/observability/logging_config.py` は、`correlation_id` を全ログレコードに付与する最小限のロギング設定を提供します（[iq_platform/observability/logging_config.py](../../iq_platform/observability/logging_config.py)）。

- `configure_logging()` は、`correlation_id` を含むフォーマット文字列（`%(asctime)s %(levelname)s %(name)s [correlation_id=%(correlation_id)s] %(message)s`）を持つ `logging.StreamHandler` をルートロガーに設定します。
- 実装は `logging.setLogRecordFactory()` ではなく、カスタムの `logging.Formatter` サブクラス（`_CorrelationIdFormatter`）を使っています。これは、呼び出し側が既に `extra={"correlation_id": ...}` を渡している場合、`LogRecordFactory` で事前に `correlation_id` 属性をレコードに設定していると Python の `logging` モジュールが `KeyError` を送出してしまう競合を避けるためです。`correlation_id` が未設定のレコードには `"-"` を補います。
- `iq_platform/orchestration/generic_orchestrator.py` は、シナリオ実行の開始・完了ログに `AgentResponse.trace_or_correlation_id` と同一の `correlation_id` を付与します。
- この挙動は [tests/integration/test_correlation_id_logging.py](../../tests/integration/test_correlation_id_logging.py) で `caplog` を用いて検証済みです。同テストは、シナリオ実行中に出力されるログレコードのうち、レスポンスの `trace_or_correlation_id` と一致する `correlation_id` を持つものが存在すること、かつ「開始」「完了」を示すログがそれぞれ存在することを確認します。

## 2. 未実装: Application Insights / Azure Monitor 連携（明示的な TBD）

**Application Insights / Azure Monitor との統合は現時点で実装されていません。** `.env.example` の `APPLICATIONINSIGHTS_CONNECTION_STRING` はプレースホルダーの環境変数として存在するのみで、いずれのコード（`iq_platform/observability/logging_config.py` を含む）にもエクスポーター（OpenTelemetry Exporter やその他の Application Insights SDK）として配線されていません。

これはギャップとして明示します。ダッシュボード・アラート・メトリクスについても同様に未実装です。

## 3. 実デプロイに向けて追加が必要な項目（すべて今後の作業）

- **エクスポーターの配線**: `APPLICATIONINSIGHTS_CONNECTION_STRING` を実際に読み取り、ログ・トレース・メトリクスを Application Insights（または OpenTelemetry 互換の別バックエンド）へ送信するエクスポーターの実装。Microsoft 製品固有の統合方法・SDK バージョン・GA/Preview 状況は `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`（[docs/decisions/product-verification.md](../decisions/product-verification.md)）。
- **ダッシュボード**: シナリオ実行回数、Tool 呼び出し成否、Adapter の `mode` 遷移などを可視化するダッシュボードの設計・実装。
- **アラート**: エラー率上昇や Live Adapter 認証失敗などを検知するアラートルールの設計・実装。

これらはすべて今後の作業であり、現時点で「実装済み」として扱わないでください。実装が進んだ際は、対応するコード・テストへのリンクとともに本ページを更新してください。
