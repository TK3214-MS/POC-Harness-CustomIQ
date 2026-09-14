# 仕入先エスカレーション・回復手順（合成参考文書）

> 文書ID: `MFG-KB-006` / 版: 1.0 / 所有者: supplier quality lead / 見直し: 四半期ごと。本書は架空の運用例である。

## 適用範囲

仕入先起因の疑いがある品質問題、回答遅延、再発、供給影響について、連絡と回復確認を統制する。

## 手順

1. `supplier_id`、`part_id`、`issue_id`、対象ロットを相互参照する。
2. supplier qualityが依頼事項、回答期限、必要証跡を明確に伝える。
3. 回答を暫定対策、原因分析、恒久対策、効果確認に分類する。
4. 生産継続への影響をquality engineerとproduction managerが確認する。
5. 回復条件を満たしたかを証跡でレビューし、未達項目を残す。

## 証跡・例外・承認

- 連絡履歴、受領資料、期限変更、検査結果、判断者を保持する。
- 無回答、再発、影響範囲不明はsupplier quality leadへエスカレーションする。
- エージェントは仕入先認定、出荷解除、契約判断を行わない。

関連文書: `supplier_quality_manual.md`、`nonconforming_material_control.md`。