# Healthcareサンプルデータ

すべて合成データであり、医療助言ではない。`fabric/`直下にはOntologyの全4 entity typeに対応する小容量CSVがあり、同じ`*-SYN-*` IDでrelationshipを検証できる。`fabric/enterprise/`にはgeneratorから再現可能な大規模CSVがある。

`work-iq/`には同一合成患者・受診を参照するSharePoint文書、Teams会話、Outlookメール、会議記録の4件がある。専用テストアカウントだけで使用し、実在患者情報を投入しない。

`knowledge/`の8文書はFoundry IQ用の管理文書である。`foundry/demo/knowledge.jsonl`は8文書を束ねた補助コーパス、`foundry/enterprise/records.jsonl`は構造化業務レコードの検索検証用であり、いずれもMarkdown管理文書の代替ではない。`prompts/enterprise_prompts.yaml`には5シナリオ50件の評価質問がある。

再生成と投入は[IQデモデータ投入・再構成ランブック](../../../docs/evaluation/Demo-Data-Deployment-Runbook.md)を参照する。
