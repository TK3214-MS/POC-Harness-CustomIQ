# Lab 4: Work IQ

想定時間: 30分

選択したIndustry Packの合成コンテンツをMicrosoft 365へ配置し、テストユーザーの既存権限で取得できる状態にします。

## 1. 配置先を準備

ラボ専用のSharePoint site、Teams team/channel、Exchange test mailboxとcalendarを使用します。本番利用者の既存コンテンツへ混在させません。

Work IQを使用する前に、管理者が実施日時点の公式手順でtenant有効化、使用量ベース課金、spending policy、MCP policyを確認します。初期検証は読み取り専用とし、作成・更新・送信操作を許可しません。

## 2. 合成コンテンツを配置

[`industry-packs/<pack>/sample-data/work-iq/*.md`](https://github.com/TK3214-MS/POC-Harness-CustomIQ/tree/main/industry-packs){ target="_blank" rel="noopener" }を開き、文書の用途に応じて配置します。

| 内容 | 配置先の例 |
| --- | --- |
| ケース・レビュー資料 | SharePoint document library |
| `teams-thread` | Teams channelへの合成投稿 |
| `email` | test mailbox間の合成メール |
| `meeting` | test calendarの会議説明または議事録 |

Markdownファイル自体を置くだけでなく、メールや会議として検証する内容は対応するMicrosoft 365 workloadへ作成します。各記録に`*-SYN-*` IDを残します。

1. SharePoint document libraryへケース・レビュー資料を保存します。
2. `teams-thread`の内容をラボ専用Teams channelへ投稿します。
3. `email`の内容をtest mailbox間で送信します。
4. `meeting`の内容をtest calendarの会議本文または議事録へ登録します。
5. Fabric Labで確認した起点IDと同じ`*-SYN-*` IDが、各コンテンツの件名または本文にあることを確認します。

<figure class="lab-image-placeholder" markdown>
    **画像差し替え位置: Microsoft 365合成コンテンツ**
    `assets/images/labs/work-iq-synthetic-content.png`
    <figcaption>TeamsまたはSharePointで合成IDが見える画面へ差し替えます。個人情報は含めません。</figcaption>
</figure>

## 3. 権限を確認

1. Copilot Studioで使用するtest userとしてMicrosoft 365へサインインします。
2. 配置したSharePoint文書、Teams投稿、メール、会議を通常の画面から開けることを確認します。
3. test userに許可していない別のラボ領域を開けないことを確認します。

Work IQへ別の検索indexとしてファイルをアップロードする手順ではありません。成功条件は、Copilot Studioの接続ユーザーが既存Microsoft 365権限の範囲で対象コンテンツを取得できることです。

<figure class="lab-image-placeholder" markdown>
    **画像差し替え位置: Test userのアクセス確認**
    `assets/images/labs/work-iq-permission-check.png`
    <figcaption>許可された対象を開けることを示す画面へ差し替えます。</figcaption>
</figure>

## 成功条件

- [ ] SharePoint、Teams、Exchange、calendarの必要な合成コンテンツを配置しました。
- [ ] 起点となる`*-SYN-*` IDが各記録に含まれています。
- [ ] test userが対象記録だけを閲覧できます。

Work IQの提供条件、課金、policy、書き込み可否は実施日時点の公式文書とtenant設定を確認します。

[前へ: Foundry IQ](03-foundry-iq.md){ .md-button }
[次へ: Copilot Studio](05-copilot-studio.md){ .md-button .md-button--primary }
