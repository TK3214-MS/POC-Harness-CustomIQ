# 合成サンプルデータラボ

想定時間: 3〜4時間

選択した1つのIndustry Packを、格納済みサンプルデータの確認からCopilot Studioの複合質問まで段階的に構成します。

<div class="lab-step-strip" markdown>
<div>Local setup</div>
<div>Fabric IQ</div>
<div>Foundry IQ</div>
<div>Work IQ</div>
<div>Copilot Studio</div>
<div>Agent test</div>
<div>Complete</div>
</div>

## ラボ構成

| Lab | 作業 | 目安 |
| --- | --- | ---: |
| 1 | サンプルデータとローカル検証 | 15分 |
| 2 | Fabric IQへentityとrelationshipを構成 | 60分 |
| 3 | Foundry IQへknowledgeを登録 | 40分 |
| 4 | Work IQへ合成M365コンテンツを配置 | 30分 |
| 5 | Copilot Studioエージェントを構成 | 30分 |
| 6 | エージェントを独立してテスト・評価 | 30〜45分 |
| 7 | 完了確認とクリーンアップ判断 | 20分 |

各Labは前段の成功を前提とします。0件や接続失敗を残したまま複合質問へ進みません。

## 使用するsource

選択した`<pack>`を次のいずれかへ置換します。

- Fabric: [`industry-packs/<pack>/sample-data/fabric/*.csv`](https://github.com/TK3214-MS/POC-Harness-CustomIQ/tree/main/industry-packs){ target="_blank" rel="noopener" }
- Foundry: [`industry-packs/<pack>/knowledge/*.md`](https://github.com/TK3214-MS/POC-Harness-CustomIQ/tree/main/industry-packs){ target="_blank" rel="noopener" }
- Work IQ: [`industry-packs/<pack>/sample-data/work-iq/*.md`](https://github.com/TK3214-MS/POC-Harness-CustomIQ/tree/main/industry-packs){ target="_blank" rel="noopener" }
- Ontology定義: [`industry-packs/<pack>/ontology/entities.yaml`](https://github.com/TK3214-MS/POC-Harness-CustomIQ/tree/main/industry-packs){ target="_blank" rel="noopener" }
- エージェント指示: [`industry-packs/<pack>/agents/investigation_agent_instructions.md`](https://github.com/TK3214-MS/POC-Harness-CustomIQ/tree/main/industry-packs){ target="_blank" rel="noopener" }

[Lab 1を開始](01-local-setup.md){ .md-button .md-button--primary }
