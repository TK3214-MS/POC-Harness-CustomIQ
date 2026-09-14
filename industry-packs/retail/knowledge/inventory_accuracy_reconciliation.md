# 在庫精度照合手順（合成参考文書）

> 文書ID: `RET-KB-004` / 版: 1.0 / 所有者: inventory control lead / 見直し: 四半期ごと。本書は架空の小売運用例である。

## 目的と手順

記録在庫、売場・倉庫の確認値、未処理注文の差異を調査し、補充判断前のデータ品質を確保する。

1. `store_id`、`product_id`、`inventory_id`、確認時刻を記録する。
2. 売場、倉庫、入出荷中の数量を情報源別に照合する。
3. 差異を未反映取引、カウント差、破損、返品などの未確認候補に分類する。
4. 再カウント結果と修正案をinventory managerへ提示する。
5. 修正後の値、理由、実行者、承認者を監査履歴へ残す。

## 例外と承認境界

- 反復差異、商品識別不能、複数店舗影響はinventory control leadへエスカレーションする。
- エージェントは在庫修正、発注、価格変更を自動実行しない。

関連文書: `inventory_replenishment_procedure.md`、`store_operations_escalation_guide.md`。
