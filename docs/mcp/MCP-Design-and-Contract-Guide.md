# MCP 設計・契約ガイド

[![日本語](https://img.shields.io/badge/%E3%81%82-%E6%97%A5%E6%9C%AC%E8%AA%9E-087F8C?style=for-the-badge)](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/docs/mcp/MCP-Design-and-Contract-Guide.md) [![English](https://img.shields.io/badge/A-English-5B6670?style=for-the-badge)](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/docs/mcp/MCP-Design-and-Contract-Guide.en.md)

## 1. MCPToolResponse 契約

すべてのMCP Toolは、共通のレスポンス型`iq_platform.contracts.mcp_tool.MCPToolResponse`（Pydanticモデル）を返します。フィールドは次のとおりです。

| フィールド | 型 | 内容 |
| --- | --- | --- |
| `tool_name` | `str` | 呼び出された Tool 名。 |
| `request_id` | `str` | このリクエスト固有の ID（未指定時は自動生成される UUID）。 |
| `correlation_id` | `str` | 呼び出し元から伝播される相関 ID。未指定時は `request_id` と同値になる。 |
| `status` | `str` | `"ok"` または `"error"`。 |
| `data` | `dict[str, Any]` | Tool 実行結果のペイロード。 |
| `source` | `str` | レスポンスの出処ラベル（例: `mcp_backend:manufacturing`）。 |
| `provenance` | `list[str]` | データの来歴情報。 |
| `executed_at` | `datetime` | 実行日時（UTC）。 |
| `adapter_mode` | `AdapterMode` | `live`または`unavailable`。本番MCP Backendの実行状態を表す。 |
| `warnings` | `list[str]` | 警告メッセージ一覧。 |
| `errors` | `list[str]` | エラーメッセージ一覧。 |
| `human_approval_required` | `bool` | このアクションの実施に人間承認が必要かどうか。 |

破壊的・高影響な操作は、実処理を行わずに `human_approval_required=True` を返すことで表現します（instruction §10 準拠）。

## 2. ToolRegistry の設計

`services/mcp_backend/mcp_backend/registry.py::ToolRegistry`（[実装](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/services/mcp-backend/mcp_backend/registry.py)）は、1つの Industry Pack が公開する Tool 群を保持し、共通の呼び出し処理を提供します。

- コンストラクタは `dataset`（合成データセット）、`tool_functions`（`tool_name -> Callable[[dataset, params], dict]` の辞書）、`descriptions`、`adapter_mode`、`source_label`、任意の `allowed_tools`（許可リスト、[MCP-Security-Guide.md](MCP-Security-Guide.md) 参照）を受け取ります。
- `list_tools()` は許可リストでフィルタした Tool 一覧を返します。
- `invoke(tool_name, params, correlation_id=None)` は次の順序でチェックし、**どの分岐でも例外を送出せず** `MCPToolResponse` を返します。
  1. 許可リストに含まれない Tool 名 → `status="error"`、`errors=["Tool '...' is not in the allowlist for this deployment"]`。
  2. 未知の Tool 名 → `status="error"`、`errors=["Unknown tool '...'"]`。
  3. Tool 関数呼び出し時の `KeyError`（必須パラメータ欠落）を捕捉 → `status="error"`、`errors=["Missing required parameter: ..."]`。
  4. Tool 関数が返した `dict` に `"error"` キーが含まれる場合 → `status="error"`。
  5. それ以外は `status="ok"`。

この設計により、未知/不正な Tool 呼び出しがサービスをクラッシュさせたり生の例外を漏らしたりすることはありません。これは [MCP Tool safety test](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/tests/security/test_mcp_tool_safety.py) と [MCP Backend integration test](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/tests/integration/test_mcp_backend_integration.py) で検証されています。

## 3. Industry Pack ごとの Tool 宣言方法

各Industry Packの`manifest.yaml`の`mcp_tools_path`がTool実装モジュールを示します。このモジュールは`industry_pack_loader`によって実行時に動的ロードされ、`TOOL_FUNCTIONS`と`TOOL_DESCRIPTIONS`を公開します。

- `TOOL_FUNCTIONS: dict[str, Callable[[dict, dict], dict]]`
- `TOOL_DESCRIPTIONS: dict[str, str]`

`services/mcp-backend/mcp_backend/factory.py::build_app()` はこれらを読み込んで `ToolRegistry` を構築するため、`services/mcp-backend/` のコード自体には業界固有のロジックが一切含まれません。

## 4. HTTP エンドポイント（REST API、この Backend 自身の内部利用向け）

`services/mcp-backend/mcp_backend/app.py::create_app()` は次の3エンドポイントを公開する FastAPI アプリを構築します。

- `GET /health` — `{"status": "ok"}` を返す簡易ヘルスチェック。
- `GET /tools` — 現在の許可リストでフィルタされた Tool 一覧（`tool_name`/`description` の辞書配列）を返す。
- `POST /tools/{tool_name}/invoke` — `{"params": {...}, "correlation_id": "..."}` を受け取り、`ToolRegistry.invoke()` の結果である `MCPToolResponse` を `response_model` として返す。

重要な設計判断として、**Tool 呼び出しのレスポンスは常に HTTP 200 です。** エラー時も生の HTTP エラー（4xx/5xx）ではなく、`status="error"` を持つ構造化された `MCPToolResponse` の本文が返されます。これにより呼び出し元は常に同じ契約でレスポンスをパースできます（[integration test](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/tests/integration/test_mcp_backend_integration.py) の `test_invoke_unknown_tool_returns_structured_error_not_http_error` で検証済み）。

**注意**: このセクション4の REST API は Model Context Protocol の実際のワイヤーフォーマット（JSON-RPC 2.0 ベースの `initialize`/`tools/list`/`tools/call` ハンドシェイク）には準拠していません。これは本リポジトリ自身の CLI・テストが内部的に呼び出すためだけの独自形状の API であり、廃止はしませんが、Copilot Studio 等の外部の MCP クライアントはこの REST API には接続できません。実際に外部クライアントが接続する先はセクション5です。

## 5. 実プロトコル準拠の MCP サーバー（`/mcp`、外部の MCP クライアント向け）

Microsoft Copilot StudioのGitHub Copilot harnessは「Add MCP server」フローでMCPサーバーへ接続できます。このBackendは公式MCP Python SDKを使った実プロトコル準拠サーバーを`/mcp`に公開し、同じ`ToolRegistry`へ委譲します。

- **実装言語の選定理由**: Python 3.11+の既存構成を維持し、公式MCP Python SDKを採用しています。
- **Tool の入力スキーマ**: 各 Tool 関数は型付けされていない `params: dict` を受け取る設計のため、公開される JSON Schema も汎用的な `{"type": "object", "additionalProperties": true}` 相当の緩いスキーマになります。フィールド単位の型付けは行っていません。これは正直な制限であり、今後 Tool ごとに厳密なスキーマを定義する場合は各 Industry Pack の `tools/*.py` 側の拡張が必要です。
- **ホスト許可リスト**: `mcp` SDK は DNS リバインディング対策として Host/Origin ヘッダーを検証します。`MCP_BACKEND_ALLOWED_HOSTS` 環境変数（カンマ区切り）で実際のデプロイ先ホスト名を追加してください。`localhost`/`127.0.0.1`（任意ポート）と `testserver`（`fastapi.testclient.TestClient` の固定ホスト名）は常に許可されます。詳細は [MCP-Security-Guide.md](MCP-Security-Guide.md) を参照してください。
- **検証方法**:
  - [MCP protocol integration test](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/tests/integration/test_mcp_protocol_server.py) — `fastapi.testclient.TestClient` 経由で生の JSON-RPC リクエスト（`initialize` → `notifications/initialized` → `tools/list` → `tools/call`）を送り、5業界すべてで検証済み（インプロセス、高速）。
  - **未実施**: 実際の Microsoft Copilot Studio 環境からこの `/mcp` エンドポイントに接続する検証は、実 Copilot Studio 環境へのアクセスがないため未実施です。上記2つの検証は、公式 SDK ベースの MCP クライアントが正しくハンドシェイクできることを示すものであり、Copilot Studio 自身の実装の挙動を保証するものではありません。
