# Industry Packを選択

1回のラボでは1業界を選び、同じIndustry PackをFabric IQ、Foundry IQ、Work IQ、Copilot Studioで使用します。途中で業界を混在させません。

| 業界 | Pack directory | 起点となる合成ID | 主なシナリオ |
| --- | --- | --- | --- |
| Manufacturing | `manufacturing` | `QI-SYN-001` | 品質問題と部品・設計変更の調査 |
| Financial Services | `financial-services` | `CASE-SYN-001` | 不正調査と証跡確認 |
| Retail | `retail` | `INV-SYN-401` | 在庫不足と需要シグナル確認 |
| Healthcare | `healthcare` | `ENC-SYN-003` | 合成患者の記録完全性確認 |
| Public Sector | `public-sector` | `CASE-SYN-301` | 合成案件と申請の確認 |

## 選択を記録

証跡へ次を記録します。

```text
Industry Pack: <pack directory>
Track: A / B
Dataset: small synthetic / customer metadata / approved customer data
Workspace: <name>
Operator: <role or test user>
Started at: <timestamp with timezone>
```

!!! note "実顧客トラックの分岐"
    実顧客データを扱う承認がない場合は`customer metadata`を選びます。承認がある場合も、最初にmetadataと匿名化sampleでモデル候補を検証します。

**完了条件**: 1つのIndustry Pack、トラック、dataset種別、作業workspaceを記録した。

[前へ: 事前チェック](prerequisites.md){ .md-button }
[トラックAへ](synthetic/index.md){ .md-button .md-button--primary }
[トラックBへ](customer-ontology/index.md){ .md-button }
