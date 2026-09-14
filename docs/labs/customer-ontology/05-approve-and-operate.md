# Lab 5: 承認と変更管理

設計成果物、検証結果、運用責任を確認し、本番反映の可否を人が判断します。

## 1. 承認

| 承認者 | 確認対象 |
| --- | --- |
| Business owner | gold questions、業務定義、禁止事項 |
| Data owner | source利用、保持、共有範囲 |
| Data steward | entity、property、relationship、品質基準 |
| Security/Privacy | 公開property、PII、role別negative test |
| Fabric administrator | workspace、binding、refresh、監視 |
| Test owner | gold dataset、受入結果、残課題 |

生成AIが作成した候補を承認記録の代わりにしません。

## 2. 運用

- refresh頻度と実行owner
- refresh失敗の通知先
- source schema変更の通知方法
- gold questionsの回帰実行頻度
- Preview仕様変更の確認owner
- incident時のActivity traceとCorrelation ID保管方法

Graph refreshは実施時点のcapacityと費用への影響を確認し、個別行の更新ごとではなく承認済みの単位で計画します。

## 3. schema変更

sourceの列名、型、table名、key、status値、更新方式が変わる場合は、非本番workspaceでbindingとgold questionsへの影響を確認します。生成AIによる差分要約を利用しても、互換性とリリース可否はownerが判断します。

## 完了条件

- [ ] 必須成果物にowner、status、approved by、approved at、source referenceがある。
- [ ] role別negative testを含む受入結果を保存した。
- [ ] refresh、監視、障害対応、schema変更のownerがいる。
- [ ] 残課題と本番反映判断を記録した。

[前へ: Bindingと段階検証](04-bind-and-validate.md){ .md-button }
[ラボホームへ戻る](../index.md){ .md-button .md-button--primary }
