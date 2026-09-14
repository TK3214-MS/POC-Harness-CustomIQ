# Lab 2: Source inventoryとprofile

各sourceを一覧化し、key候補とrelationship候補を判断できる品質指標を収集します。

## 1. source inventory

| 分類 | 必須項目 |
| --- | --- |
| Source | system、database、schema、table、owner、用途 |
| Column | name、native type、nullable、description、unit、classification |
| Key | primary key候補、unique制約、複合key、生成規則 |
| Join | foreign key、対応列、想定cardinality |
| Operation | 更新頻度、削除方式、late arrival、SLA |
| Security | PII、機密区分、row/column制御、利用可能workspace |

## 2. profile

最低限、row count、null count、distinct count、duplicate key count、日時範囲、status分布、orphan countを計測します。値を生成AIに推測させません。

$$
\text{orphan率} = \frac{\text{target keyが存在しないrelationship行数}}{\text{relationship全行数}}
$$

単位、通貨、タイムゾーン、大小文字、前後空白、soft delete、履歴重複も確認します。

## 3. Copilotを使う場合

[設計ガイドのprofileレビューprompt](../../Customer-Data-Ontology-Design-Guide.md)を使用し、入力を承認済みのprofile表へ限定します。出力された指摘にはsource値と確認担当を付け、人が再確認します。

## 成功条件

- [ ] 全sourceにownerと機密区分がある。
- [ ] key候補のNULLと重複を実測した。
- [ ] relationship候補のorphanを実測した。
- [ ] 型、単位、通貨、タイムゾーンの不一致を記録した。
- [ ] 未計測項目を推測値で埋めていない。

[前へ: 質問とデータ認可](01-scope-and-authorization.md){ .md-button }
[次へ: Ontology論理設計](03-model.md){ .md-button .md-button--primary }
