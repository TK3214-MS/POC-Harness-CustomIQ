# トラックA: 合成データE2E

想定時間: 3〜4時間

選択した1つのIndustry Packを、ローカル生成からCopilot Studioの複合質問まで段階的に構成します。

## ラボ構成

| Lab | 作業 | 目安 |
| --- | --- | ---: |
| 1 | ローカル生成と検証 | 20分 |
| 2 | Fabric IQへentityとrelationshipを構成 | 60分 |
| 3 | Foundry IQへknowledgeを登録 | 40分 |
| 4 | Work IQへ合成M365コンテンツを配置 | 30分 |
| 5 | Copilot Studioへ接続して段階テスト | 50分 |
| 6 | 証跡確認とクリーンアップ判断 | 20分 |

各Labは前段の成功を前提とします。0件や接続失敗を残したまま複合質問へ進みません。

## 使用するsource

選択した`<pack>`を次のいずれかへ置換します。

- Fabric: `industry-packs/<pack>/sample-data/fabric/*.csv`
- Foundry: `industry-packs/<pack>/knowledge/*.md`
- Work IQ: `industry-packs/<pack>/sample-data/work-iq/*.md`
- Ontology定義: `industry-packs/<pack>/ontology/entities.yaml`
- エージェント指示: `industry-packs/<pack>/agents/investigation_agent_instructions.md`

[Lab 1を開始](01-local-setup.md){ .md-button .md-button--primary }
