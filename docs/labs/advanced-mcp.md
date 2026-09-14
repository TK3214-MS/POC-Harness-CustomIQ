# 上級ラボ: MCP Backend

このラボは任意です。Fabric IQ、Foundry IQ、Work IQでは提供しない顧客固有Business SystemのToolをCopilot Studioへ接続する場合だけ実施します。

## 開始条件

- トラックAまたはBを完了している。
- Azureリソース作成と費用発生について承認を得ている。
- HTTPS endpoint、認証、Secret管理、network境界の設計担当者が決まっている。
- 現在のMCP Backendには受信request認証が未実装であることを理解している。

!!! danger "公開しない"
    認証とnetwork境界を構成せずにMCP Backendをpublic ingressへ公開しません。

実装と契約は[MCP Backendドキュメント](../mcp/README.md)、Azure構築の位置付けは[本番環境構築ガイド](../Production-Environment-Setup.md)を参照してください。
