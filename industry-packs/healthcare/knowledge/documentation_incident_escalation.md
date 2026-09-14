# 記録インシデント・エスカレーション手順（合成参考文書）

> 文書ID: `HC-KB-008` / 版: 1.0 / 所有者: clinical governance lead / 見直し: 四半期ごと。本書は実在する医療機関の事故対応基準ではない。

## 対象と手順

患者取り違え疑義、記録欠落、誤った関連付け、権限外表示、監査履歴欠損を対象とする。

1. 対象ID、発見時刻、情報源、発見者、影響候補を記録する。
2. 原記録を変更せず、追加アクセスや共有を最小限にする。
3. 確認済み事実と影響仮説を分離する。
4. clinical governance leadとprivacy operations leadへ所定経路で通知する。
5. 対応、確認者、解消条件、再確認結果を監査履歴へ残す。

## 承認境界

- エージェントは影響、診断、治療上の結論を確定しない。
- `close_case_review`にはclinicianの承認が必要であり、インシデント未解決時は終結を提案しない。

## エスカレーション判定表

| 確認された条件 | 対応 | 所有ロール | 期限 |
| --- | --- | --- | --- |
| 単一記録の非臨床項目に訂正漏れがある | 原記録を保持して訂正候補を記録し、clinicianへ確認を依頼 | documentation reviewer | 次回レビューまで |
| 直近確認記録の20%超、または4件以上の合成患者記録に同種欠損がある | care team escalationを開始 | documentation lead | 当日中 |
| 診断、投薬、検査結果に関する記録欠損または誤関連付けがある | clinical flagを付け、clinicianとclinical governance leadへ通知 | care coordination lead | 4時間以内（合成SLA） |
| 権限外表示または監査履歴欠損がある | 追加共有を停止し、privacy operations leadへ通知 | documentation lead | 即時 |

件数、割合、臨床影響は取得済み記録だけから算出し、不足時は推測しない。

関連文書: `care_team_escalation_process.md`、`minimum_necessary_information_handling.md`。
