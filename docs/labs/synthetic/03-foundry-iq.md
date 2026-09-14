# Lab 3: Foundry IQ

想定時間: 40分

選択したIndustry Packの手順・ポリシー文書を登録し、文書名と引用を含む回答が得られる状態にします。

## 1. sourceを確認

`industry-packs/<pack>/knowledge/*.md`を確認します。このラボではMarkdown文書を推奨sourceとします。`sample-data/foundry/demo/knowledge.jsonl`は一括取込を検討する場合の補助artifactです。

## 2. Knowledge Sourceを構成

1. ラボ用のAzure AI SearchおよびFoundry環境を開く。
2. 選択したpackのMarkdown文書だけを承認済みstorageへ配置する。
3. Knowledge Source、indexer、indexを構成する。
4. indexerを実行し、失敗件数が0であることを確認する。
5. title、content、source filenameを検索結果から確認できるようにする。

## 3. Knowledge Baseを検証

1. Knowledge BaseへKnowledge Sourceを追加する。
2. 「このKnowledge Baseで参照できる手順文書名を一覧表示してください」と質問する。
3. 選択したpackの文書名が返ることを確認する。
4. 選択した業界の`K-01`を[テスト質問集](../../evaluation/Copilot-Studio-IQ-Layer-Test-Catalog.md)から実行する。
5. 回答に文書名と該当箇所の引用があることを確認する。

## 証跡

- indexerの最終成功日時と取込件数
- Knowledge Baseへ登録したsource名
- `K-01`の回答と引用

## 成功条件

- [ ] 選択したpackの文書だけが取込対象である。
- [ ] indexerが成功している。
- [ ] 文書名を指定しない質問でも関連文書を取得できる。
- [ ] 回答に引用が含まれ、sourceにない手順を生成していない。

[前へ: Fabric IQ](02-fabric-iq.md){ .md-button }
[次へ: Work IQ](04-work-iq.md){ .md-button .md-button--primary }
