# industry-packs/manufacturing/

標準 Industry Pack 第一号(instruction §9.1)。**Phase 2 の Local Preview 垂直スライスで実装済み。**

標準シナリオ: Manufacturing Quality Issue Investigation

**状態: 実装済み(Phase 2)。** `manifest.yaml` は `iq_platform.contracts.manifest.IndustryPackManifest` で検証されます([ADR-0004](../../docs/decisions/0004-industry-pack-manifest-schema.md))。データ生成は `data/generator.py`(6エンティティ: Factory, ProductionLine, Supplier, Part, QualityIssue, EngineeringChange)、MCP ツールは `tools/manufacturing_tools.py`。Product / Vehicle / Recall / WorkOrder / Inspection / Shipment 等の残りのエンティティは未実装(Phase 3+ で拡張検討)。

利用方法: [本番環境構築ガイド](../../docs/Production-Environment-Setup.md)で作成したCopilot StudioエージェントまたはMCP Backendから、このIndustry PackのMCP Toolを利用します。
