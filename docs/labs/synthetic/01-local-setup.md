# Lab 1: サンプルデータ確認

想定時間: 15分

## 1. 格納済みデータを確認

選択したIndustry Packの次のディレクトリを確認します。このラボでは格納済みファイルをそのまま使用し、再生成しません。

```text
industry-packs/<pack>/sample-data/fabric/
industry-packs/<pack>/sample-data/foundry/demo/
industry-packs/<pack>/sample-data/work-iq/
industry-packs/<pack>/knowledge/
```

再生成が必要な開発者は[サンプルデータ再生成ガイド](../../reference/Sample-Data-Regeneration-Guide.md)を参照してください。

## 2. 自動検証

```bash
pytest tests/contract/test_demo_iq_data.py -q
python scripts/validation/validate_synthetic_data.py
```

## 3. 対応関係を確認

[`industry-packs/<pack>/ontology/entities.yaml`](https://github.com/TK3214-MS/POC-Harness-CustomIQ/tree/main/industry-packs){ target="_blank" rel="noopener" }を開き、各entityの`dataset_key`と`identifier_field`を確認します。対応するCSVに同名tableとkey列があることを確認します。

!!! tip "IDを揃える"
    このラボではsmall synthetic datasetの`*-SYN-*` IDを使います。`enterprise/`の連番IDと混在させません。

## 成功条件

- [ ] contract testが成功した。
- [ ] synthetic data validationが成功した。
- [ ] 選択したpackのFabric、Foundry、Work IQ sourceを確認した。

[前へ: ラボ概要](index.md){ .md-button }
[次へ: Fabric IQ](02-fabric-iq.md){ .md-button .md-button--primary }
