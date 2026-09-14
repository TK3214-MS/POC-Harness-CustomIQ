# Lab 4: Bindingと段階検証

承認された論理モデルの最小縦断スライスを非本番workspaceへ実装します。

## 1. curated table

次の場合はraw sourceへ直接bindingせず、Ontology用managed tableを作ります。

- key、型、単位、通貨、タイムゾーンの統一が必要。
- soft deleteや履歴からcurrent rowを選ぶ必要がある。
- PIIを除外・token化する必要がある。
- N:M relationship用junction tableが必要。
- source schema変更からOntology契約を隔離したい。

## 2. 最小スライス

1. gold questionを1件選ぶ。
2. 起点entityのkey、display name、必要propertyをbindingする。
3. Instancesで承認済みgold IDを確認する。
4. target entityを1つbindingする。
5. mapping tableからrelationshipを1つbindingする。
6. Graphをrefreshする。
7. 1-hop edgeを確認する。
8. 単一entity query、1-hop queryの順で実行する。

成功後だけ、残りのentity、relationship、2-hop、集計、時系列へ拡張します。

## 3. 受入テスト

| レベル | 合格条件 |
| --- | --- |
| Source | key、join、件数がsource ownerの期待と一致 |
| Instances | keyとpropertyがNULL化・誤変換されていない |
| Graph | origin、relationship、targetが期待どおり |
| Query | filterと1-hop traversalが期待結果を返す |
| Agent | ID、根拠、不足情報を区別して回答する |
| Security | 未許可データを別roleへ返さない |

## 成功条件

- [ ] 非本番workspaceで実装した。
- [ ] gold IDがInstancesに表示される。
- [ ] gold edgeがGraphに表示される。
- [ ] 単一entityと1-hop queryが成功する。
- [ ] negative testで未許可データを返さない。

[前へ: Ontology論理設計](03-model.md){ .md-button }
[次へ: 承認と変更管理](05-approve-and-operate.md){ .md-button .md-button--primary }
