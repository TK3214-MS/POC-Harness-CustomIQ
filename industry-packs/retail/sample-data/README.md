# Retailサンプルデータ

[![日本語](https://img.shields.io/badge/%E3%81%82-%E6%97%A5%E6%9C%AC%E8%AA%9E-087F8C?style=for-the-badge)](README.md) [![English](https://img.shields.io/badge/A-English-5B6670?style=for-the-badge)](README.en.md)

すべて合成データである。`fabric/`直下にはOntologyの全5 entity typeに対応する小容量CSVがあり、同じ`*-SYN-*` IDでrelationshipを検証できる。`fabric/enterprise/`にはgeneratorから再現可能な大規模CSVがある。

`work-iq/`には同一需要・在庫案件を参照するSharePoint文書、Teams会話、Outlookメール、会議記録の4件がある。専用テストアカウントへ登録する。

`knowledge/`の8文書はFoundry IQ用の管理文書である。`foundry/demo/knowledge.jsonl`は8文書を束ねた補助コーパス、`foundry/enterprise/records.jsonl`は構造化業務レコードの検索検証用であり、いずれもMarkdown管理文書の代替ではない。`prompts/enterprise_prompts.yaml`には5シナリオ50件の評価質問がある。

再生成と投入は[IQデモデータ投入・再構成ランブック](../../../docs/evaluation/Demo-Data-Deployment-Runbook.md)を参照する。
