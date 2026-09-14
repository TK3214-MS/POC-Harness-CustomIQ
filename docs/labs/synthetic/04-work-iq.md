# Lab 4: Work IQ

想定時間: 30分

選択したIndustry Packの合成コンテンツをMicrosoft 365へ配置し、テストユーザーの既存権限で取得できる状態にします。

## 1. 配置先を準備

ラボ専用のSharePoint site、Teams team/channel、Exchange test mailboxとcalendarを使用します。本番利用者の既存コンテンツへ混在させません。

## 2. 合成コンテンツを配置

`industry-packs/<pack>/sample-data/work-iq/*.md`を開き、文書の用途に応じて配置します。

| 内容 | 配置先の例 |
| --- | --- |
| ケース・レビュー資料 | SharePoint document library |
| `teams-thread` | Teams channelへの合成投稿 |
| `email` | test mailbox間の合成メール |
| `meeting` | test calendarの会議説明または議事録 |

Markdownファイル自体を置くだけでなく、メールや会議として検証する内容は対応するMicrosoft 365 workloadへ作成します。各記録に`*-SYN-*` IDを残します。

## 3. 権限を確認

1. Copilot Studioで使用するtest userとしてMicrosoft 365へサインインする。
2. 配置したSharePoint文書、Teams投稿、メール、会議を通常の画面から開けることを確認する。
3. test userに許可していない別のラボ領域を開けないことを確認する。

## 証跡

- 配置先と合成record IDの対応表
- test userでの閲覧成功
- 未許可領域を取得できないことの確認結果

## 成功条件

- [ ] SharePoint、Teams、Exchange、calendarの必要な合成コンテンツを配置した。
- [ ] 起点となる`*-SYN-*` IDが各記録に含まれる。
- [ ] test userが対象記録だけを閲覧できる。

Work IQの提供条件、課金、policy、書き込み可否は実施日時点の公式文書とtenant設定を確認します。

[前へ: Foundry IQ](03-foundry-iq.md){ .md-button }
[次へ: Copilot Studio](05-copilot-studio.md){ .md-button .md-button--primary }
