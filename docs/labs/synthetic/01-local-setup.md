# Lab 1: ローカル準備

想定時間: 20分

## 1. データ生成

リポジトリルートで実行します。

```bash
source .venv/bin/activate
python scripts/generate_demo_iq_data.py
```

選択したIndustry Packの次のディレクトリを確認します。

```text
industry-packs/<pack>/sample-data/fabric/
industry-packs/<pack>/sample-data/foundry/demo/
industry-packs/<pack>/sample-data/work-iq/
```

## 2. 自動検証

```bash
pytest tests/contract/test_demo_iq_data.py -q
python scripts/validation/validate_synthetic_data.py
```

## 3. 対応関係を確認

`industry-packs/<pack>/ontology/entities.yaml`を開き、各entityの`dataset_key`と`identifier_field`を確認します。対応するCSVに同名tableとkey列があることを確認します。

!!! tip "IDを揃える"
    このラボではsmall synthetic datasetの`*-SYN-*` IDを使います。`enterprise/`の連番IDと混在させません。

## 成功条件

- [ ] 生成コマンドがエラーなく終了した。
- [ ] contract testが成功した。
- [ ] synthetic data validationが成功した。
- [ ] 選択したpackのFabric、Foundry、Work IQ sourceを確認した。
- [ ] 自動検証結果を証跡へ記録した。

[前へ: トラックA概要](index.md){ .md-button }
[次へ: Fabric IQ](02-fabric-iq.md){ .md-button .md-button--primary }
