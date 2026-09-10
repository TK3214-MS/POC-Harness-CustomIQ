# deployment/azd/

Azure Developer CLI 構成（優先度1位、[ADR-0008](../../docs/decisions/0008-deployment-tooling-priority.md)）。

**状態: 実装済み(Phase 5)、実デプロイ未検証。** `azd` はリポジトリルートの `azure.yaml` を必要とするため、実体はリポジトリルート直下に配置している(azd のツール制約。詳細は `azure.yaml` 内のコメントを参照)。インフラ本体は [deployment/bicep/](../bicep/) を参照。

実行コマンド(テスト用 Azure サブスクリプション接続後、ユーザーが実行):

```bash
azd auth login
azd up
```

`az bicep build` によるコンパイル検証は完了しているが、`azd up` / `azd provision` による実デプロイはこの開発環境に実 Azure 認証情報がないため未実施([ADR-0012](../../docs/decisions/0012-mcp-backend-deployment-target.md))。
