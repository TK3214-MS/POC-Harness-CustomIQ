# ケース引継ぎ・職務分離手順（合成参考文書）

> 文書ID: `FIN-KB-006` / 版: 1.0 / 所有者: compliance operations lead / 見直し: 半年ごと。本書はデモ用の架空統制である。

## 適用範囲

不正ケースの担当変更、シフト引継ぎ、上位レビュー、利益相反がある場合に適用する。

## 手順

1. 引継ぎ元は確認済み事実、未確認仮説、未完了アクション、期限を分離する。
2. 使用したTool、文書、取引ID、検索期間を記録する。
3. 引継ぎ先は受領時刻と不足情報を記録し、推測で補わない。
4. 実行提案者と承認者を分離し、自己承認を認めない。
5. 利益相反や権限不足はcompliance officerへ割り当て直す。

## 承認境界

- `freeze_account`はfraud analyst、`close_fraud_case`はcompliance officerの明示承認を必要とする。
- エージェントは担当割当、承認、ケース終結を自動実行しない。

関連文書: `fraud_investigation_procedure.md`、`compliance_escalation_process.md`。