# ADR-0008: デプロイツールの優先順位

- ステータス: Accepted
- 日付: 2026-09-08

## コンテキスト

Azureデプロイ方式は、MCP Backendの現行構成に合わせてAzure Developer CLIとBicepに限定する。未実装の方式を完成済みとして記載しない。

## 決定

Phase 5 で次の優先順位に従って実装する。

1. Azure Developer CLI (`azd`)（`deployment/azd/`）
2. Bicep（`deployment/bicep/`）

## 影響

- README・デプロイガイドには実装済みの方式のみを「利用可能」と記載し、未実装の方式は「未実装」と明記する。
- テスト用 Azure サブスクリプションが利用可能になった段階で、`azd up` の実行結果を実測してドキュメントに記録する（未実測の場合は「設計上の想定」であることを明記する）。
