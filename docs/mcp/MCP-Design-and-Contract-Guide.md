# MCP 設計・契約ガイド

## 1. MCPToolResponse 契約

すべての MCP Tool（汎用・業界固有を問わず）は、共通のレスポンス型 `iq_platform.contracts.mcp_tool.MCPToolResponse`（[iq_platform/contracts/mcp_tool.py](../../iq_platform/contracts/mcp_tool.py)、Pydantic モデル）を返します（[ADR-0006](../decisions/0006-mcp-tool-response-contract.md)）。フィールドは次のとおりです。

| フィールド | 型 | 内容 |
|---|---|---|
| `tool_name` | `str` | 呼び出された Tool 名。 |
| `request_id` | `str` | このリクエスト固有の ID（未指定時は自動生成される UUID）。 |
| `correlation_id` | `str` | 呼び出し元から伝播される相関 ID。未指定時は `request_id` と同値になる。 |
| `status` | `str` | `"ok"` または `"error"`。 |
| `data` | `dict[str, Any]` | Tool 実行結果のペイロード。 |
| `source` | `str` | レスポンスの出処ラベル（例: `mcp_backend:manufacturing`）。 |
| `provenance` | `list[str]` | データの来歴情報。 |
| `executed_at` | `datetime` | 実行日時（UTC）。 |
| `adapter_mode` | `AdapterMode` | `live`/`mock`/`simulated`/`unavailable`/`verification_required` のいずれか。 |
| `warnings` | `list[str]` | 警告メッセージ一覧。 |
| `errors` | `list[str]` | エラーメッセージ一覧。 |
| `human_approval_required` | `bool` | このアクションの実施に人間承認が必要かどうか。 |

破壊的・高影響な操作は、実処理を行わずに `human_approval_required=True` を返すことで表現します（instruction §10 準拠）。

## 2. ToolRegistry の設計

`services/mcp_backend/mcp_backend/registry.py::ToolRegistry`（[services/mcp-backend/mcp_backend/registry.py](../../services/mcp-backend/mcp_backend/registry.py)）は、1つの Industry Pack が公開する Tool 群を保持し、共通の呼び出し処理を提供します。

- コンストラクタは `dataset`（合成データセット）、`tool_functions`（`tool_name -> Callable[[dataset, params], dict]` の辞書）、`descriptions`、`adapter_mode`、`source_label`、任意の `allowed_tools`（許可リスト、[MCP-Security-Guide.md](MCP-Security-Guide.md) 参照）を受け取ります。
- `list_tools()` は許可リストでフィルタした Tool 一覧を返します。
- `invoke(tool_name, params, correlation_id=None)` は次の順序でチェックし、**どの分岐でも例外を送出せず** `MCPToolResponse` を返します。
  1. 許可リストに含まれない Tool 名 → `status="error"`、`errors=["Tool '...' is not in the allowlist for this deployment"]`。
  2. 未知の Tool 名 → `status="error"`、`errors=["Unknown tool '...'"]`。
  3. Tool 関数呼び出し時の `KeyError`（必須パラメータ欠落）を捕捉 → `status="error"`、`errors=["Missing required parameter: ..."]`。
  4. Tool 関数が返した `dict` に `"error"` キーが含まれる場合 → `status="error"`。
  5. それ以外は `status="ok"`。

この設計により、未知/不正な Tool 呼び出しがサービスをクラッシュさせたり生の例外を漏らしたりすることはありません。これは [tests/security/test_mcp_tool_safety.py](../../tests/security/test_mcp_tool_safety.py) と [tests/integration/test_mcp_backend_integration.py](../../tests/integration/test_mcp_backend_integration.py) で検証されています。

## 3. Industry Pack ごとの Tool 宣言方法

各 Industry Pack の `manifest.yaml` の `mcp_tools_path` フィールドが、その Pack の MCP Tool 実装モジュール（例: [industry-packs/manufacturing/tools/manufacturing_tools.py](../../industry-packs/manufacturing/tools/manufacturing_tools.py)）へのパスを示します。このモジュールは `iq_platform.orchestration.industry_pack_loader.load_plugin_module()` によって `importlib.util.spec_from_file_location` 経由で実行時に動的ロードされ（[ADR-0010](../decisions/0010-industry-pack-plugin-loading.md)）、以下の2つのモジュールレベル変数を公開しなければなりません。

- `TOOL_FUNCTIONS: dict[str, Callable[[dict, dict], dict]]`
- `TOOL_DESCRIPTIONS: dict[str, str]`

`services/mcp-backend/mcp_backend/factory.py::build_app()` はこれらを読み込んで `ToolRegistry` を構築するため、`services/mcp-backend/` のコード自体には業界固有のロジックが一切含まれません。

## 4. HTTP エンドポイント（REST API、この Backend 自身の内部利用向け）

