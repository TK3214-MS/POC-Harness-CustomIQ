# Lab 1: 質問とデータ認可

このLabではOntologyの構築を始めず、答えるべき業務質問と使用可能なデータ範囲を確定します。

## 1. 役割を割り当てる

最低限、Business owner、Data owner、Data steward、Source system owner、Security/Privacy、Ontology designer、Test ownerを記録します。兼務する場合も、各成果物の承認者を空欄にしません。

## 2. gold questionsを作る

選択した業界で価値が高い質問を3〜7件記録します。

| 項目 | 記入内容 |
| --- | --- |
| Question ID | 変更されないID |
| 質問 | 利用者が実際に使う表現 |
| 利用者 | roleと利用場面 |
| 必要な事実 | entity、property、relationship候補 |
| 鮮度 | 許容される更新間隔 |
| 禁止事項 | 自動承認、診断、凍結など |
| 成功条件 | 期待ID、根拠、許容誤差 |

## 3. データ利用経路を選ぶ

=== "metadata・匿名化sample"

    DDL、データ辞書、集計済みprofile、匿名化sampleだけを対象にします。これを標準経路とします。

=== "承認済み実データ"

    Data ownerとSecurity/Privacyが、目的、対象列、利用者、保存先、AI利用、保持期間を承認した記録を添付します。承認対象外の列は除外します。

## 成功条件

- [ ] 3〜7件のgold questionsがある。
- [ ] 各質問にBusiness ownerと成功条件がある。
- [ ] 使用可能なデータ範囲と禁止事項が記録されている。
- [ ] 生成AIへ渡してよい情報がSecurity/Privacyにより確認されている。

[前へ: トラックB概要](index.md){ .md-button }
[次へ: Source inventory](02-inventory-and-profile.md){ .md-button .md-button--primary }
