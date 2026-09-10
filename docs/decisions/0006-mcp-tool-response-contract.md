# ADR-0006: MCP Tool response contract

- ステータス: Accepted
- 日付: 2026-09-08

## コンテキスト

指示書 §10 は、全 MCP Tool（汎用・業界別）が共通で返すべきフィールド（`tool_name`, `request_id`, `correlation_id`, `status`, `data`, `source`, `provenance`, `executed_at`, `adapter_mode`, `warnings`, `errors`, `human_approval_required`）を定義している。また破壊的・高影響な操作は dry run または承認リクエストとして実装することを求めている。

## 決定

`iq_platform/contracts/mcp_tool.py` の `MCPToolResponse`（Pydantic モデル）を、FastAPI の MCP Backend（Phase 2）における全ツールの共通レスポンス型とする。破壊的操作は実処理を行わず、`human_approval_required=True` を返すことで表現する。

## 影響

- 新しいツールを追加してもレスポンス契約は変わらない。
- FastAPI の `response_model` としてそのまま使用でき、OpenAPI スキーマも自動生成される。
