# Lab 6: Copilot Studioエージェントをテスト

想定時間: 30〜45分

このページでは、Lab 5で開発したエージェントを変更せず、テストと結果記録だけを実施します。質問の追加やTool設定の修正が必要な場合は、テスト結果を保存してから[Copilot Studioの構成](05-copilot-studio.md)へ戻ります。

## 1. テスト条件を固定

| 項目 | 記録値 |
| --- | --- |
| Industry Pack | `<pack>` |
| Agent / environment | |
| 接続ユーザー | |
| Fabric workspace / Ontology | |
| Foundry Knowledge Base | |
| Work IQ test user | |
| 実行日時 / timezone | |
| Dataset | `small` |

ブラウザー、ユーザー、接続先、データ版をテスト中に変更しません。初回実行はウォームアップとして分けて記録します。

## 2. 必須テストを実行

[IQレイヤー別テスト実行・評価ガイド](../../evaluation/Copilot-Studio-IQ-Layer-Test-Catalog.md)を新しいタブで開き、選択業界の展開パネルから次の順で実行します。

1. `F-01`と`F-02`でFabric IQのschemaと既知IDを確認します。
2. `K-01`でFoundry IQの文書名と引用を確認します。
3. `W-01`でWork IQのユーザー権限とM365横断取得を確認します。
4. 単一レイヤーがすべて成功した後、`X-01`と`X-02`を実行します。

各質問後にActivity traceを開き、期待Tool、実際のTool、入力、結果、エラー、Correlation IDを記録します。

## 3. 結果を記録

| Test ID | 実際のTool | 根拠 / 引用 | 応答時間 | 判定 | 残課題 |
| --- | --- | --- | ---: | --- | --- |
| `<pack>-F-01` | | | | Pass / Partial / Fail | |
| `<pack>-F-02` | | | | Pass / Partial / Fail | |
| `<pack>-K-01` | | | | Pass / Partial / Fail | |
| `<pack>-W-01` | | | | Pass / Partial / Fail | |
| `<pack>-X-01` | | | | Pass / Partial / Fail | |
| `<pack>-X-02` | | | | Pass / Partial / Fail | |

想定回答例は完全一致を要求する正解文ではありません。値、引用元、情報源分離、安全性を比較するための基準として使用します。

## 成功条件

- [ ] 単一レイヤーの必須テストがすべて`Pass`です。
- [ ] 複合回答でFabric、Foundry、Work IQの根拠が分離されています。
- [ ] 0件、権限不足、Tool失敗を成功として扱っていません。
- [ ] 高影響判断を自動実行せず、必要な人手承認を示しています。
- [ ] 想定回答例との差異を残課題へ記録しています。

[前へ: Copilot Studioを構成](05-copilot-studio.md){ .md-button }
[次へ: 完了確認](06-complete.md){ .md-button .md-button--primary }
