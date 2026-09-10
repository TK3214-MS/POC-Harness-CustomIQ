# Industry Pack Selection（業界パックの選び方・切り替え方）

## 選択肢

| ID | 表示名 | 標準シナリオ |
|---|---|---|
| `manufacturing`（既定） | Manufacturing | Manufacturing Quality Issue Investigation |
| `financial-services` | Financial Services | Financial Fraud Investigation |
| `retail` | Retail | Retail Demand and Inventory Analysis |
| `healthcare` | Healthcare | Healthcare Case History Search（完全架空データ、診断・治療判断なし） |
| `public-sector` | Public Sector | Public Sector Case Investigation |

## 選択方法

```bash
./scripts/demo/run-demo-cli.sh select-industry <ID>
./scripts/demo/run-demo-cli.sh run-demo --industry <ID>
```

`select-industry` は選択状態を `scripts/demo/output/selected_industry_pack.json`（gitignore 対象）に保存します。以後 `--industry` を省略すると選択済みの業界が使われます。`run-demo --industry <ID>` のように毎回明示することもできます。

## 切り替え時に変わるもの / 変わらないもの

変わるもの（Industry Pack 内、`industry-packs/<ID>/`）:
- Ontology（`ontology/entities.yaml`）
- Sample Data Generator（`data/generator.py`）
- Knowledge Documents（`knowledge/*.md`）
- Work Context Fixtures（`work-context/fixtures.json`）
- MCP Tools（`tools/*.py`）
- Semantic 関係性ロジック（`semantics/*.py`）
- シナリオ実行ロジック（`agents/scenario.py`）
- Demo Prompts、Expected Results、Evaluation Rubric、Terminology、Responsible AI Notice

変わらないもの（`iq_platform/` 配下、共通コード）:
- `GenericLocalOrchestrator`
- `MockKnowledgeAdapter` / `MockSemanticAdapter` / `SimulatedWorkContextAdapter`
- `services/mcp-backend/` の `ToolRegistry` / FastAPI アプリ
- `AgentResponse` / `MCPToolResponse` / `IndustryPackManifest` の契約スキーマ

この分離は [ADR-0010](../decisions/0010-industry-pack-plugin-loading.md) と [ADR-0011](../decisions/0011-generic-orchestrator-and-semantic-adapter.md) で設計され、[tests/end-to-end/test_industry_pack_switching.py](../../tests/end-to-end/test_industry_pack_switching.py) で自動検証されています。
