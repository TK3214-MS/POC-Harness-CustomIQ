# Lab Cost Estimation Guide

[![日本語](https://img.shields.io/badge/%E3%81%82-%E6%97%A5%E6%9C%AC%E8%AA%9E-5B6670?style=for-the-badge)](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/docs/reference/Cost-Estimation-Guide.md) [![English](https://img.shields.io/badge/A-English-087F8C?style=for-the-badge)](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/docs/reference/Cost-Estimation-Guide.en.md)

Last verified: 2026-09-16

This page estimates consumption-based costs by solution when building and running the Industry IQ Platform Labs. Because listed prices, exchange rates, contract discounts, regions, SKUs, and GA/Preview status can change, amounts are not reproduced as fixed values. Enter quantities in the official Calculator at the time of implementation, and share the saved estimate with the approver.

!!! warning "Estimates and billed amounts are different"
    The usage frequencies on this page are examples for planning. Actual billed amounts vary based on the Azure agreement, Microsoft 365 licenses, region, model, retention time, and number of Tool calls. Treat unknown unit prices as `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`.

## 1. Usage Frequency Baseline

| Scenario | Users | Usage | Monthly interactions |
| --- | ---: | --- | ---: |
| Small lab | 1 | 20 times/month | 20 |
| Team validation | 10 | 10 times/business day x 20 days | 2,000 |
| Department pilot | 100 | 20 times/business day x 22 days | 44,000 |

An `interaction` is a unit in which a user submits one question and receives one final answer. For compound questions, multiple Tools may be called within one interaction.

## 2. Billing Components by Solution

| Solution | Main billing components | Quantities to enter in the Calculator | Cost control checks |
| --- | --- | --- | --- |
| Fabric IQ | Fabric capacity, OneLake storage, optional Spark autoscale/overage | SKU, running hours, stored GB, Spark CU hours | Check whether an existing capacity can be used and whether it can be paused after the lab. |
| Foundry IQ | Azure AI Search, Blob Storage, embedding/chat model, agentic retrieval | Search tier/SU or CU hours, index GB, Blob GB/operation count, input/output/embedding tokens | Register only 8 documents, and avoid unnecessary indexer runs and continuous operation. |
| Work IQ | Copilot Credits, required Microsoft 365 licenses | Interaction count, Tool/action count, tenant graph grounding, licenses for target users | Limit test users and the spending policy, and set a monthly cap. |
| Copilot Studio | Copilot Credits, agent action, generative answer, optional AI tool tokens | Credits per feature x execution count | Use Activity trace to measure the actual number of calls per answer. |
| Custom MCP Backend (optional) | Container Apps compute, Log Analytics, Container Registry | vCPU seconds, GiB seconds, requests, log GB, registry tier | Check whether scale-to-zero is available when unused, and delete it after the lab. |

## 3. Estimate with Azure Pricing Calculator

Open the [Azure Pricing Calculator](https://azure.microsoft.com/pricing/calculator/){ target="_blank" rel="noopener" }, sign in with the contract account, and apply the currency and contract pricing.

### Fabric IQ

1. Add **Microsoft Fabric**, then select the region and capacity SKU that will actually be used.
2. If it will run only during lab hours, record `running hours/month`. If using an existing shared capacity, check overage in capacity metrics because the incremental lab cost is not necessarily zero.
3. Enter the GB for managed tables and retained data under **OneLake Storage**.
4. Add Spark CU hours only when enabling Autoscale Billing for Spark in a Notebook.

Manage the approximate monthly cost with the following formula.

$$
C_{Fabric}=C_{capacity\times hours}+C_{OneLake\ GB}+C_{Spark\ CUh}+C_{overage}
$$

Recheck the SKU and CU using [Fabric pricing](https://azure.microsoft.com/pricing/details/microsoft-fabric/){ target="_blank" rel="noopener" } and the [Fabric capacity estimator](https://www.microsoft.com/en-us/microsoft-fabric/capacity-estimator){ target="_blank" rel="noopener" }.

### Foundry IQ

1. Add **Azure AI Search**, and enter the Dedicated tier and number of Search Units created for the lab, or the available and selected Serverless meter.
2. Add **Storage Accounts**, and enter Standard GPv2, redundancy, Hot tier, stored GB, and the number of read/write/list operations.
3. Add **Azure OpenAI Service** or the meter for the Foundry model actually deployed, and enter embedding input tokens, chat input tokens, and chat output tokens separately.
4. If agentic retrieval, semantic ranker, or similar features were used, enter the measured tokens/requests in the additional Azure AI Search meter.

$$
C_{Foundry}=C_{Search}+C_{Blob}+C_{embedding\ input}+C_{chat\ input}+C_{chat\ output}+C_{agentic\ retrieval}
$$

Check [Azure AI Search pricing](https://azure.microsoft.com/pricing/details/search/){ target="_blank" rel="noopener" }, [Blob Storage pricing](https://azure.microsoft.com/pricing/details/storage/blobs/){ target="_blank" rel="noopener" }, and [Azure OpenAI pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/){ target="_blank" rel="noopener" } on the implementation date. Add together the meters for Search, Storage, models, and other resources used under the Foundry project, rather than treating the Foundry project itself as a meter.

## 4. Estimate Copilot Credits

Enter the agent type, traffic, orchestration, knowledge, and tools in the [Copilot Studio agent usage estimator](https://microsoft.github.io/copilot-studio-estimator/){ target="_blank" rel="noopener" }. The following rates are planning units verified against the [official billing rates](https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-messages-management){ target="_blank" rel="noopener" } on 2026-09-16. Always verify the latest values again.

| Feature | Planning rate |
| --- | ---: |
| Classic answer | 1 Copilot Credit |
| Generative answer | 2 Copilot Credits |
| Agent action | 5 Copilot Credits |
| Tenant graph grounding | 10 Copilot Credits |
| Basic AI tool | 0.1 Copilot Credit / 1K tokens |
| Standard AI tool | 1.5 Copilot Credits / 1K tokens |
| Premium AI tool | 10 Copilot Credits / 1K tokens |

For employee-facing use by users licensed for Microsoft 365 Copilot, qualifying features may be no-charge. Verify the treatment of eligible channels, authenticated users, fair usage, Work IQ, and bring-your-own-model against [Copilot Studio licensing](https://learn.microsoft.com/en-us/microsoft-copilot-studio/billing-licensing){ target="_blank" rel="noopener" } and the contract terms.

### Credit Planning Values by Frequency

The following table is an example for cap management that assumes `1 Generative answer = 2 credits` for a simple question and `1 Generative answer + 3 Agent actions = 17 credits` for a compound question. Replace these values with actual billing from Activity trace and consumption in the Power Platform admin center. If a Work IQ-specific additional meter cannot be confirmed, add `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`.

| Scenario | Monthly interactions | Simple questions only | Compound questions only |
| --- | ---: | ---: | ---: |
| Small lab | 20 | 40 credits | 340 credits |
| Team validation | 2,000 | 4,000 credits | 34,000 credits |
| Department pilot | 44,000 | 88,000 credits | 748,000 credits |

$$
Credits_{month}=\sum(feature\ rate\times feature\ executions)+AI\ tool\ token\ credits
$$

For conversion to Japanese yen, use the unit price displayed at the time of implementation in the Power Platform admin center or Azure billing policy.

$$
C_{Copilot}=Credits_{month}\times Price_{current\ contract}
$$

## 5. Estimate Record Template

| Item | Recorded value |
| --- | --- |
| Estimate date / currency | |
| Azure agreement / subscription | |
| Region | |
| Fabric SKU / running hours / OneLake GB | |
| Search tier / SU or CU hours / index GB | |
| Blob GB / read / write / list | |
| Embedding model / input tokens | |
| Chat model / input tokens / output tokens | |
| Monthly interactions / Tool call count | |
| Copilot Credits / applicable unit price | |
| Scope included in existing licenses | |
| Total monthly cost / budget cap | |
| Estimate URL / approver | |

After completing the lab, compare the estimate with Azure Cost Management, Fabric Capacity Metrics, and Copilot Credit consumption in the Power Platform admin center, and record the reasons for any differences.
