# ADR-0005: Agent Response contract

- ステータス: Accepted
- 日付: 2026-09-08

## コンテキスト

指示書 §13 は、全業界・全実行モード共通の最終回答スキーマ（14項目: Executive Summary から Trace/Correlation ID まで）を要求している。実データと Mock データが混在する場合はラベル付けを必須としている。

## 決定

`iq_platform/contracts/agent_response.py` の `AgentResponse`（Pydantic モデル）を、全 Industry Pack・全実行モードで共通利用する唯一のレスポンス契約とする。`mock_or_simulation_disclosure` と `responsible_ai_notice` は必須フィールド（デフォルト値なし）とし、省略した回答オブジェクトは構築できない。

## 影響

- Orchestrator（Phase 2 で実装）は、必ずこのモデルを経由して最終回答を組み立てる。
- Mock/Simulation の開示を「うっかり忘れる」実装ミスを、型レベルで防止する。
