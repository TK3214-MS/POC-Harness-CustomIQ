# ADR-0015: Work IQ / Foundry IQ / Fabric IQ の実際の統合方式は各製品自身が提供する MCP エンドポイントである(現行 Live Adapter は未対応)

- ステータス: Proposed(実装への合意・着手は未実施。設計上の発見と今後の方向性の記録)
- 日付: 2026-09-10

## コンテキスト

ユーザーから提供された3つの実際の Microsoft Learn ページを 2026-09-10 に取得・確認した([docs/decisions/product-verification.md](product-verification.md) の該当行を参照):

- [Connect Agents to Foundry IQ Knowledge Bases](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/foundry-iq-connect)(ms.date 2026-08-07)
- [Connect agents to Microsoft Fabric with Fabric IQ (preview)](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/fabric-iq)(ms.date 2026-08-05)
- [Work IQ MCP overview](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/work-iq/mcp/overview)(ms.date 2026-08-20)

これらは実在し、かなり具体的な統合方式を示している。**3製品すべてが、Model Context Protocol (MCP) を介したエージェント接続を公式の統合方式として文書化している。**

- **Foundry IQ**: Azure AI Search の agentic-retrieval knowledge base を、`{search_service_endpoint}/knowledgebases/{knowledge_base_name}/mcp?api-version=2026-08-01-preview` という MCP エンドポイントとして公開し、`knowledge_base_retrieve` という単一の MCP Tool を通じて Foundry Agent Service のエージェントに接続する。
- **Fabric IQ**: Ontology・Fabric data agent・Power BI semantic model の3種類の Fabric アイテムそれぞれに専用の MCP エンドポイント URL パターンがあり(例: data agent は `https://api.fabric.microsoft.com/v1/mcp/workspaces/{workspaceId}/dataagents/{dataAgentId}/agent`)、Foundry エージェントに `fabric_iq_preview` Tool として(または Toolbox 経由で汎用 `mcp` Tool として)接続する。
- **Work IQ**: Microsoft 365 データに対する汎用的な10個の MCP Tool(`fetch`/`create_entity`/`update_entity`/`delete_entity`/`do_action`/`call_function`/`ask`/`list_agents`/`get_schema`/`search_paths`)を、単一の MCP エンドポイントとして公開する。認証は Microsoft Entra ID で、MCP クライアントが `/.well-known/oauth-protected-resource` から自動的に認証設定を発見する。

**これは、本リポジトリが現在実装している Live Adapter の設計(`iq_platform/adapters/*/live_adapter.py`)と根本的に異なる。** 現行実装は、3レイヤー共通の `ClientSecretCredential`(クライアントクレデンシャルフロー、アプリのみ認証)による Entra ID 認証のみを行い、`query()` は常に `LiveAdapterNotYetVerifiedError` を送出するスタブである([ADR-0013](0013-live-adapter-verification-required-scaffold.md))。実際に検証された統合方式は次の点で現行実装と異なる。

1. **プロトコル**: 独自の REST 呼び出しではなく、各製品自身が提供する **MCP エンドポイントへの接続**が正式な統合方式である。
2. **認証方式は製品・アイテム種別ごとに異なる**: Work IQ は MCP クライアントによる自動ディスカバリー、Foundry IQ は Foundry プロジェクトのマネージド ID(またはユーザートークンをヘッダーで転送)、Fabric IQ は Entra ID の委任(On-Behalf-Of)認証(Fabric data agent のみ追加でアプリ単体トークンも許可)。現行実装が前提とする「3レイヤー共通の単一クライアントクレデンシャルフロー」という単純化は、検証された実際の認証モデルと一致しない。
3. **エージェントホストとして文書中で一貫して登場するのは "Microsoft Foundry Agent Service"(Azure AI Foundry)であり、"Microsoft Copilot Studio" や "GitHub Copilot harness" という語は3ページのいずれにも登場しなかった。** これは [ADR-0014](0014-local-orchestrator-is-not-a-harness-replacement.md) が前提とする「本番のオーケストレーション層は GitHub Copilot Harness(Copilot Studio)」という設計判断に対する新しい検証結果であり、Foundry Agent Service が実際にはより直接的に文書化された選択肢である可能性を示唆する。

## 決定(現時点では「提案」であり、未実装)

1. **`docs/decisions/product-verification.md` を更新し、上記の検証結果を記録した。**(本 ADR と同時に実施済み)
2. **`config/capabilities.yaml` の `work_iq` / `foundry_iq` / `fabric_iq` エントリを、検証済みの実際の情報で更新する。**(本 ADR と同時に実施予定 — 下記「影響」参照)
3. **Live Adapter の実装方針そのものの見直しはまだ実施していない。** 現行の `iq_platform/adapters/*/live_adapter.py` を「MCP クライアントとして各製品の MCP エンドポイントに接続する」設計に置き換えるかどうか、置き換える場合の実装方式(MCP クライアントライブラリの選定、製品ごとに異なる認証方式への対応、`iq_platform.contracts.adapter.Adapter` インターフェースとの整合性)は、**別途スコープを確認した上で着手する**。本 ADR はこの決定を実装するものではなく、決定が必要であることを記録するものである。
4. **「本番のオーケストレーション層は Copilot Studio(GitHub Copilot harness)である」という [ADR-0014](0014-local-orchestrator-is-not-a-harness-replacement.md) の前提を、Microsoft Foundry Agent Service という選択肢も踏まえて再検討する必要がある。** これも本 ADR では決定せず、[docs/decisions/open-questions.md](open-questions.md) に新しい未解決事項として追記する。

## 影響

- `config/capabilities.yaml` の `foundry_iq` と `fabric_iq` の `status` を `Preview` に更新し(実際の `last_verified_date` と非 TBD の `documentation_reference` を付与、[ADR-0007](0007-capability-registry-authority.md) の検証済みステータス強制ルールに従う)、`known_limitations` に実際の MCP エンドポイントパターン・認証方式・および「現行 Live Adapter は未対応」の旨を明記する。`work_iq` は `documentation_reference` を実際の URL に更新するが、GA/Preview 状態は未確認のため `status` は `Unknown` のまま維持する。
- [docs/Known-Limitations.md](../Known-Limitations.md) に新しい制限事項として「Live Adapter は各製品の公式 MCP エンドポイントに接続していない」ことを追記する。
- [docs/decisions/open-questions.md](open-questions.md) に、「本番のエージェントホストは Copilot Studio か、Foundry Agent Service か」という新しい未解決事項を追記する。
- **未実施のフォローアップ作業(ユーザーの合意が必要)**:
  - Live Adapter を実際の MCP エンドポイントに接続する形に再設計・再実装する(MCP クライアントライブラリの選定、`iq_platform.contracts.adapter.Adapter` との整合、テストの全面的な見直しを伴う大きな変更)。
  - `docs/setup/live-adapters-configuration.md` の Work IQ/Foundry IQ/Fabric IQ セクションを、確認できた実際のエンドポイントパターン・認証方式で更新する。
  - `docs/architecture/architecture-guide.md` / `docs/presentations/Architecture-Diagrams.md` の本番構成図([ADR-0014](0014-local-orchestrator-is-not-a-harness-replacement.md) 時点で追加したもの)を、MCP ベースの接続方式を反映する形に更新する。
  - Copilot Studio と Foundry Agent Service のどちらが実際の対象エージェントホストなのか、ユーザー/ステークホルダーに確認する。
