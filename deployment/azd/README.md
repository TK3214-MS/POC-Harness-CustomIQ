# deployment/azd/

[![日本語](https://img.shields.io/badge/%E3%81%82-%E6%97%A5%E6%9C%AC%E8%AA%9E-087F8C?style=for-the-badge)](README.md) [![English](https://img.shields.io/badge/A-English-5B6670?style=for-the-badge)](README.en.md)

Azure Developer CLI構成です。

**状態: 構成実装済み、実デプロイ未検証。** `azd`はリポジトリルートの`azure.yaml`を必要とするため、実体はリポジトリルート直下に配置しています。インフラ本体は[deployment/bicep/](../bicep/)を参照してください。

実行コマンド(承認済みAzure subscriptionへ接続後、ユーザーが実行):

```bash
azd auth login
azd env new <environment-name>
azd env set AZURE_LOCATION <location>
azd env set IIQ_INDUSTRY_PACK manufacturing
azd env set IIQ_DATA_SEED 42
azd provision --preview
azd up
```

`azd up`はsourceをACR remote buildへ送り、生成したcontainer imageを内部IngressのContainer Appへdeployします。ローカルDocker/Podmanは不要です。Bicepは`SERVICE_MCP_BACKEND_RESOURCE_EXISTS`を使うAVM upsert patternで、再provision時の最新image上書きを防ぎます。

`az bicep build`によるコンパイル検証は完了していますが、`azd up`による実デプロイは未検証です。手順と停止条件は[Custom MCP Backendラボ](../../docs/labs/advanced-mcp.md)を参照してください。
