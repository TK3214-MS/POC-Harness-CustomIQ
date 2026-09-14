# 是正・予防対応ガバナンス（合成参考文書）

> 文書ID: `MFG-KB-005` / 版: 1.0 / 所有者: quality manager / 見直し: 半年ごと。本書は合成データ検証用であり、特定の品質規格を表さない。

## 目的

品質問題に対する暫定封じ込め、原因分析、是正対応、有効性確認を、事実と仮説を分離して追跡する。

## 役割と手順

1. quality engineerが問題記述、対象範囲、既知事実、未確認事項を登録する。
2. 調査チームが原因仮説ごとの確認方法と証跡を定義する。
3. action ownerが対応案、期限、影響、ロールバック方法を記録する。
4. engineering changeが必要な場合は`engineering_change_process.md`へ引き継ぐ。
5. quality engineerが有効性確認結果を記録し、quality managerが完了可否をレビューする。

## 必須証跡と承認境界

- Before/afterの検査結果、原因根拠、対応履歴、未完了リスクを保持する。
- 期限超過、再発、重大度上昇はquality managerとengineering leadへ通知する。
- 推奨は自動的な原因確定ではない。品質問題のクローズにはquality engineerの承認が必要である。

関連文書: `quality_control_procedure.md`、`engineering_change_process.md`。
