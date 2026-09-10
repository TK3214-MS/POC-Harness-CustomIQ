# Architecture Explained（デモ中に説明するアーキテクチャの要点）

詳細は [docs/architecture/architecture-guide.md](../architecture/architecture-guide.md) が正本です。ここではデモ中に口頭で説明しやすい要点のみをまとめます。

## レイヤーと今の状態（Local Preview Mode）

| レイヤー | デモでの役割 | 本番での役割 | 現在の状態 |
|---|---|---|---|
| GitHub Copilot harness | `GenericLocalOrchestrator` が代替 | Copilot Studio 上で実行 | Local: 実装済み / Live: 未検証（Adapter概念自体なし、harnessそのもの） |
| Work IQ | `SimulatedWorkContextAdapter` | 実際の Teams/Outlook/SharePoint 等 | Local: 実装済み / Live: verification_required スキャフォールド |
| Foundry IQ | `MockKnowledgeAdapter` | 実際のナレッジベース | Local: 実装済み / Live: verification_required スキャフォールド |
| Fabric IQ | `MockSemanticAdapter` + Pack固有 semantics plugin | 実際の Semantic Model/Ontology | Local: 実装済み / Live: verification_required スキャフォールド |
| MCP Backend | FastAPI、`ToolRegistry` | 同じコードを Azure Container Apps 等にデプロイ | 実装済み（[ADR-0012](../decisions/0012-mcp-backend-deployment-target.md)）、実デプロイ未検証 |
| Identity (Entra ID) | 不要（Local Preview） | Live Adapter の認証 | 認証コード自体は実装・単体テスト済み（[iq_platform/security/entra_auth.py](../../iq_platform/security/entra_auth.py)）、実テナントでの検証は未実施 |

## Adapter パターンと mode

すべての Adapter は `health_check` / `capabilities` / `mode` / `query` / `validate_configuration` / `get_diagnostics` を実装します（`iq_platform.contracts.adapter.Adapter`）。`mode` は `live` / `mock` / `simulated` / `unavailable` / `verification_required` のいずれかです。Live Adapter は認証情報が揃っても、製品 API 仕様が未検証な限り `verification_required` のままで、`live` には絶対に到達しません（[ADR-0013](../decisions/0013-live-adapter-verification-required-scaffold.md)）。

## Industry Pack が業界固有ロジックをすべて持つ理由

`iq_platform/` は業界名を一切知りません。関係性解決（`semantics/*.py`）とシナリオ実行（`agents/scenario.py`）は各 Industry Pack 内のプラグインとして動的ロードされます（`importlib`、[ADR-0010](../decisions/0010-industry-pack-plugin-loading.md)、[ADR-0011](../decisions/0011-generic-orchestrator-and-semantic-adapter.md)）。これにより、新しい業界を追加してもプラットフォームコードの変更が不要です。

## Mock/Simulation の開示

`AgentResponse.mock_or_simulation_disclosure` と `responsible_ai_notice` は必須フィールドで、省略した回答オブジェクトはそもそも構築できません（Pydantic の必須フィールド、[ADR-0005](../decisions/0005-agent-response-contract.md)）。
