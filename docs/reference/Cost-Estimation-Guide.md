# ラボコスト見積もりガイド

最終確認日: 2026-09-16

このページでは、Industry IQ Platform Labsを構築・実行する際の従量課金コストを、ソリューション別に見積もります。表示価格、為替、契約割引、リージョン、SKU、GA/Preview状態は変わるため、金額を固定値として転記しません。実施時点の公式Calculatorへ数量を入力し、保存した見積もりを承認者と共有してください。

!!! warning "見積もりと請求額は異なります"
    このページの利用頻度は計画用の例です。実際の請求額はAzure契約、Microsoft 365ライセンス、リージョン、モデル、保持時間、Tool呼び出し回数によって変わります。不明な単価は`TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`として扱ってください。

## 1. 利用頻度の基準

| シナリオ | 利用者 | 利用量 | 月間interaction |
| --- | ---: | --- | ---: |
| 小規模ラボ | 1人 | 20回/月 | 20 |
| チーム検証 | 10人 | 10回/営業日 × 20日 | 2,000 |
| 部門パイロット | 100人 | 20回/営業日 × 22日 | 44,000 |

`interaction`はユーザーが質問を1回送信し、最終回答を1回受け取る単位です。複合質問では1 interaction内で複数Toolが呼び出される場合があります。

## 2. ソリューション別の課金要素

| ソリューション | 主な課金要素 | Calculatorへ入力する数量 | コストを抑える確認 |
| --- | --- | --- | --- |
| Fabric IQ | Fabric capacity、OneLake storage、任意のSpark autoscale/overage | SKU、稼働時間、保存GB、Spark CU時間 | 既存capacityを使用できるか、ラボ後にpauseできるか確認します。 |
| Foundry IQ | Azure AI Search、Blob Storage、embedding/chat model、agentic retrieval | Search tier/SUまたはCU時間、index GB、Blob GB/操作数、input/output/embedding token | 8文書だけを登録し、不要なindexer実行と常時稼働を避けます。 |
| Work IQ | Copilot Credits、必要なMicrosoft 365ライセンス | interaction数、Tool/action数、tenant graph grounding、対象ユーザーのライセンス | test userとspending policyを限定し、月次上限を設定します。 |
| Copilot Studio | Copilot Credits、agent action、generative answer、任意のAI tool token | 機能別credit × 実行回数 | Activity traceで1回答当たりの実呼び出し数を測定します。 |
| Custom MCP Backend（任意） | Container Apps compute、Log Analytics、Container Registry | vCPU秒、GiB秒、request、log GB、registry tier | 未使用時scale-to-zero可否を確認し、ラボ後に削除します。 |

## 3. Azure Pricing Calculatorで見積もる

