# 事前チェック

想定時間: 20〜30分

このページの全項目を確認できない場合、SaaS構築へ進みません。提供条件、ライセンス、region、Preview状態は変更されるため、実施日時点のMicrosoft公式文書とtenant管理者の判断を優先します。

## 1. ローカル環境

リポジトリルートで実行します。

```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python scripts/generate_demo_iq_data.py
pytest tests/contract/test_demo_iq_data.py -q
python scripts/validation/validate_synthetic_data.py
```

## 成功条件

- Python 3.11以上を使用している。
- demo data contract testsが成功する。
- synthetic data validationが成功する。

## 2. Microsoft環境

次をtenant管理者と確認します。具体的なライセンス、価格、region、GA/Preview状態はこのラボで固定しません。

- [ ] Microsoft Fabricを利用できるcapacityとworkspaceがある。
- [ ] Fabric Ontologyと必要な関連機能をtenantで利用できる。
- [ ] Lakehouseへmanaged tableを作成できる。
- [ ] Azure AI Searchと、ラボで使用するFoundry IQ機能を利用できる。
- [ ] Copilot Studioでエージェントを作成し、Fabric IQ、Foundry IQ、Work IQのToolを追加できる。
- [ ] Work IQを利用する場合、tenant設定、課金ポリシー、利用者ポリシーが構成済みである。
- [ ] SharePoint、Teams、Exchangeへラボ用合成コンテンツを配置できる。

## 3. 権限

| 対象 | 必要な作業 | 確認担当 |
| --- | --- | --- |
| Fabric workspace | Lakehouse、Ontology、binding、Graph確認 | Fabric管理者 |
| Azure AI Search / Foundry | Knowledge Source、index、Knowledge Baseの構成 | Azure管理者 |
| Microsoft 365 | 合成文書、Teams投稿、メール、会議の準備 | M365管理者 |
| Copilot Studio | エージェント作成、Tool接続、Activity trace確認 | Power Platform管理者 |

!!! danger "不足している場合"
    不足項目を推測で回避せず、管理者へworkspace名、必要操作、対象ユーザー、利用期間を伝えて確認します。条件が揃うまで[業界選択](choose-industry.md)以降の構築を開始しません。

## 4. 証跡フォルダー

ラボ外の承認済み保存先に、次の情報を記録する場所を準備します。

- 実施日時とタイムゾーン
- 選択したIndustry Packとdataset種別
- workspace、Ontology、Knowledge Baseの識別情報
- Activity traceのTool名、結果、Correlation ID
- 自動検証コマンドと結果

アクセストークン、接続文字列、Secretは記録しません。

**完了条件**: ローカル検証が成功し、Microsoft環境の全チェック項目を確認できた。

[前へ: ラボガイド](index.md){ .md-button }
[次へ: 業界を選択](choose-industry.md){ .md-button .md-button--primary }
