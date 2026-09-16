# Lab 5: Copilot Studio

想定時間: 50分

各IQを個別に接続・検証してから、複合質問を実行します。

## 1. エージェントを準備

1. Copilot Studioでラボ用エージェントを作成する。
2. [`industry-packs/<pack>/agents/investigation_agent_instructions.md`](https://github.com/TK3214-MS/POC-Harness-CustomIQ/tree/main/industry-packs){ target="_blank" rel="noopener" }の内容をエージェント指示へ設定する。
3. 指示内の情報源分離、0件、Tool失敗、人手承認のルールを確認する。
4. エージェント名、environment、接続ユーザー、選択業界を記録する。

<figure class="lab-image-placeholder" markdown>
	**画像差し替え位置: Agent Instructions**
	`assets/images/labs/copilot-studio-instructions.png`
	<figcaption>選択業界の指示が設定された画面へ差し替えます。</figcaption>
</figure>

## 2. Toolを個別接続

次の順で1つずつ追加し、追加直後に単一Toolテストを行います。

1. **Tools > Add Tool > Fabric IQ MCP (Preview)**で新規connectionを作り、Fabric workspace IDとOntology item IDを入力して**Create > Add**を選択する。
2. **Tools > Add Tool > Foundry IQ**で認証方式を選び、Lab 3で作成したKnowledge Baseを選択して**Add to agent**を選択する。
3. **Tools > Add Tool > Model Context Protocol > Work IQ (preview)**でtest userのconnectionを作成し、**Add and Configure**を選択する。

Toolの表示名だけで接続先を判断せず、workspace、Ontology、Knowledge Base、connection userが想定どおりであることを確認します。

!!! warning "Work IQ接続画面"
		Work IQの接続経路、表示名、提供条件は変更される可能性があります。上記選択肢が表示されない場合は推測で汎用Remote MCP URLを入力せず、実施日時点の[公式手順](https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-work-iq)とtenant policyを確認します。

<figure class="lab-image-placeholder" markdown>
	**画像差し替え位置: 3つのIQ Tool一覧**
	`assets/images/labs/copilot-studio-tools.png`
	<figcaption>Fabric IQ、Foundry IQ、Work IQと各connectionが見える画面へ差し替えます。</figcaption>
</figure>

## 3. 単一レイヤーテスト

[IQレイヤー別テスト質問集](../../evaluation/Copilot-Studio-IQ-Layer-Test-Catalog.md)から、選択した業界の次を実行します。

1. `F-01`: schema discovery
2. `F-02`: 起点IDのentity検索
3. `K-01`: 手順検索と引用
4. `W-01`: M365横断検索

各質問後にActivity traceを開き、期待したTool、入力、結果、エラーを確認します。

| 質問 | 期待Tool | 最低限の確認 |
| --- | --- | --- |
| `F-01` / `F-02` | Fabric IQ | entity typeと既知IDが一致 |
| `K-01` | Foundry IQ | 文書名と引用がある |
| `W-01` | Work IQ | test userが閲覧可能なM365情報だけを返す |

<figure class="lab-image-placeholder" markdown>
	**画像差し替え位置: Activity trace**
	`assets/images/labs/copilot-studio-activity-trace.png`
	<figcaption>選択Tool、入力、出力、エラー状態が確認できる画面へ差し替えます。</figcaption>
</figure>

## 4. 複合テスト

単一レイヤーがすべて成功した後、同じ業界の`X-01`と`X-02`を実行します。

- Fabricの事実、Foundryの規程、Work IQの担当者コンテキストが分離されている。
- 取得できない情報やsource間の差異を隠していない。
- 自動承認、凍結、発注、診断、行政判断などの禁止操作を実行していない。

実行結果は質問ID、実行日時、接続ユーザー、回答、引用、Activity trace、`Pass`/`Partial`/`Fail`、残課題を同じ記録へ保存します。

## 成功条件

- [ ] 3つのIQを個別に呼び出せる。
- [ ] Activity traceのTool選択が質問意図と一致する。
- [ ] 複合回答でsource種別と引用が分離される。
- [ ] 0件、権限不足、Tool失敗を成功回答として扱わない。
- [ ] 高影響判断に人手承認を示す。

失敗を残した場合は[トラブルシューティング](../../troubleshooting/README.md)へ進み、解消後に同じ単一レイヤーテストから再開します。

[前へ: Work IQ](04-work-iq.md){ .md-button }
[次へ: 完了確認](06-complete.md){ .md-button .md-button--primary }
