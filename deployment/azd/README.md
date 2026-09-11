# deployment/azd/

Azure Developer CLI構成です。

**状態: 実装済み(Phase 5)、実デプロイ未検証。** `azd` はリポジトリルートの `azure.yaml` を必要とするため、実体はリポジトリルート直下に配置している(azd のツール制約。詳細は `azure.yaml` 内のコメントを参照)。インフラ本体は [deployment/bicep/](../bicep/) を参照。

実行コマンド(テスト用 Azure サブスクリプション接続後、ユーザーが実行):

```bash
azd auth login
azd up
```

`az bicep build`によるコンパイル検証は完了しているが、`azd up` / `azd provision`による実デプロイは対象Azure環境で実施してください。手順は[本番環境構築ガイド](../../docs/Production-Environment-Setup.md)を参照してください。
