# deployment/bicep/

Bicepテンプレートです。

`main.bicep`(サブスクリプションスコープ、リソースグループ作成)と`resources.bicep`(Log Analytics、Container Registry、User-Assigned Managed Identity、Container Apps Environment、MCP Backend用Container App)を提供します。

`az bicep build --file deployment/bicep/main.bicep --stdout`でコンパイル検証済みです。実際のリソースへのデプロイは対象Azure環境で実施してください。
