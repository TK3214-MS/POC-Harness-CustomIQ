# ADR-0016: Copilot Studio の GitHub Copilot Harness を対象と確定し、MCP Backend を実プロトコル準拠の MCP サーバーとして実装する

- ステータス: Accepted
- 日付: 2026-09-10

## コンテキスト

[ADR-0015](0015-mcp-native-iq-layer-integration.md) は、Work IQ / Foundry IQ / Fabric IQ が実際に MCP ベースで統合されることを検証した一方、フェッチした3ページには "Copilot Studio" も "GitHub Copilot harness" も一切登場せず、代わりに "Microsoft Foundry Agent Service" が一貫してエージェントホストとして登場したため、[open-questions.md](open-questions.md) Q11 として「本番の対象は Copilot Studio か Foundry Agent Service か」を未解決事項とした。

ユーザーから「オーケストレーション層は Copilot Studio GitHub Harness で作成したエージェントを想定している」との確認と、追加の実 URL(Microsoft Tech Community ブログ記事)が提供されたため、2026-09-10 に以下の実際の Microsoft Learn ページを追加で取得・確認した。

- [Foundry IQ is now in Copilot Studio](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/foundry-iq-is-now-in-copilot-studio-bring-your-enterprise-data-to-every-agent-co/4534635)(Tech Community ブログ、2026-07-08)
- [Connect to Foundry IQ from an agent - Microsoft Copilot Studio (GitHub Copilot)](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/foundry-iq-connect)(ms.date 2026-06-23)
- [Connect to Fabric IQ from an agent (preview) - Microsoft Copilot Studio (GitHub Copilot)](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/fabric-iq-connect)(ms.date 2026-07-29)
- [Harnesses in Copilot Studio](https://learn.microsoft.com/en-us/microsoft-copilot-studio/harnesses-overview)(ms.date 2026-07-28)
- [Available tools for agents](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/tools-available)、[Tools overview for agents](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/tools-overview)、[Add a Model Context Protocol (MCP) server to your agent as a tool (preview)](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/tools-add-mcp-server)(ms.date 各ページ参照)
- [Available knowledge sources for agents](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/knowledge-sources-overview)(ms.date 2026-08-31)

## 判明した事実(すべて上記の実ページで確認済み)

1. **"GitHub Copilot harness" は実在し、指示書が前提とする概念そのものである。** Copilot Studio には3種類の Harness(ランタイム)があり、GitHub Copilot harness はそのうち「複雑な多段階業務プロセス向けの最も高機能なもの」で、コネクタ・ナレッジ・MCP・接続済みエージェントを横断してツールを呼び出せる([harnesses-overview](https://learn.microsoft.com/en-us/microsoft-copilot-studio/harnesses-overview))。**[ADR-0014](0014-local-orchestrator-is-not-a-harness-replacement.md) の前提(GitHub Copilot harness が本番のオーケストレーション層)は正しかった。**
2. **Foundry IQ は Copilot Studio の GitHub Copilot harness エージェントに、専用の一次機能として直接接続できる。** Build タブ → Tools → 「Foundry IQ」を選択し、API キー・クライアント証明書・サービスプリンシパル・Entra ID 統合のいずれかで接続を作成する。この接続設定は Copilot Studio 自身が提供する UI/バックエンドで完結する。
3. **Fabric IQ も同様に、Copilot Studio の GitHub Copilot harness エージェントに専用の一次機能として直接接続できる**(プレビュー)。
4. **Copilot Studio の GitHub Copilot harness は、汎用の Tool 種別として任意の MCP サーバーへの接続もネイティブにサポートする。**「Add a Model Context Protocol (MCP) server as a tool」フローで、Server URL(HTTPS エンドポイント)・認証方式を入力すると、Copilot Studio がプロトコルハンドシェイクを行い、そのサーバーが公開する Tool 一覧を取得する。**これは本リポジトリの MCP Backend が Copilot Studio に接続される際の正式な経路である。**
5. **Work IQ (preview) は Copilot Studio の一次機能として利用できる。** [Work IQ in Microsoft Copilot Studio](https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-work-iq) は、GitHub Copilot harnessで動作するWork IQを、**Tools → Add Tool → Model Context Protocol → Work IQ (preview)** から追加し、**Create New Connection → Create → サインイン → Add and Configure** で接続する手順を明記している。Work IQはPreviewであり、Copilot Creditsの使用量ベース課金、テナント有効化、spending policy、管理者によるMCPポリシー管理が必要である。これは汎用Remote MCP URLを手入力する経路ではない。

## 決定

1. **[open-questions.md](open-questions.md) Q11 を解決する。本番のオーケストレーション層は Microsoft Foundry Agent Service ではなく、Copilot Studio の GitHub Copilot harness で作成されたエージェントである。** [ADR-0014](0014-local-orchestrator-is-not-a-harness-replacement.md) の結論(`GenericLocalOrchestrator` は Local Preview Mode 専用の代替であり、本番の設計要素ではない)は変更しない。
2. **本リポジトリのコード側の責務は、Copilot Studio の GitHub Copilot harness が「Add MCP server」フローで接続できる、実プロトコル準拠の MCP サーバーを提供することに限定される。** Foundry IQ / Fabric IQ への接続は Copilot Studio 自身が一次機能として提供するため、本リポジトリが Foundry IQ / Fabric IQ 用の独自クライアントコードを実装する必要はない。
3. **現行の `services/mcp-backend/` は、`/health` / `/tools` / `/tools/{name}/invoke` という独自形状の REST API であり、Model Context Protocol の実際のワイヤーフォーマット(JSON-RPC 2.0 ベースの initialize/tools-list/tools-call ハンドシェイク)には準拠していない。** Copilot Studio の「Add MCP server」フローが行う「プロトコルハンドシェイク」に応答できるようにするため、実際の MCP プロトコルに準拠したサーバー実装を追加する。
4. **実装言語は Python とする。** 本リポジトリは既に Python 3.11+ で統一されており([ADR-0002](0002-python-primary-language.md))、Model Context Protocol の公式 SDK(`mcp` パッケージ、`mcp.server.fastmcp.FastMCP` を含む)は Python と TypeScript の双方で最も高いカバレッジ・公式サポートを持つ。追加言語を導入するコストを避けるため、Python 版の公式 SDK を採用する。
5. **既存のカスタム REST API(`/health`/`/tools`/`/tools/{name}/invoke`)は削除せず併存させる。** これは実 MCP プロトコル未対応のクライアント(本リポジトリ自身のテスト・デモ CLI 等)から使われ続けるため、廃止せずそのまま残す。実 MCP プロトコルのエンドポイントは別途追加する形とする。
6. **Work IQの専用Copilot Studio接続を採用する。** Work IQ Knowledge SourceをFoundry IQに組み込む構成は、Foundry IQの検索計画にWork IQを含める必要がある場合の代替構成として扱い、Work IQをCopilot Studioで利用する標準手順とは混同しない。

## 影響

- `services/mcp-backend/` に実 MCP プロトコル準拠のサーバー実装を追加する(`mcp` パッケージの `FastMCP` を使用し、既存の `ToolRegistry` のロジックに委譲する)。
- 追加した MCP サーバーに対して、実際に Copilot Studio が行うのと同種のハンドシェイク(initialize → tools/list → tools/call)を行う MCP クライアントによる検証スクリプトを用意する。
- `docs/mcp/` 配下のドキュメントを、実プロトコル準拠の MCP サーバーの追加を反映する形で更新する。
- `docs/deployment/Step-by-Step-Deployment-Guide.md` のステップ10(Copilot Studio harness の設定)を、実際に確認された「Add MCP server」フロー(Server URL・認証方式の入力、Copilot Studio 側でのハンドシェイク)に基づいて具体化する。
- `config/capabilities.yaml` の `harness.copilot_studio` エントリを、確認された事実(Copilot Studio に3種類の Harness が存在し、GitHub Copilot harness が対象であること)で更新する。
- Work IQ の Copilot Studio 対応は、ユーザーへの確認事項として [docs/decisions/product-verification.md](product-verification.md) に明記したままにする。
