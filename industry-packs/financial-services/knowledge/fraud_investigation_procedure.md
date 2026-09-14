# Fraud Investigation Procedure (Synthetic Reference Document)

> This is a synthetic reference document created for the Industry IQ Platform Accelerator demo. It does not represent a real institution's procedure and cites no real regulations.

## Purpose

Describes how a synthetic fraud case is triaged once a transaction is flagged.

## Triage Steps

1. A flagged transaction generates a `FraudCase` with a `risk_score` between 0 and 1.
2. A `risk_score` at or above **0.7** requires contacting the customer to verify the transaction before any further action.
3. A `FraudCase` may never be closed as `confirmed_fraud` or `closed_no_fraud` without a fraud analyst's review.

## Human Review Requirement

No fraud case may be closed automatically. No account may be frozen automatically. No transaction may be denied or reversed automatically. A fraud analyst must review the case and a compliance officer must approve closure.

## 終結前の必須証跡

ケース終結前に、次の証跡がすべて存在することを確認する。

1. 顧客確認記録: 実施日時、連絡方法、確認結果。連絡できなかった場合は試行履歴。
2. 取引比較: 対象取引、比較期間、通常パターンとの差異、比較に使用したtransaction ID。
3. 加盟店情報: merchant名、transaction type、既知の照会または異議申立て状態。
4. 関連口座確認: 同一顧客の確認対象account IDと、関連活動の有無。
5. 監査証跡: 使用した情報源、確認担当、確認日時、未取得期間。
6. 承認記録: fraud analystのレビューとcompliance officerの終結承認。

1件でも不足する場合はケースを調査中として維持し、口座凍結、取引取消、不正確定を自動実行しない。
