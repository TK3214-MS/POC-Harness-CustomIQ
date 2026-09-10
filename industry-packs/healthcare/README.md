# industry-packs/healthcare/

標準 Industry Pack（instruction §9.4）。標準シナリオ: Healthcare Case History Search。完全な架空データのみを使用します。

禁止事項: 診断の自動確定、治療方法の自動決定、薬剤の自動推奨、実患者データの使用、Human review なしの臨床判断。

回答には Synthetic data notice / Not medical advice / Human clinical review required を必ず含めます。

**状態: 実装済み（Phase 3）**。エンティティ: SyntheticPatient, Provider, Encounter, ClinicalEvent（Claim / Medication / Appointment は未実装）。MCP Tool は診断・処方・治療判断を一切行いません。
