# Lab 2: Fabric IQ

想定時間: 60分

このLabでは、選択したIndustry PackのCSVをLakehouse managed tableへ変換し、Ontologyのentity、property、relationshipを構成します。

## 1. tableを準備

1. ラボ用Fabric workspaceでLakehouseを作成する。
2. `industry-packs/<pack>/sample-data/fabric/*.csv`を`Files/demo/`へアップロードする。
3. CSVごとに拡張子を除いた名前のmanaged tableを作成する。
4. ID列をstring、日時列をdatetime、数値列を適切な数値型として確認する。

!!! warning "binding制約"
    OneLake security、external table、Delta column mappingなどの対応状況は、実施日時点の[公式data binding文書](https://learn.microsoft.com/en-us/fabric/iq/ontology/how-to-bind-data)で確認します。利用できないsourceを無理にbindingせず、ラボ用managed tableへ変換します。

## 2. entityを構成

1. `industry-packs/<pack>/ontology/entities.yaml`を開く。
2. Ontology itemを作成する。
3. `entities`の各項目をentity typeとして作成する。
4. `dataset_key`と同名のmanaged tableをstatic dataへbindingする。
5. `identifier_field`をentity type keyへ設定する。
6. propertyをsource列へ対応付け、display nameを設定する。
7. **Instances**で起点IDが表示されることを確認する。

## 3. relationshipを構成

1. `relationships`から1つ選ぶ。
2. 一意なrelationship名、origin、targetを作成する。
3. mapping tableを選び、origin keyとtarget keyに対応するMatched列を設定する。
4. 保存後、残りのrelationshipも同様に構成する。
5. 関連するGraph modelをrefreshする。
6. 起点IDを開き、期待するtargetへのedgeを確認する。

業界別のmapping tableとMatched列は[デモデータ投入runbook](../../evaluation/Demo-Data-Deployment-Runbook.md#32-relationship-binding)を参照します。

## 4. 証跡

- entity type一覧
- 起点IDを表示したInstances画面
- 起点IDから1-hopのrelationshipを表示したGraph画面
- Graph refreshの実行日時

## 成功条件

- [ ] 全CSVがmanaged tableになっている。
- [ ] 全entity typeにkeyとstatic bindingがある。
- [ ] 起点IDがInstancesに表示される。
- [ ] 少なくとも1つのrelationship edgeを既知ID間で確認した。

Instancesが0件、またはedgeがない場合は[トラブルシューティング](../../troubleshooting/README.md#fabric-iq)で解消してから進みます。

[前へ: ローカル準備](01-local-setup.md){ .md-button }
[次へ: Foundry IQ](03-foundry-iq.md){ .md-button .md-button--primary }