[Azure Pricing Calculator](https://azure.microsoft.com/pricing/calculator/){ target="_blank" rel="noopener" }を開き、契約アカウントでサインインして通貨と契約価格を反映します。

### Fabric IQ

1. **Microsoft Fabric**を追加し、実際に使用するregionとcapacity SKUを選択します。
2. ラボ時間だけ起動する場合は、`稼働時間/月`を記録します。既存共有capacityを利用する場合は、ラボ増分がゼロとは限らないためcapacity metricsでoverageを確認します。
3. **OneLake Storage**へmanaged tableと保持データのGBを入力します。
4. NotebookでAutoscale Billing for Sparkを有効にする場合だけ、SparkのCU時間を追加します。

月額概算は次の式で管理します。

$$
C_{Fabric}=C_{capacity\times hours}+C_{OneLake\ GB}+C_{Spark\ CUh}+C_{overage}
$$

[Fabric料金](https://azure.microsoft.com/pricing/details/microsoft-fabric/){ target="_blank" rel="noopener" }と[Fabric capacity estimator](https://www.microsoft.com/en-us/microsoft-fabric/capacity-estimator){ target="_blank" rel="noopener" }でSKUとCUを再確認してください。

### Foundry IQ

1. **Azure AI Search**を追加し、ラボで作成したDedicated tierとSearch Unit数、または利用可能で選択済みのServerless meterを入力します。
2. **Storage Accounts**を追加し、Standard GPv2、redundancy、Hot tier、保存GB、read/write/list操作数を入力します。
3. **Azure OpenAI Service**または実際にdeployしたFoundry modelのmeterを追加し、embedding input token、chat input token、chat output tokenを分けて入力します。
4. Agentic retrieval、semantic rankerなどを使用した場合は、Azure AI Searchの追加meterへ実測token/requestを入力します。

$$
C_{Foundry}=C_{Search}+C_{Blob}+C_{embedding\ input}+C_{chat\ input}+C_{chat\ output}+C_{agentic\ retrieval}
$$

[Azure AI Search料金](https://azure.microsoft.com/pricing/details/search/){ target="_blank" rel="noopener" }、[Blob Storage料金](https://azure.microsoft.com/pricing/details/storage/blobs/){ target="_blank" rel="noopener" }、[Azure OpenAI料金](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/){ target="_blank" rel="noopener" }を実施日に確認してください。Foundry project自体ではなく、配下で使用するSearch、Storage、modelなどのmeterを合算します。

## 4. Copilot Creditsを見積もる

[Copilot Studio agent usage estimator](https://microsoft.github.io/copilot-studio-estimator/){ target="_blank" rel="noopener" }へagent type、traffic、orchestration、knowledge、toolsを入力します。次のrateは2026-09-16に[公式billing rates](https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-messages-management){ target="_blank" rel="noopener" }で確認した計画用の単位です。最新値を必ず再確認してください。

| 機能 | 計画用rate |
| --- | ---: |
| Classic answer | 1 Copilot Credit |
| Generative answer | 2 Copilot Credits |
| Agent action | 5 Copilot Credits |
| Tenant graph grounding | 10 Copilot Credits |
| Basic AI tool | 0.1 Copilot Credit / 1K tokens |
| Standard AI tool | 1.5 Copilot Credits / 1K tokens |
| Premium AI tool | 10 Copilot Credits / 1K tokens |

Microsoft 365 Copilotライセンスユーザーのemployee-facing利用には、条件を満たす機能がno-chargeになる場合があります。対象チャネル、認証ユーザー、fair usage、Work IQ、bring-your-own-modelの扱いを[Copilot Studio licensing](https://learn.microsoft.com/en-us/microsoft-copilot-studio/billing-licensing){ target="_blank" rel="noopener" }と契約条件で確認してください。

### 頻度別のcredit計画値

次の表は、単純質問を`Generative answer 1回 = 2 credits`、複合質問を`Generative answer 1回 + Agent action 3回 = 17 credits`と仮定した上限管理用の例です。実請求はActivity traceとPower Platform admin centerの消費量で置き換えてください。Work IQ固有の追加meterが確認できない場合は`TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`を加算します。

| シナリオ | 月間interaction | 単純質問のみ | 複合質問のみ |
| --- | ---: | ---: | ---: |
| 小規模ラボ | 20 | 40 credits | 340 credits |
| チーム検証 | 2,000 | 4,000 credits | 34,000 credits |
| 部門パイロット | 44,000 | 88,000 credits | 748,000 credits |

$$
Credits_{month}=\sum(feature\ rate\times feature\ executions)+AI\ tool\ token\ credits
$$

円換算は、Power Platform admin centerまたはAzure billing policyに表示される実施時点の単価を使用します。

$$
C_{Copilot}=Credits_{month}\times Price_{current\ contract}
$$

## 5. 見積もり記録テンプレート

| 項目 | 記録値 |
| --- | --- |
| 見積日 / 通貨 | |
| Azure契約 / subscription | |
| Region | |
| Fabric SKU / 稼働時間 / OneLake GB | |
| Search tier / SUまたはCU時間 / index GB | |
| Blob GB / read / write / list | |
| Embedding model / input token | |
| Chat model / input token / output token | |
| 月間interaction / Tool呼び出し数 | |
| Copilot Credits / 適用単価 | |
| 既存ライセンスに含まれる範囲 | |
| 月額合計 / 予算上限 | |
| 見積もりURL / 承認者 | |

ラボ完了後はAzure Cost Management、Fabric Capacity Metrics、Power Platform admin centerのCopilot Credit consumptionを見積もりと照合し、差分理由を記録してください。
