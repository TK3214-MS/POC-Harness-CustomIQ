# MCP セキュリティガイド

認証そのもの（誰がリクエストできるか）については [Authentication-and-Error-Handling-Guide.md](Authentication-and-Error-Handling-Guide.md) を参照してください。本ページは、認証以外に実装済みのセキュリティ管理策と、未実装のセキュリティ管理策を整理します。

## 1. 実装済みの管理策

### 1.1 `MCP_BACKEND_ALLOWED_TOOLS` 許可リスト（Defense-in-Depth）

`services/mcp-backend/mcp_backend/factory.py::_allowed_tools_from_env()` は、環境変数 `MCP_BACKEND_ALLOWED_TOOLS`（カンマ区切りの Tool 名リスト）を読み取り、`ToolRegistry` に許可リストとして渡します。

```bash
# .env.example より
# 任意の Defense-in-Depth 許可リスト（カンマ区切りの Tool 名）。
# 未設定の場合は選択中の Industry Pack が宣言する全 Tool を許可する。
MCP_BACKEND_ALLOWED_TOOLS=
```

未設定（空文字列）の場合は、選択中の Industry Pack の `manifest.yaml`（`mcp_tools_path` が指すモジュールの `TOOL_FUNCTIONS`）が宣言する全 Tool が許可されます。この許可リストは Tool 名の集合をさらに狭めるためだけに使え、Pack が宣言していない Tool 名を追加で許可することはできません（`ToolRegistry.invoke()` は許可リストのチェックの後、実際に `tool_functions` 辞書にその Tool 名が存在するかを別途確認するため）。挙動は [tests/security/test_mcp_tool_safety.py](../../tests/security/test_mcp_tool_safety.py) の `test_tool_not_in_allowlist_is_rejected` / `test_tool_in_allowlist_is_permitted` / `test_list_tools_respects_allowlist` で検証されています。

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

## 2. 未実装のセキュリティ管理策（明示的なギャップ）

以下は現時点で **実装されていません**。本番デプロイ前に評価・実装が必要です。

- **API 認証**: [Authentication-and-Error-Handling-Guide.md](Authentication-and-Error-Handling-Guide.md) に記載のとおり、MCP Backend への受信リクエストを検証する仕組みは存在しません。
- **依存関係の脆弱性スキャン**: `services/mcp-backend/` および Industry Pack コードが依存する Python パッケージに対する自動脆弱性スキャン（例: `pip-audit`、Dependabot 相当）は、本リポジトリのドキュメント作成時点では確認できていません。CI ワークフロー（`.github/workflows/`）に組み込む場合は、その内容を本ページに追記してください。
- **プロンプトインジェクション・テストスイート**: MCP Tool やエージェント指示に対するプロンプトインジェクション耐性を検証する専用のテストスイートは、まだ実装されていません。

これらの項目を「実装済み」として他のドキュメントに記載しないでください。実装した際は本ガイドを更新し、対応するテストファイルへのリンクを追加してください。