`services/mcp-backend/mcp_backend/app.py::create_app()` は次の3エンドポイントを公開する FastAPI アプリを構築します。

- `GET /health` — `{"status": "ok"}` を返す簡易ヘルスチェック。
- `GET /tools` — 現在の許可リストでフィルタされた Tool 一覧（`tool_name`/`description` の辞書配列）を返す。
- `POST /tools/{tool_name}/invoke` — `{"params": {...}, "correlation_id": "..."}` を受け取り、`ToolRegistry.invoke()` の結果である `MCPToolResponse` を `response_model` として返す。

重要な設計判断として、**Tool 呼び出しのレスポンスは常に HTTP 200 です。** エラー時も生の HTTP エラー（4xx/5xx）ではなく、`status="error"` を持つ構造化された `MCPToolResponse` の本文が返されます。これにより呼び出し元は常に同じ契約でレスポンスをパースできます（[tests/integration/test_mcp_backend_integration.py](../../tests/integration/test_mcp_backend_integration.py) の `test_invoke_unknown_tool_returns_structured_error_not_http_error` で検証済み）。

**注意**: このセクション4の REST API は Model Context Protocol の実際のワイヤーフォーマット（JSON-RPC 2.0 ベースの `initialize`/`tools/list`/`tools/call` ハンドシェイク）には準拠していません。これは本リポジトリ自身の CLI・テストが内部的に呼び出すためだけの独自形状の API であり、廃止はしませんが、Copilot Studio 等の外部の MCP クライアントはこの REST API には接続できません。実際に外部クライアントが接続する先はセクション5です。

## 5. 実プロトコル準拠の MCP サーバー（`/mcp`、外部の MCP クライアント向け）

[ADR-0016](../decisions/0016-copilot-studio-github-harness-confirmed.md) の検証により、Microsoft Copilot Studio の GitHub Copilot harness は「Add MCP server」フローで任意の MCP サーバーに接続できることが確認されました（Server URL・認証方式を入力すると、Copilot Studio がプロトコルハンドシェイクを行い Tool 一覧を取得する）。この経路に対応するため、`services/mcp-backend/mcp_backend/mcp_protocol_server.py` に、公式 MCP Python SDK（`mcp` パッケージ、`mcp.server.fastmcp.FastMCP`）を使った実プロトコル準拠のサーバーを実装し、同じ `ToolRegistry` に委譲する形で `/mcp` に公開しています(`mcp_backend/factory.py::build_app()` が両方のエンドポイントを1つの FastAPI アプリにまとめます)。

- **実装言語の選定理由**: 本リポジトリは既に Python 3.11+ で統一されており([ADR-0002](../decisions/0002-python-primary-language.md))、Model Context Protocol の公式 SDK は Python と TypeScript の両方で最も高いカバレッジ・公式サポートを持つため、追加言語を導入せず Python 版の公式 SDK を採用しました([ADR-0016](../decisions/0016-copilot-studio-github-harness-confirmed.md) 決定4)。
- **Tool の入力スキーマ**: 各 Tool 関数は型付けされていない `params: dict` を受け取る設計のため、公開される JSON Schema も汎用的な `{"type": "object", "additionalProperties": true}` 相当の緩いスキーマになります。フィールド単位の型付けは行っていません。これは正直な制限であり、今後 Tool ごとに厳密なスキーマを定義する場合は各 Industry Pack の `tools/*.py` 側の拡張が必要です。
- **ホスト許可リスト**: `mcp` SDK は DNS リバインディング対策として Host/Origin ヘッダーを検証します。`MCP_BACKEND_ALLOWED_HOSTS` 環境変数（カンマ区切り）で実際のデプロイ先ホスト名を追加してください。`localhost`/`127.0.0.1`（任意ポート）と `testserver`（`fastapi.testclient.TestClient` の固定ホスト名）は常に許可されます。詳細は [MCP-Security-Guide.md](MCP-Security-Guide.md) を参照してください。
- **検証方法**:
  - [tests/integration/test_mcp_protocol_server.py](../../tests/integration/test_mcp_protocol_server.py) — `fastapi.testclient.TestClient` 経由で生の JSON-RPC リクエスト（`initialize` → `notifications/initialized` → `tools/list` → `tools/call`）を送り、5業界すべてで検証済み（インプロセス、高速）。
  - [tests/integration/test_mcp_protocol_server.py](../../tests/integration/test_mcp_protocol_server.py) — MCPプロトコルのハンドシェイクとtools/list/tools/callを検証する統合テスト。
- **未実施**: 実際の Microsoft Copilot Studio 環境からこの `/mcp` エンドポイントに接続する検証は、実 Copilot Studio 環境へのアクセスがないため未実施です。上記2つの検証は、公式 SDK ベースの MCP クライアントが正しくハンドシェイクできることを示すものであり、Copilot Studio 自身の実装の挙動を保証するものではありません。

