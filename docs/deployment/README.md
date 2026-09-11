# MCP Backendデプロイ

本リポジトリでAzureへデプロイする対象は、Copilot Studioから業務ツールとして呼び出すMCP Backendです。Fabric IQ、Foundry IQ、Work IQのSaaS環境は、[本番環境構築ガイド](../Production-Environment-Setup.md)に従って各サービス側で構成します。

## 手順

1. [deployment/azd/](../../deployment/azd/)のAzure Developer CLI構成を確認する。
2. [deployment/bicep/](../../deployment/bicep/)と[deployment/containers/](../../deployment/containers/)を確認する。
3. Azureへログインし、対象subscription・location・environmentを選択する。
4. `azd provision`と`azd deploy`を実行する。実行前に必ずBicepのwhat-ifと権限を確認する。
5. HTTPSのMCP endpointが利用可能になったら、[本番環境構築ガイド](../Production-Environment-Setup.md)のCopilot Studio接続手順を実施する。

```bash
azd auth login
azd env select <environment-name>
azd provision
azd deploy
```

実Azureへのデプロイ結果、実際のendpoint、認証方式、権限は環境ごとに記録してください。IQ用の環境変数やAdapter設定は行いません。
