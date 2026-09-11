# 未解決事項

## Q11: オーケストレーション層

- **回答**: Microsoft Copilot StudioのGitHub Copilot harnessを本番のオーケストレーション層とする。
- **Foundry Agent Service**: IQを利用できる別ホストだが、本リポジトリの対象ではない。
- **根拠**: [Copilot Studio harnesses](https://learn.microsoft.com/en-us/microsoft-copilot-studio/harnesses-overview)、[本番環境構築ガイド](../Production-Environment-Setup.md)
- **状態**: 解決済み

## 残る実環境確認

- Copilot Studioから実MCP Backendへ接続する認証・ネットワーク設定
- Fabric IQ、Foundry IQ、Work IQのPreview提供、価格、リージョン、課金条件
- 実テナントでのデータ権限、Activity trace、監査ログ

不明な製品仕様は `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION` として、公式情報を確認してから更新します。
