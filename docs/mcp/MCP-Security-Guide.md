# MCP セキュリティガイド

[![日本語](https://img.shields.io/badge/%E3%81%82-%E6%97%A5%E6%9C%AC%E8%AA%9E-087F8C?style=for-the-badge)](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/docs/mcp/MCP-Security-Guide.md) [![English](https://img.shields.io/badge/A-English-5B6670?style=for-the-badge)](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/docs/mcp/MCP-Security-Guide.en.md)

認証そのもの（誰がリクエストできるか）は、MCP Backendを公開するAzure環境とCopilot Studioの接続設定で構成します。本ページは、認証以外のMCP Backendセキュリティ管理策を整理します。

## 1. 実装済みの管理策

### 1.1 `MCP_BACKEND_ALLOWED_TOOLS` 許可リスト（Defense-in-Depth）

`services/mcp-backend/mcp_backend/factory.py::_allowed_tools_from_env()` は、環境変数 `MCP_BACKEND_ALLOWED_TOOLS`（カンマ区切りの Tool 名リスト）を読み取り、`ToolRegistry` に許可リストとして渡します。

```bash
# .env.example より
# 任意の Defense-in-Depth 許可リスト（カンマ区切りの Tool 名）。
# 未設定の場合は選択中の Industry Pack が宣言する全 Tool を許可する。
MCP_BACKEND_ALLOWED_TOOLS=
```

未設定（空文字列）の場合は、選択中の Industry Pack の `manifest.yaml`（`mcp_tools_path` が指すモジュールの `TOOL_FUNCTIONS`）が宣言する全 Tool が許可されます。この許可リストは Tool 名の集合をさらに狭めるためだけに使え、Pack が宣言していない Tool 名を追加で許可することはできません（`ToolRegistry.invoke()` は許可リストのチェックの後、実際に `tool_functions` 辞書にその Tool 名が存在するかを別途確認するため）。挙動は [MCP Tool safety test](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/tests/security/test_mcp_tool_safety.py) の `test_tool_not_in_allowlist_is_rejected` / `test_tool_in_allowlist_is_permitted` / `test_list_tools_respects_allowlist` で検証されています。

### 1.2 非 root コンテナ実行

`deployment/containers/mcp-backend/Dockerfile` は非 root ユーザーでアプリケーションを実行します。

```dockerfile
RUN groupadd --gid 1000 iiq && useradd --uid 1000 --gid iiq --shell /usr/sbin/nologin --create-home iiq
...
USER iiq
```

### 1.3 既定で内部限定の Ingress

`deployment/bicep/resources.bicep` は Azure Container Apps の Ingress を既定で内部限定（`external: false`）に設定しています。

```bicep
// Environment, and one Container App. Ingress is internal-only by default -
// flip to external only with explicit approval (see instruction section 24).
...
ingress: {
  external: false
```

外部公開（`external: true`）へ切り替えるのは、明示的な承認を得た場合のみとされています。

### 1.4 実 MCP プロトコルエンドポイント(`/mcp`)の Host/Origin 許可リスト

`services/mcp-backend/mcp_backend/mcp_protocol_server.py` は、公式 `mcp` SDK が備える DNS リバインディング対策(`TransportSecuritySettings`)を有効にしています。`MCP_BACKEND_ALLOWED_HOSTS` 環境変数(カンマ区切り)で、実際のデプロイ先ホスト名(例: Container App の FQDN)を許可リストに追加してください。未設定でも `localhost`/`127.0.0.1`(任意ポート)と `testserver`(テスト用の固定ホスト名)は常に許可されます。許可されていない Host ヘッダーでのリクエストは `421 Misdirected Request` で拒否されます。詳細は [MCP-Design-and-Contract-Guide.md](MCP-Design-and-Contract-Guide.md) セクション5を参照してください。

## 2. 未実装のセキュリティ管理策（明示的なギャップ）

以下は現時点で **実装されていません**。本番デプロイ前に評価・実装が必要です。

- **API 認証**: MCP Backendへの受信リクエスト認証は未実装です。公開前にAzureの認証層またはCopilot Studio接続の認証方式を構成してください。
- **依存関係の脆弱性スキャン**: `services/mcp-backend/` および Industry Pack コードが依存する Python パッケージに対する自動脆弱性スキャン（例: `pip-audit`、Dependabot 相当）は、本リポジトリのドキュメント作成時点では確認できていません。CI ワークフロー（`.github/workflows/`）に組み込む場合は、その内容を本ページに追記してください。
- **プロンプトインジェクション・テストスイート**: MCP Tool やエージェント指示に対するプロンプトインジェクション耐性を検証する専用のテストスイートは、まだ実装されていません。

これらの項目を「実装済み」として他のドキュメントに記載しないでください。実装した際は本ガイドを更新し、対応するテストファイルへのリンクを追加してください。
