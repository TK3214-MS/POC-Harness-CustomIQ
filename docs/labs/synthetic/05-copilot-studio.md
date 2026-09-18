# Lab 5: Copilot Studioエージェントを構成

想定時間: 30分

各IQをエージェントへ個別に接続し、テストを開始できる状態まで構成します。このページでは評価質問を実行しません。

## 1. エージェントを準備

1. Copilot Studioでラボ用エージェントを作成します。
2. [`industry-packs/<pack>/agents/investigation_agent_instructions.md`](https://github.com/TK3214-MS/POC-Harness-CustomIQ/tree/main/industry-packs){ target="_blank" rel="noopener" }の内容をエージェント指示へ設定します。
3. 指示内の情報源分離、0件、Tool失敗、人手承認のルールを確認します。
4. エージェント名、environment、接続ユーザー、選択業界を記録します。

<figure class="lab-image-placeholder" markdown>
    **画像差し替え位置: Agent Instructions**
    `assets/images/labs/copilot-studio-instructions.png`
    <figcaption>選択業界の指示が設定された画面へ差し替えます。</figcaption>
</figure>

## 2. Toolを個別接続

次の順で1つずつ追加します。

1. **Tools > Add Tool > Fabric IQ MCP (Preview)**で新規connectionを作り、Fabric workspace IDとOntology item IDを入力して**Create > Add**を選択します。
2. **Tools > Add Tool > Foundry IQ**で認証方式を選び、Lab 3で作成したKnowledge Baseを選択して**Add to agent**を選択します。
3. **Tools > Add Tool > Model Context Protocol > Work IQ (preview)**でtest userのconnectionを作成し、**Add and Configure**を選択します。

Toolの表示名だけで接続先を判断せず、workspace、Ontology、Knowledge Base、connection userが想定どおりであることを確認します。

!!! warning "Work IQ接続画面"
    Work IQの接続経路、表示名、提供条件は変更される可能性があります。上記選択肢が表示されない場合は推測で汎用Remote MCP URLを入力せず、実施日時点の[公式手順](https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-work-iq)とtenant policyを確認します。

<figure class="lab-image-placeholder" markdown>
    **画像差し替え位置: 3つのIQ Tool一覧**
    `assets/images/labs/copilot-studio-tools.png`
    <figcaption>Fabric IQ、Foundry IQ、Work IQと各connectionが見える画面へ差し替えます。</figcaption>
</figure>

## 3. テスト前の構成確認

1. 3つのToolを開き、接続先と認証ユーザーを記録します。
2. エージェントの指示を保存し、未公開の開発版としてversionを記録します。
3. Tool名、説明、接続先に別業界の値が混在していないことを確認します。
4. 構成を変更せずに[エージェントテスト](06-agent-test.md)へ進みます。

## 成功条件

- [ ] 3つのIQ Toolがエージェントへ追加されています。
- [ ] Fabric workspace、Ontology、Knowledge Base、connection userが記録値と一致しています。
- [ ] 選択業界のエージェント指示が保存されています。
- [ ] テスト開始前のagent versionを記録しています。

接続または保存に失敗した場合は[トラブルシューティング](../../troubleshooting/README.md)で解消してからテストへ進みます。

[前へ: Work IQ](04-work-iq.md){ .md-button }
[次へ: エージェントをテスト](06-agent-test.md){ .md-button .md-button--primary }
