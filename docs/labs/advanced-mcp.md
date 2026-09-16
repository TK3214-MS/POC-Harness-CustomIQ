# 任意ラボ: Custom MCP Backend

このラボは任意です。Fabric IQ、Foundry IQ、Work IQでは提供しない顧客固有Business SystemのToolをCopilot Studioへ接続する場合だけ実施します。

この手順でデプロイする実装は、選択したIndustry Packの**合成dataset**をmemory上に生成する検証用Backendです。顧客Business System接続と受信request認証は実装していません。

## 開始条件

- 合成サンプルデータラボを完了している。
- Azureリソース作成と費用発生について承認を得ている。
- HTTPS endpoint、認証、Secret管理、network境界の設計担当者が決まっている。
- 現在のMCP Backendには受信request認証が未実装であることを理解している。

!!! danger "公開しない"
    認証とnetwork境界を構成せずにMCP Backendをpublic ingressへ公開しません。

## 1. ローカル契約を検証

リポジトリルートで実行します。

```bash
source .venv/bin/activate
pytest tests/contract/test_mcp_tool_contract.py -q
pytest tests/integration/test_mcp_protocol_server.py -q
python scripts/demo/test_mcp_protocol_connectivity.py
```

最後のscriptはローカルsocketで公式MCP client SDKから`initialize`、`tools/list`、`tools/call`を検証します。

## 2. azd環境を設定

Azure resource作成権限と費用承認を得た担当者が実行します。`<environment-name>`と`<location>`を承認済みの値へ置き換えます。

```bash
azd auth login
azd env new <environment-name>
azd env set AZURE_LOCATION <location>
azd env set IIQ_INDUSTRY_PACK manufacturing
azd env set IIQ_DATA_SEED 42
azd provision --preview
```

`IIQ_INDUSTRY_PACK`には`manufacturing`、`financial-services`、`retail`、`healthcare`、`public-sector`のいずれかを指定します。`azd provision --preview`の差分で、Log Analytics、ACR、managed identity、Container Apps environment、内部IngressのContainer Appだけが対象であることを確認します。

## 3. Azureへデプロイ

previewを承認者が確認した後に実行します。

```bash
azd up
```

`azd up`はBicepをprovisionし、Dockerfileとrepository rootのbuild contextをACR remote buildへ送り、生成imageを`azd-service-name: mcp-backend` tagのContainer Appへdeployします。ローカルのDocker/Podmanは不要です。`azd provision`を再実行しても最新deploy imageをplaceholderへ戻さないよう、Bicepは公式AVM upsert patternを使用します。

!!! note "replicaと費用"
        AVM upsert moduleの制約により、この構成は最小replicaを`1`、最大を`2`に設定します。価格は記載しません。実施日時点の料金と予算を確認してください。

<figure class="lab-image-placeholder" markdown>
    **画像差し替え位置: Container App概要**
    `assets/images/labs/mcp-container-app-overview.png`
    <figcaption>Internal ingress、最新revision、image、状態が確認できる画面へ差し替えます。</figcaption>
</figure>

## 4. 内部endpointを検証

出力をshellへ読み込みます。

```bash
eval "$(azd env get-values)"
az containerapp show \
    --resource-group "$AZURE_RESOURCE_GROUP" \
    --name "$MCP_BACKEND_NAME" \
    --query "{fqdn:properties.configuration.ingress.fqdn,external:properties.configuration.ingress.external,latestReady:properties.latestReadyRevisionName,image:properties.template.containers[0].image}" \
    --output table
```

`external`が`false`、`latestReady`とACR imageが表示されることを確認します。次に、running container内からhealth endpointを呼び出します。imageには`curl`を含めないためPython standard libraryを使用します。

```bash
az containerapp exec \
    --resource-group "$AZURE_RESOURCE_GROUP" \
    --name "$MCP_BACKEND_NAME" \
    --command "python -c \"import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8000/health').read().decode())\""
```

起動ログも確認します。

```bash
az containerapp logs show \
    --resource-group "$AZURE_RESOURCE_GROUP" \
    --name "$MCP_BACKEND_NAME" \
    --type console \
    --tail 100
```

## 5. Copilot Studio接続の停止条件

内部Ingressはインターネット上のCopilot Studioから直接到達できません。またBackendに受信request認証がないため、public ingressへの切り替えをこのラボでは行いません。次のすべてを別設計で満たすまで、**Tools > Add Tool > Model Context Protocol**への登録は未完了として扱います。

- Copilot Studioが到達できる承認済みnetwork経路
- Copilot Studio対応の受信認証
- Secret管理、rate limit、監査ログ、host/origin allowlist
- threat model、Security承認、negative test

## 完了条件

- [ ] ローカルのcontract、integration、公式MCP client connectivity testが成功した。
- [ ] `azd provision --preview`を承認者が確認した。
- [ ] ACR remote buildを含む`azd up`が成功し、latest ready revisionに生成imageがある。
- [ ] Ingressの`external`が`false`である。
- [ ] Container内から`/health`が成功した。
- [ ] Copilot Studio接続を認証実装済みと誤記していない。

実装と契約は[MCP Backendドキュメント](../mcp/README.md)、公開前の要件は[MCPセキュリティガイド](../mcp/MCP-Security-Guide.md)、本番構成の位置付けは[本番環境構築ガイド](../Production-Environment-Setup.md)を参照してください。
