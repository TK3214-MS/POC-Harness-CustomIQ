# Lab 3: Ontology論理設計

gold questionsとprofile結果から、最小のentity、property、relationshipを設計します。

## 1. entity catalog

独立したidentity、lifecycle、ownerを持ち、質問の主語・目的語・絞り込み対象になる概念をentity候補とします。初期モデルは質問に必要な範囲へ限定します。

| 必須項目 | 内容 |
| --- | --- |
| entity name | 利用者が使う短く一意な名称 |
| definition | 含むものと含まないもの |
| key | 安定したstringまたはinteger候補 |
| display name | 利用者向け表示property |
| owner | 定義の承認者 |
| source | curated table候補 |

## 2. property catalog

key、表示名、状態、分類、時刻、質問に必要な測定値を優先します。各propertyに型、単位、機密区分、source column、採用理由を記録します。

## 3. relationship catalog

| 必須項目 | 内容 |
| --- | --- |
| name | Ontology全体で一意な動詞表現 |
| origin / target | 方向を明示 |
| mapping table | 両entity keyを同じ行に持つtable |
| matched columns | origin key列とtarget key列 |
| cardinality | 1:1、1:N、N:M |
| evidence | FK、業務定義、source owner確認 |

N:Mは1行1組のjunction tableへ正規化します。`has`や`relatesTo`だけを複数箇所で使わず、質問から関係の意味が分かる名前にします。

## 4. question coverage

各gold questionについて、start entity、filter property、relationship path、期待結果を1行で記録します。経路を作れない質問は、モデル不足かスコープ外かをBusiness ownerが判断します。

## 成功条件

- [ ] 全entityに定義、key、ownerがある。
- [ ] 全propertyに型、単位、機密区分、sourceがある。
- [ ] 全relationshipに方向、mapping table、matched columns、根拠がある。
- [ ] 全gold questionにquery pathまたはスコープ外判断がある。
- [ ] Data stewardとSource system ownerが候補をレビューした。

[前へ: Source inventory](02-inventory-and-profile.md){ .md-button }
[次へ: Bindingと段階検証](04-bind-and-validate.md){ .md-button .md-button--primary }
