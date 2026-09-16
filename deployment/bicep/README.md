# deployment/bicep/

Bicepテンプレートです。

`main.bicep`(サブスクリプションスコープ、リソースグループ作成)と`resources.bicep`(Log Analytics、Container Registry、User-Assigned Managed Identity、Container Apps Environment、MCP Backend用Container App)を提供します。Container AppはAVM `container-app-upsert:0.4.0`を使用し、内部Ingress、ACR managed identity pull、`/health` liveness probe、Industry Pack環境変数を構成します。

`az bicep build --file deployment/bicep/main.bicep --stdout`でコンパイル検証済みです。`azd`が設定する`SERVICE_MCP_BACKEND_RESOURCE_EXISTS`が必須のため、単独の`az deployment`ではなくリポジトリルートの`azd up`を使用します。実際のリソースへのデプロイは未検証です。
