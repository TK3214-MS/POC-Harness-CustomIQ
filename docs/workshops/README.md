# Workshop Guide

Industry IQ Platform Accelerator を紹介するワークショップの構成案です。想定するセッションは3種類（Executive Session / Technical Session / Half-Day Workshop）で、いずれも **Local Preview Mode（合成データ・ローカル実行）でのデモ** を前提としています。Microsoft 製品（Copilot Studio、Foundry、Fabric 等）との実接続を体験するワークショップではありません。

各セッションの時間配分はあくまで発表運営上の目安であり、Microsoft 製品の仕様・提供状況とは無関係です。

---

## セッション共通の事前準備

いずれのセッションも、進行役は事前に以下を実施してください。

1. [docs/self-guided-demo/Prerequisites.md](../self-guided-demo/Prerequisites.md) と [docs/self-guided-demo/Environment-Checklist.md](../self-guided-demo/Environment-Checklist.md) に従って手元の環境を準備する
2. `./scripts/demo/run-demo-cli.sh health` を一度実行し、Local Preview Mode で正常に動作することを確認する
3. 対象セッションのプレゼンテーション資料（下記参照）に目を通す

---

## 1. Executive Session（60〜90分）

**対象**: 経営層・事業責任者・意思決定者
**目的**: コンセプトと現状（証明済みのこと／未検証のこと）を正しく理解してもらう

| 時間 | 内容 |
|---|---|
| 0〜30分 | [docs/presentations/Executive-Presentation.md](../presentations/Executive-Presentation.md) によるプレゼンテーション |
| 30〜55分 | Industry Pack 1つを選んでのライブデモ（[docs/self-guided-demo/30-Minute-Demo-Guide.md](../self-guided-demo/30-Minute-Demo-Guide.md) の一部を抜粋。[docs/presentations/Demo-Storyline.md](../presentations/Demo-Storyline.md) の台本に沿って実演） |
| 55〜90分 | Q&A（進行役は [docs/presentations/Speaker-Notes.md](../presentations/Speaker-Notes.md) の「Executive Presentation 発表者ノート」を参照して回答） |

**進行役へのポイント**:
- 「証明済みのこと／未検証のこと」のスライドは絶対に省略しない
- Microsoft 製品との連携について聞かれた場合は、必ず「構想・検討段階であり、現時点で実接続はしていない」と明言する

---

## 2. Technical Session（2〜3時間）

**対象**: アーキテクト・開発者・インフラ担当者
**目的**: 設計思想・実装の詳細・拡張方法を理解してもらう

| 時間 | 内容 |
|---|---|
| 0〜45分 | [docs/presentations/Technical-Presentation.md](../presentations/Technical-Presentation.md) によるプレゼンテーション |
| 45〜90分 | ハンズオン: 参加者自身の端末で [docs/self-guided-demo/30-Minute-Demo-Guide.md](../self-guided-demo/30-Minute-Demo-Guide.md) を実施し、複数業界（例: 製造 → 金融サービス → 小売）を切り替えながら実行する |
| 90〜135分 | コードウォークスルー: `iq_platform/contracts/` 配下の契約定義（Adapter・Manifest・Agent Response・MCP Tool）と、1つの Industry Pack（例: `industry-packs/manufacturing/`）のファイル構成を実際のコードを見ながら説明する |
| 135〜165分 | テストスイートウォークスルー: `pytest tests/ -v` を実行し、`tests/contract/` `tests/unit/` `tests/integration/` `tests/end-to-end/` `tests/evaluation/` `tests/security/` の各カテゴリが何を保証しているかを説明する |
| 165〜180分 | Q&A（進行役は [docs/presentations/Speaker-Notes.md](../presentations/Speaker-Notes.md) の「Technical Presentation 発表者ノート」を参照） |

**進行役へのポイント**:
- コードウォークスルーでは、業界固有のロジックが共通コード（`iq_platform/` 配下）に一切含まれていないことを実際にファイルを開いて示す
- テストが保証する範囲（契約準拠・ロジックの正しさ）と保証しない範囲（実環境での性能・セキュリティ・可用性）を明確に区別して説明する

---

## 3. Half-Day Workshop（4時間以上）

**対象**: Executive Session と Technical Session の両方に関心がある混成グループ、または実際に Industry Pack を拡張してみたい開発チーム
**目的**: コンセプト理解 + ハンズオン体験 + 実際の拡張作業の疑似体験

| 時間 | 内容 |
|---|---|
| 0〜60分 | Executive Session の内容を圧縮して実施（[docs/presentations/Executive-Presentation.md](../presentations/Executive-Presentation.md) + ライブデモ） |
| 60〜180分 | Technical Session の内容を圧縮して実施（[docs/presentations/Technical-Presentation.md](../presentations/Technical-Presentation.md) + 複数業界のハンズオン + コード/テストウォークスルー） |
| 180〜240分以降 | **ハンズオン演習**: 既存の Industry Pack に小さな拡張（例: 新しい MCP ツールを1つ追加する）を参加者自身で行う。手順は [docs/industry-packs/Industry-Pack-Guide.md](../industry-packs/Industry-Pack-Guide.md) を参照 |
| 演習後 | 成果物を互いに共有し、進行役が講評。最後に「証明済みのこと／未検証のこと」を改めて振り返り、次のステップ（検証環境での接続検証など）を確認して終了 |

**ハンズオン演習の進め方の例**:
1. 参加者を少人数のグループに分ける
2. 各グループに、既存の Industry Pack（例: `industry-packs/retail/`）から1つ選んでもらう
3. [docs/industry-packs/Industry-Pack-Guide.md](../industry-packs/Industry-Pack-Guide.md) の手順に従い、その業界向けに新しい MCP ツールを1つ追加してもらう
4. `pytest tests/ -v` を実行し、既存のテストが引き続き成功すること、プラットフォーム側の共通コードを変更していないことを確認する
5. `./scripts/demo/run-demo-cli.sh run-demo` で追加したツールが動作することを確認する

**進行役へのポイント**:
- 演習はあくまで「Industry Pack の拡張がプラットフォームコードに影響しないこと」を体感してもらうためのものであり、本番品質のツール実装を求めるものではない
- 演習中に Microsoft 製品への実接続を試みないよう案内する（Local Preview Mode の範囲内で完結させる）

---

## 全セッション共通の留意事項

- いずれのセッションも Local Preview Mode（合成データ・ローカル実行）のデモであることを、セッション開始時に必ず明示する
- Microsoft 製品の価格・ライセンス・GA/Preview状態・リージョン提供状況について質問された場合は、推測で回答せず「Microsoft の最新の公式情報を確認してほしい」と案内する
- 各セッションの資料本文には内部専用のファイルパスや ADR 番号を含めていない設計だが、コードウォークスルーやハンズオン演習では実際のリポジトリ構成を直接参照するため、社外向けにセッションを実施する場合は事前にリポジトリの公開範囲を確認すること
