# サンプルデータ再生成ガイド

[![日本語](https://img.shields.io/badge/%E3%81%82-%E6%97%A5%E6%9C%AC%E8%AA%9E-087F8C?style=for-the-badge)](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/docs/reference/Sample-Data-Regeneration-Guide.md) [![English](https://img.shields.io/badge/A-English-5B6670?style=for-the-badge)](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/docs/reference/Sample-Data-Regeneration-Guide.en.md)

このページは、リポジトリへ格納済みの合成データを変更または再生成する開発者向けリファレンスです。通常のラボでは生成コマンドを実行せず、`industry-packs/<pack>/sample-data/`の既存ファイルを使用します。

## 環境準備

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## 小容量デモデータ

```bash
python scripts/generate_demo_iq_data.py
pytest tests/contract/test_demo_iq_data.py -q
python scripts/validation/validate_synthetic_data.py
```

生成先:

- Fabric: `industry-packs/<pack>/sample-data/fabric/*.csv`
- Foundry補助コーパス: `industry-packs/<pack>/sample-data/foundry/demo/knowledge.jsonl`

Work IQテンプレートとFoundryのMarkdownナレッジは、それぞれ`sample-data/work-iq/`と`knowledge/`で管理します。

## Enterpriseデータ

```bash
python scripts/generate_enterprise_sample_data.py
python scripts/generate_enterprise_prompts.py
pytest tests/contract -q
python scripts/validation/validate_synthetic_data.py
```

生成先:

- Fabric: `industry-packs/<pack>/sample-data/fabric/enterprise/*.csv`
- Foundry: `industry-packs/<pack>/sample-data/foundry/enterprise/records.jsonl`
- 質問: `industry-packs/<pack>/sample-data/prompts/enterprise_prompts.yaml`

## 変更時の原則

1. 継続利用する変更は生成済みCSVやJSONLだけへ直接加えず、generatorまたは元のKnowledge文書へ反映する。
2. 全業界で合成ID体系とrelationship参照を維持する。
3. 生成後にcontract testとsynthetic data validationを実行する。
4. 実在する個人、組織、患者、顧客、口座、住民の情報を追加しない。

投入先と期待件数は[IQデモデータ投入・再構成ランブック](../evaluation/Demo-Data-Deployment-Runbook.md)を参照してください。
