# Demand Signal Handling Guide (Synthetic Reference Document)

> This is a synthetic reference document created for the Industry IQ Platform Accelerator demo. It does not represent a real retailer's guide.

## Signal Types

- `spike`: demand trending sharply upward.
- `decline`: demand trending downward.
- `seasonal`: expected seasonal pattern, generally lower priority for urgent action.

## Review Requirement

Demand signals inform recommendations only. Pricing changes and reorders always require human approval from a merchandising lead or inventory manager (see `industry-packs/retail/manifest.yaml` `human_approval_rules`).

## 販促期間中の需要シグナル

販促期間と需要上昇が重なる場合は、次の順序で確認する。

1. promotion ID、対象期間、signal ID、検知日時、trend percentを同じレビュー記録へ残す。
2. 店舗別客数、取引頻度、SKU販売速度、現在庫、入荷予定を確認する。
3. 過去の通常期間または同種販促を比較し、販促だけを原因として断定しない。
4. 在庫がreorder point未満でも、既存注文と店舗間移送候補を確認するまで新規発注を確定しない。
5. 需要シグナルと販促想定が矛盾する場合は、merchandising leadへレビューを依頼する。

エージェントは推奨数量、根拠、不足情報を提示できるが、発注や価格変更は実行しない。
