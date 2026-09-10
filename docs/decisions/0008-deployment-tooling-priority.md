# ADR-0008: デプロイツールの優先順位

- ステータス: Accepted
- 日付: 2026-09-08

## コンテキスト

指示書 §15 は、Terraform / Bicep / Azure Developer CLI を全て同時に完全実装することが合理的でない場合の優先順位（1. azd、2. Bicep、3. Terraform）を明示し、未完成の方式を完成済みとして記載しないことを求めている。[docs/decisions/open-questions.md](../decisions/open-questions.md) の Q4 の回答（テスト用 Azure サブスクリプションで Full Hybrid テストを行いたい）により、Phase 5 のデプロイ実装は実際に検証可能になる見込みである。

## 決定

Phase 5 で次の優先順位に従って実装する。

1. Azure Developer CLI (`azd`)（`deployment/azd/`）
2. Bicep（`deployment/bicep/`）
3. Terraform（`deployment/terraform/`、時間的余裕がある場合のみ）

## 影響

- README・デプロイガイドには実装済みの方式のみを「利用可能」と記載し、未実装の方式は「未実装」と明記する。
- テスト用 Azure サブスクリプションが利用可能になった段階で、`azd up` の実行結果を実測してドキュメントに記録する（未実測の場合は「設計上の想定」であることを明記する）。
