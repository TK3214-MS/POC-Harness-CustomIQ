# トラックB: 実顧客Ontology設計

このトラックでは、テーブルをそのままOntologyへ移さず、業務質問から承認可能な最小モデルを作ります。既定の入力はDDL、データ辞書、profile結果、匿名化sampleです。

## データ利用の分岐

=== "metadata・匿名化sample"

    Data ownerによる実レコード利用承認がない場合の標準経路です。DDL、列定義、集計済み品質profile、匿名化した数行だけを使用します。

=== "承認済み実データ"

    Data ownerとSecurity/Privacyが利用目的、保存先、AI利用、保持期間を承認した場合だけ選択します。承認があってもSecretや資格情報はpromptへ入力しません。

## 到達点

- 3〜7件のgold questions
- source inventoryとbusiness glossary
- entity/property catalog
- relationship/binding catalog
- data quality profile
- ownerと承認記録
- 段階的な受入テスト

詳細な判断基準とprompt例は[実顧客データ向けOntology設計・構築ガイド](../../Customer-Data-Ontology-Design-Guide.md)を正本として使用します。このトラックでは、その成果物を順番に作成します。

[前へ: 業界を選択](../choose-industry.md){ .md-button }
[Lab 1を開始](01-scope-and-authorization.md){ .md-button .md-button--primary }
