# docs/presentations/

顧客向け・社内向けのプレゼンテーション素材一式です。**PowerPoint の自動生成機能は現時点で用意していない**ため、まず Markdown 形式でスライド構成・発表内容を確定させ、その後 [Architecture-Diagrams.md](Architecture-Diagrams.md) 末尾に記載の変換方法（Mermaid 図の画像化）に従って手動でスライド化する運用です。

## 含まれるファイル

| ファイル | 内容 | 想定オーディエンス |
|---|---|---|
| [Architecture-Diagrams.md](Architecture-Diagrams.md) | アーキテクチャ図一式（Mermaid、7図）と画像化手順。他の資料のソース素材 | 全員 |
| [Executive-Presentation.md](Executive-Presentation.md) | 経営層・意思決定者向けスライド構成案（全12スライド） | 経営層・事業責任者 |
| [Technical-Presentation.md](Technical-Presentation.md) | 技術担当者向けスライド構成案（全15スライド） | アーキテクト・開発者・インフラ担当者 |
| [Speaker-Notes.md](Speaker-Notes.md) | 上記2資料のスライド番号に対応した発表者ノート（想定質問・避けるべき表現を含む） | 発表者 |
| [Demo-Storyline.md](Demo-Storyline.md) | 30分セルフガイドデモをライブで実演する際の発表台本 | 発表者 |

## 使い方の流れ

1. 対象オーディエンスに応じて [Executive-Presentation.md](Executive-Presentation.md) または [Technical-Presentation.md](Technical-Presentation.md) を選ぶ（両方使う場合は Executive → Technical の順）
2. 発表前に [Speaker-Notes.md](Speaker-Notes.md) の該当セクションを読み、想定質問への回答を準備する
3. ライブデモを含む場合は [Demo-Storyline.md](Demo-Storyline.md) の台本に沿って [docs/self-guided-demo/30-Minute-Demo-Guide.md](../self-guided-demo/30-Minute-Demo-Guide.md) を実演する
4. 画像が必要な場合は [Architecture-Diagrams.md](Architecture-Diagrams.md) の図を画像化してスライドに貼り付ける

## 重要な注意事項

- これらの資料はすべて **Local Preview Mode（合成データ・ローカル実行）** の内容のみを実装済みとして扱っています。Microsoft 製品（Copilot Studio、Foundry、Fabric 等）との連携は構想・検討段階として明示的に区別しており、実装済みであるかのように書かれた記述はありません。
- 各資料の本文には、内部専用のファイルパスや ADR 番号を含めていません。それらは各資料末尾の「内部参考（社内限定・顧客には見せない）」セクションにのみ記載しています。顧客向けにこれらの資料を共有する際は、必ずそのセクションを削除してください。
- 資料の内容と実装状況に食い違いがある場合は、[README.md](../../README.md) の実装状況チェックリストと [docs/architecture/architecture-guide.md](../architecture/architecture-guide.md) を正としてください。
