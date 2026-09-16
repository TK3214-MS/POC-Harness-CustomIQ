# Lab 3: Foundry IQ

想定時間: 60〜90分

選択したIndustry Packの手順・ポリシー文書を登録し、文書名と引用を含む回答が得られる状態にします。

## 1. 提供条件とregionを確認

このラボはAzure Blob Storage、Azure AI Search、Microsoft Foundry project、embedding/chat modelを新規作成する手順です。課金が発生する可能性があるため、作成権限と削除担当を先に決めます。

1. [Azure AI Searchのregion対応](https://learn.microsoft.com/en-us/azure/search/search-region-support){ target="_blank" rel="noopener" }でAgentic Retrievalを利用できるregionを確認します。
2. [Foundryのregion対応](https://learn.microsoft.com/en-us/azure/foundry/reference/region-support){ target="_blank" rel="noopener" }とmodel catalogで、同じregionに利用可能なembedding/chat modelとquotaがあることを確認します。
3. Storage、Search、Foundryを同じsubscription、resource group、regionに作る方針を管理者と確認します。
4. Search tierはsystem-assigned managed identityを利用できるBasic以上から、Agentic Retrievalの要件と予算に合うものを選びます。具体的な価格とtier提供状況は作成時に再確認します。

!!! danger "確認できない場合は停止"
    モデル、quota、region、tier、ライセンス、GA/Preview状態を推測で補いません。確認できない値は`TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`と記録し、管理者の確認後に再開します。Microsoft Foundry portalとAzure portalのAgentic Retrieval UIはPreview表示の場合があります。

## 2. 作業メモを作る

名前は例です。`<suffix>`には自分のイニシャルなどを使い、Azure全体で一意にする必要がある名前は作成画面で確認します。

| 項目 | 記録例 | 実値 |
| --- | --- | --- |
| Subscription ID | `00000000-0000-0000-0000-000000000000` | |
| Resource group | `rg-iiq-lab-<suffix>` | |
| Region | `<全機能を確認したregion>` | |
| Storage account | `stiiqlab<suffix>` | |
| Blob container | `<pack>-knowledge` | |
| Search service | `srch-iiq-lab-<suffix>` | |
| Search endpoint | `https://srch-iiq-lab-<suffix>.search.windows.net` | |
| Foundry resource | `ai-iiq-lab-<suffix>` | |
| Foundry project | `iiq-<pack>-project` | |
| Project endpoint | `<project Homeに表示されたendpoint>` | |
| Embedding deployment | `<検証済みdeployment name>` | |
| Chat deployment | `<検証済みdeployment name>` | |
| Knowledge Source | `ks-<pack>-policy` | |
| Knowledge Base | `kb-<pack>-operations` | |
| 構築ユーザー | `lab.user@contoso.example` | |
| Search identity object ID | `<SearchのIdentity画面に表示されたGUID>` | |

## 3. Azure resourceを作る

### 3.1 Resource groupとStorage

1. [Azure portal](https://portal.azure.com/){ target="_blank" rel="noopener" }で**Resource groups > Create**を選び、メモのsubscription、resource group、regionで作成します。
2. **Storage accounts > Create**を選び、同じresource groupとregionを指定します。
3. Account kindは汎用v2相当、Performanceは**Standard**、Redundancyはラボ要件と組織方針に合うものを選びます。価格は作成時に確認します。
4. **Security**でsecure transferを必須、minimum TLSを1.2以上、anonymous accessを無効にします。Shared Keyを無効化できるかは利用するportal/API経路と組織方針で判断し、未確認のまま変更しません。
5. **Review + create > Create**を選びます。
6. 作成後、**Data storage > Containers > + Container**を選び、メモのcontainer名を**Private (no anonymous access)**で作成します。

### 3.2 Azure AI Search

1. Azure portalで**Azure AI Search > Create**を選び、同じresource groupと確認済みregionを指定します。
2. 一意なSearch service名を入力し、確認済みtierを選んで作成します。
3. Search serviceの**Settings > Identity > System assigned**を**On**にして保存し、object IDをメモします。
4. **Settings > Keys**のAPI access controlを、role assignment中は**Both**にします。role疎通を確認後、組織方針に従って**Role-based access control**へ切り替えます。

### 3.3 Foundry resource、project、model

1. [Microsoft Foundry](https://ai.azure.com/){ target="_blank" rel="noopener" }へサインインし、**New Foundry**が有効であることを確認します。
2. 左上のproject名から**Create new project**を選び、**Advanced options**を開きます。
3. メモのresource group、Foundry resource名、project名、確認済みregionを入力して作成します。portalがFoundry resourceも作成します。
4. project Homeでproject endpointをメモします。
5. **Discover > Models**で、Blob Knowledge Sourceが現在対応するembedding modelを選び、**Deploy > Custom settings**からdeployment名とquotaを確認して作成します。
6. 同様にKnowledge Baseのanswer synthesisに対応するchat modelをdeployします。
7. **Build > Models**で両deploymentのstatusが**Succeeded**であることを確認し、model名ではなく**deployment name**をメモします。

モデルの具体名、version、deployment type、capacityはsubscriptionとregionで変わるため、このラボでは固定しません。[公式model deployment手順](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/how-to/deploy-foundry-models){ target="_blank" rel="noopener" }と作成時の利用可能一覧を優先します。

## 4. IdentityとRBACを構成

role assignmentにはOwner、User Access Administrator、Role Based Access Control Administratorなど、`Microsoft.Authorization/roleAssignments/write`を含む権限が必要です。反映に時間がかかる場合があります。

| Scope | Principal | Role | 目的 |
| --- | --- | --- | --- |
| Search service | 構築ユーザー | **Search Service Contributor** | Knowledge Source/BaseなどのSearch object管理 |
| Search service | 構築ユーザー | **Search Index Data Contributor** | index内容の読み書きとKnowledge Base retrieve |
| Storage account | 構築ユーザー | **Storage Blob Data Contributor** | portalから8文書をupload |
| Storage account | Searchのsystem-assigned identity | **Storage Blob Data Reader** | Blob Knowledge Sourceの読み取り |
| Foundry resource | Searchのsystem-assigned identity | **Cognitive Services User** | embedding/chat deploymentの利用 |
| Foundry resource | model作成者 | **Cognitive Services Contributor**または同等権限 | model deploymentの作成・管理 |

各scopeで**Access control (IAM) > Add > Add role assignment**を選び、表のPrincipalとRoleを1行ずつ割り当てます。Search identityを選ぶときは**Managed identity > Search service**を選びます。過剰なOwner権限を実行用identityへ付与しません。

## 5. 選択業界の8文書をupload

選択業界の8ファイルだけをcontainerへuploadします。別業界を混在させません。各リンクはRepositoryの原本を新しいタブで開きます。

??? example "Manufacturing"
    [quality_control_procedure.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/manufacturing/knowledge/quality_control_procedure.md){ target="_blank" rel="noopener" } · [supplier_quality_manual.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/manufacturing/knowledge/supplier_quality_manual.md){ target="_blank" rel="noopener" } · [engineering_change_process.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/manufacturing/knowledge/engineering_change_process.md){ target="_blank" rel="noopener" } · [nonconforming_material_control.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/manufacturing/knowledge/nonconforming_material_control.md){ target="_blank" rel="noopener" } · [supplier_escalation_and_recovery.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/manufacturing/knowledge/supplier_escalation_and_recovery.md){ target="_blank" rel="noopener" } · [corrective_action_governance.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/manufacturing/knowledge/corrective_action_governance.md){ target="_blank" rel="noopener" } · [quality_audit_evidence_guide.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/manufacturing/knowledge/quality_audit_evidence_guide.md){ target="_blank" rel="noopener" } · [production_release_readiness.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/manufacturing/knowledge/production_release_readiness.md){ target="_blank" rel="noopener" }

??? example "Financial Services"
    [fraud_investigation_procedure.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/financial-services/knowledge/fraud_investigation_procedure.md){ target="_blank" rel="noopener" } · [transaction_monitoring_policy.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/financial-services/knowledge/transaction_monitoring_policy.md){ target="_blank" rel="noopener" } · [investigation_evidence_handling.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/financial-services/knowledge/investigation_evidence_handling.md){ target="_blank" rel="noopener" } · [customer_contact_governance.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/financial-services/knowledge/customer_contact_governance.md){ target="_blank" rel="noopener" } · [data_quality_and_false_positive_review.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/financial-services/knowledge/data_quality_and_false_positive_review.md){ target="_blank" rel="noopener" } · [case_handoff_and_segregation.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/financial-services/knowledge/case_handoff_and_segregation.md){ target="_blank" rel="noopener" } · [case_closure_readiness.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/financial-services/knowledge/case_closure_readiness.md){ target="_blank" rel="noopener" } · [compliance_escalation_process.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/financial-services/knowledge/compliance_escalation_process.md){ target="_blank" rel="noopener" }

??? example "Retail"
    [inventory_replenishment_procedure.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/retail/knowledge/inventory_replenishment_procedure.md){ target="_blank" rel="noopener" } · [returns_and_demand_anomaly_review.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/retail/knowledge/returns_and_demand_anomaly_review.md){ target="_blank" rel="noopener" } · [store_operations_escalation_guide.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/retail/knowledge/store_operations_escalation_guide.md){ target="_blank" rel="noopener" } · [inventory_accuracy_reconciliation.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/retail/knowledge/inventory_accuracy_reconciliation.md){ target="_blank" rel="noopener" } · [supplier_disruption_response.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/retail/knowledge/supplier_disruption_response.md){ target="_blank" rel="noopener" } · [promotion_readiness_review.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/retail/knowledge/promotion_readiness_review.md){ target="_blank" rel="noopener" } · [demand_signal_handling_guide.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/retail/knowledge/demand_signal_handling_guide.md){ target="_blank" rel="noopener" } · [allocation_and_transfer_governance.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/retail/knowledge/allocation_and_transfer_governance.md){ target="_blank" rel="noopener" }

??? example "Healthcare"
    [minimum_necessary_information_handling.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/healthcare/knowledge/minimum_necessary_information_handling.md){ target="_blank" rel="noopener" } · [care_team_escalation_process.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/healthcare/knowledge/care_team_escalation_process.md){ target="_blank" rel="noopener" } · [case_history_documentation_guideline.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/healthcare/knowledge/case_history_documentation_guideline.md){ target="_blank" rel="noopener" } · [documentation_correction_and_addendum.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/healthcare/knowledge/documentation_correction_and_addendum.md){ target="_blank" rel="noopener" } · [downtime_record_reconciliation.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/healthcare/knowledge/downtime_record_reconciliation.md){ target="_blank" rel="noopener" } · [documentation_completeness_checklist.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/healthcare/knowledge/documentation_completeness_checklist.md){ target="_blank" rel="noopener" } · [documentation_incident_escalation.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/healthcare/knowledge/documentation_incident_escalation.md){ target="_blank" rel="noopener" } · [care_transition_handoff.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/healthcare/knowledge/care_transition_handoff.md){ target="_blank" rel="noopener" }

??? example "Public Sector"
    [accessible_communication_and_accommodation.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/public-sector/knowledge/accessible_communication_and_accommodation.md){ target="_blank" rel="noopener" } · [case_review_procedure.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/public-sector/knowledge/case_review_procedure.md){ target="_blank" rel="noopener" } · [fairness_and_protected_attribute_safeguards.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/public-sector/knowledge/fairness_and_protected_attribute_safeguards.md){ target="_blank" rel="noopener" } · [inter_agency_referral_guide.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/public-sector/knowledge/inter_agency_referral_guide.md){ target="_blank" rel="noopener" } · [case_records_and_evidence_handling.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/public-sector/knowledge/case_records_and_evidence_handling.md){ target="_blank" rel="noopener" } · [case_transfer_and_service_continuity.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/public-sector/knowledge/case_transfer_and_service_continuity.md){ target="_blank" rel="noopener" } · [decision_audit_and_closure_readiness.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/public-sector/knowledge/decision_audit_and_closure_readiness.md){ target="_blank" rel="noopener" } · [application_handling_policy.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/industry-packs/public-sector/knowledge/application_handling_policy.md){ target="_blank" rel="noopener" }

Storage accountの**Containers > `<pack>-knowledge` > Upload**で8ファイルを選び、upload後にblob数が`8`であることを確認します。

## 6. Knowledge Sourceを構成

1. Foundry portalで作成したprojectを開き、**Build > Knowledge**へ移動します。
2. Search serviceが未接続の場合は、接続操作からメモのSearch serviceを選びます。画面名が異なる場合は[Foundry IQの公式概要](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/what-is-foundry-iq){ target="_blank" rel="noopener" }を確認し、推測で別resourceを作りません。
3. **Create knowledge source**を選び、Source typeを**Azure Blob Storage**にします。
4. 次の値を入力します。

    | Field | Value |
    | --- | --- |
    | Name | メモの`ks-<pack>-policy` |
    | Storage account / connection | メモのStorage account。managed identityを使用 |
    | Container | メモの`<pack>-knowledge` |
    | Folder path | 空欄 |
    | Content extraction | text/Markdownを取り込める検証済み設定 |
    | Embedding model | メモのembedding **deployment name** |
    | Chat completion model | メモのchat **deployment name** |
    | Image verbalization | このMarkdown-onlyラボでは無効 |

5. 作成して同期を開始します。role付与直後の403は伝播待ちの可能性があるため、role、principal、scopeを再確認してから再試行します。
6. Knowledge Source statusで`lastSynchronizationState.endTime`に値があり、`itemsUpdatesFailed`が`0`、処理対象が8文書であることを確認します。
7. `createdResources`またはSearch serviceで自動生成されたdata source、skillset、indexer、indexを確認します。これらは直接編集しません。
8. Search ExplorerまたはKnowledge Sourceのpreviewで、文書本文とsource filenameを取得できることを確認します。

!!! note "APIとportalの提供状態"
    Agentic Retrievalのcore機能はAzure AI Search REST API `2026-04-01`でGAと記載されていますが、Azure portalとMicrosoft Foundry portalの操作はPreview表示の場合があります。実施日の[Blob Knowledge Source公式手順](https://learn.microsoft.com/en-us/azure/search/agentic-knowledge-source-how-to-blob){ target="_blank" rel="noopener" }を優先します。

<figure class="lab-image-placeholder" markdown>
    **画像差し替え位置: Knowledge Sourceの同期結果**
    `assets/images/labs/foundry-knowledge-source.png`
    <figcaption>Source名、同期完了、失敗0件が確認できる画面へ差し替えます。</figcaption>
</figure>

## 7. Knowledge Baseを作成して検証

1. **Build > Knowledge > Create knowledge base**を選び、Nameをメモの`kb-<pack>-operations`にします。
2. `ks-<pack>-policy`だけをKnowledge Sourceへ追加します。
3. メモのchat deploymentを選択し、現在の画面で利用できる場合はanswer synthesisを有効にします。
4. Retrieval instructionsへ次を入力します。

    ```text
    選択業界の手順、規程、確認事項に関する質問には、このKnowledge Sourceだけを使用する。
    根拠となる文書名と該当箇所を返し、取得できない事実を補完しない。
    ```

5. Answer instructionsへ次を入力します。

    ```text
    日本語で回答する。確認済み事実、推奨、未確認事項を分離する。
    人手承認を必要とする高影響操作を承認済みと扱わない。
    回答末尾に参照文書名を示す。
    ```

6. 保存後、PlaygroundまたはRetrieveで「このKnowledge Baseで参照できる手順文書名を一覧表示してください」と質問する。
7. 選択業界の質問を実行します。

    | 業界 | 質問 | 期待する主な引用元 |
    | --- | --- | --- |
    | Manufacturing | 品質問題をEngineering Reviewへエスカレーションする条件を、文書名と該当箇所付きで示してください。 | `quality_control_procedure.md` |
    | Financial Services | 不正調査で保持すべき記録を、文書名と該当箇所付きで示してください。 | 調査・evidence文書 |
    | Retail | 在庫がreorder pointを下回った場合の確認手順と必要な承認を、文書名付きで示してください。 | `inventory_replenishment_procedure.md` |
    | Healthcare | ケース履歴の記録完全性を確認する項目を、文書名と該当箇所付きで示してください。 | completeness/checklist文書 |
    | Public Sector | 追加情報待ち案件の確認手順を、文書名と該当箇所付きで示してください。 | case/application文書 |

8. 回答に文書名と該当箇所の引用があり、別業界の文書が含まれないことを確認する。

<figure class="lab-image-placeholder" markdown>
    **画像差し替え位置: Knowledge Baseの引用付き回答**
    `assets/images/labs/foundry-knowledge-base-result.png`
    <figcaption>質問、回答、引用元文書が一画面で確認できる状態へ差し替えます。</figcaption>
</figure>

!!! note "モデルと提供条件"
    利用可能なモデル、deployment、リージョン、課金、GA/Preview状態は固定しません。実施日時点のMicrosoft公式文書と対象subscriptionの利用可能一覧で確認してください。

## 成功条件

- [ ] 選択したpackの文書だけが取込対象である。
- [ ] Storage、Search、Foundry project、2つのmodel deploymentを作成し、実値をメモした。
- [ ] 利用者とSearch identityのroleを正しいscopeへ付与した。
- [ ] indexerが8文書を処理し、失敗0件である。
- [ ] 文書名を指定しない質問でも関連文書を取得できる。
- [ ] 回答に引用が含まれ、sourceにない手順を生成していない。

[前へ: Fabric IQ](02-fabric-iq.md){ .md-button }
[次へ: Work IQ](04-work-iq.md){ .md-button .md-button--primary }
