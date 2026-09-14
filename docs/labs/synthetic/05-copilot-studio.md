# Lab 5: Copilot Studio

想定時間: 50分

各IQを個別に接続・検証してから、複合質問を実行します。

## 1. エージェントを準備

1. Copilot Studioでラボ用エージェントを作成する。
2. `industry-packs/<pack>/agents/investigation_agent_instructions.md`の内容をエージェント指示へ設定する。
3. 指示内の情報源分離、0件、Tool失敗、人手承認のルールを確認する。

## 2. Toolを個別接続

次の順で1つずつ追加し、接続同意と識別情報を確認します。

1. Fabric IQ Ontology MCP
2. Foundry IQ Knowledge Base
3. Work IQ

Toolの表示名だけで接続先を判断せず、workspace、Ontology、Knowledge Base、connection userを証跡へ記録します。

## 3. 単一レイヤーテスト

[IQレイヤー別テスト質問集](../../evaluation/Copilot-Studio-IQ-Layer-Test-Catalog.md)から、選択した業界の次を実行します。

1. `F-01`: schema discovery
2. `F-02`: 起点IDのentity検索
3. `K-01`: 手順検索と引用
4. `W-01`: M365横断検索

各質問後にActivity traceを開き、期待したTool、入力、結果、エラーを記録します。

## 4. 複合テスト

単一レイヤーがすべて成功した後、同じ業界の`X-01`と`X-02`を実行します。

- Fabricの事実、Foundryの規程、Work IQの担当者コンテキストが分離されている。
- 取得できない情報やsource間の差異を隠していない。
- 自動承認、凍結、発注、診断、行政判断などの禁止操作を実行していない。

## 成功条件

- [ ] 3つのIQを個別に呼び出せる。
- [ ] Activity traceのTool選択が質問意図と一致する。
- [ ] 複合回答でsource種別と引用が分離される。
- [ ] 0件、権限不足、Tool失敗を成功回答として扱わない。
- [ ] 高影響判断に人手承認を示す。

失敗を残した場合は[トラブルシューティング](../../troubleshooting/README.md)へ進み、解消後に同じ単一レイヤーテストから再開します。

[前へ: Work IQ](04-work-iq.md){ .md-button }
[次へ: 完了確認](06-complete.md){ .md-button .md-button--primary }
