# MCP 認証・エラーハンドリングガイド

## 1. MCP Backend 自体のリクエスト認証は未実装（明示的なギャップ）

**現時点で、MCP Backend（`services/mcp-backend/`）には組み込みのリクエスト認証機構が存在しません。** `.env.example` に `MCP_BACKEND_API_KEY` という環境変数プレースホルダーが存在しますが、これは値を保持するだけであり、`services/mcp-backend/mcp_backend/app.py` のいずれのエンドポイント（`/health`、`/tools`、`/tools/{tool_name}/invoke`）にも API キー検証ミドルウェアとして組み込まれていません。つまり、現状の `create_app()` が返す FastAPI アプリに到達できる呼び出し元は誰でも全 Tool を呼び出せます。

これは本番デプロイに向けた明確な TBD 項目であり、[docs/architecture/architecture-guide.md §8](../architecture/architecture-guide.md) の「未実装」一覧、および `deployment/bicep/resources.bicep` の Container Apps Ingress が既定で内部限定である設計（[MCP-Security-Guide.md](MCP-Security-Guide.md) 参照）と合わせて評価してください。

**注意: これは Live Adapter が使う Microsoft Entra ID 認証とは別物です。** `iq_platform/security/entra_auth.py` は `azure-identity` の `ClientSecretCredential` による実際の Entra ID 認証を実装・単体テスト済みです（[tests/unit/test_live_adapters.py](../../tests/unit/test_live_adapters.py)）。これは Work IQ / Foundry IQ / Fabric IQ の各 Live Adapter が外部の Microsoft 製品 API を呼び出す際の認証であり、本ページで扱っている「MCP Backend 自体への受信リクエストの認証」とは対象範囲もコードパスも完全に独立しています。両者を混同しないでください。

## 2. エラーの表面化方法

MCP Backend はエラーを生の例外や HTTP 500 として返しません。すべてのエラーは `iq_platform.contracts.mcp_tool.MCPToolResponse`（[ADR-0006](../decisions/0006-mcp-tool-response-contract.md)）の `status="error"` / `errors` フィールドを通じて構造化された形で返されます。詳細な設計は [MCP-Design-and-Contract-Guide.md](MCP-Design-and-Contract-Guide.md) の「ToolRegistry の設計」を参照してください。要点は次のとおりです。

- 未知の Tool 名、許可リスト非該当、必須パラメータ欠落（`KeyError`）はいずれも `ToolRegistry.invoke()` 内で捕捉され、構造化エラーとして返される。
- HTTP レスポンスコードは常に `200`。クライアントは常に同じ JSON スキーマ（`MCPToolResponse`）をパースすればよく、HTTP レイヤーのエラーハンドリングを別途実装する必要がない。
- この挙動は [tests/security/test_mcp_tool_safety.py](../../tests/security/test_mcp_tool_safety.py) と [tests/integration/test_mcp_backend_integration.py](../../tests/integration/test_mcp_backend_integration.py) の `test_invoke_unknown_tool_returns_structured_error_not_http_error` で検証されています。

## 3. 本番投入に向けて追加が必要な項目（すべて TBD・未決定）

以下はいずれも設計方針として決定されておらず、`TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION` を含め要検証・要決定の項目です。

- **API キー検証ミドルウェア**: `MCP_BACKEND_API_KEY` を実際に検証する FastAPI ミドルウェア（または依存性注入）の追加。
- **Entra ID で保護された Ingress**: Azure Container Apps の組み込み認証（Easy Auth 相当）または API Management 経由での Entra ID トークン検証。製品固有の設定手順・対応状況は `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`（[docs/decisions/product-verification.md](../decisions/product-verification.md)）。
- **Container Apps 組み込み認証機能の利用**: Azure Container Apps 自体が提供する認証・認可機能の活用可否・設定方法。同様に `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`。

これらのどれを採用するかはまだ決定されていません。決定した際は本ガイドおよび [docs/decisions/](../decisions/) に ADR として記録してください。
