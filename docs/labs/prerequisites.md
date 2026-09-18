# 事前チェック

[![日本語](https://img.shields.io/badge/%E3%81%82-%E6%97%A5%E6%9C%AC%E8%AA%9E-087F8C?style=for-the-badge)](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/docs/labs/prerequisites.md) [![English](https://img.shields.io/badge/A-English-5B6670?style=for-the-badge)](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/docs/labs/prerequisites.en.md)

想定時間: 20〜30分

このページの全項目を確認できない場合、SaaS構築へ進みません。提供条件、ライセンス、region、Preview状態は変更されるため、実施日時点のMicrosoft公式文書とtenant管理者の判断を優先します。

## 1. Microsoft環境（必須）

次をtenant管理者と確認します。具体的なライセンス、価格、region、GA/Preview状態はこのラボで固定しません。

- [ ] Microsoft Fabricを利用できるcapacityとworkspaceがあります。
- [ ] Fabric Ontologyと必要な関連機能をtenantで利用できます。
- [ ] Lakehouseへmanaged tableを作成できます。
- [ ] Azure AI Searchと、ラボで使用するFoundry IQ機能を利用できます。
- [ ] Copilot Studioでエージェントを作成し、Fabric IQ、Foundry IQ、Work IQのToolを追加できます。
- [ ] Work IQを利用する場合、tenant設定、課金ポリシー、利用者ポリシーが構成済みです。
- [ ] SharePoint、Teams、Exchangeへラボ用合成コンテンツを配置できます。

[ラボコスト見積もりガイド](../reference/Cost-Estimation-Guide.md)で、利用するソリューションと月間利用頻度を基に予算上限を確認してください。

## 2. ローカル環境（サンプルを自身で生成する場合のみ）

Repositoryに格納済みの合成データを使用する場合、このセクションは不要です。生成元を変更する開発者、またはサンプルデータを自身で再生成する場合だけ実施します。

リポジトリルートで実行します。

```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest tests/contract/test_demo_iq_data.py -q
python scripts/validation/validate_synthetic_data.py
```

### 成功条件

- Python 3.11以上を使用しています。
- demo data contract testsが成功します。
- synthetic data validationが成功します。

再生成の詳細は[サンプルデータ再生成ガイド](../reference/Sample-Data-Regeneration-Guide.md)を参照してください。

## 3. 権限（必須）

| 対象 | 必要な作業 | 確認担当 |
| --- | --- | --- |
| Fabric workspace | Lakehouse、Ontology、binding、Graph確認 | Fabric管理者 |
| Azure AI Search / Foundry | Knowledge Source、index、Knowledge Baseの構成 | Azure管理者 |
| Microsoft 365 | 合成文書、Teams投稿、メール、会議の準備 | M365管理者 |
| Copilot Studio | エージェント作成、Tool接続、Activity trace確認 | Power Platform管理者 |

!!! danger "不足している場合"
    不足項目を推測で回避せず、管理者へworkspace名、必要操作、対象ユーザー、利用期間を伝えて確認します。条件が揃うまで[業界選択](choose-industry.md)以降の構築を開始しません。

**完了条件**: Microsoft環境と権限の全チェック項目を確認できました。自身でデータを生成する場合だけ、ローカル検証も成功しています。

[前へ: ラボガイド](index.md){ .md-button }
[次へ: 業界を選択](choose-industry.md){ .md-button .md-button--primary }
