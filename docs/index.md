---
hide:
    - navigation
    - toc
---

<section class="lab-hero" markdown>
<div markdown>

# Industry IQ Platform Labs

合成データから業界知識を組み立て、Microsoft Fabric IQ、Foundry IQ、Work IQをCopilot Studioへ接続するハンズオンラボです。

<div class="lab-hero__actions" markdown>
[ラボを開始する](labs/index.md){ .md-button .md-button--primary }
[開始前チェック](labs/prerequisites.md){ .md-button }
</div>

</div>
</section>

<div class="lab-grid" markdown>
<div class="lab-card" markdown>
:material-database-outline:
**Fabric IQ**
<small>Lakehouseの合成データをOntologyのentityとrelationshipへbindingします。</small>
</div>
<div class="lab-card" markdown>
:material-bookshelf:
**Foundry IQ**
<small>業界文書をKnowledge Sourceへ取り込み、引用付き回答を検証します。</small>
</div>
<div class="lab-card" markdown>
:material-account-search-outline:
**Work IQ**
<small>合成Microsoft 365コンテンツから業務コンテキストを確認します。</small>
</div>
</div>

## ラボ構成

| 内容 | 対象 | 所要時間 | ゴール |
| --- | --- | ---: | --- |
| メインラボ | ソリューションアーキテクト、Copilot Studio作成者 | 3〜4時間 | 5業界から1つを選び、合成データで3つのIQレイヤーを接続して検証する |
| Custom MCP Backend | 上級者、連携実装担当者 | 任意 | 合成データを公開するMCP BackendをAzure Container Appsで検証する |

!!! warning "開始前に確認"
    このラボは受講者ごとの既存tenantと、リポジトリに格納済みの合成データだけを使用します。実顧客データは使用しません。必要なライセンス、Preview提供状況、tenant設定、capacity、ロールが確認できない場合は、構築を開始せず管理者へ確認してください。

## 既存リファレンス

- [本番環境構築ガイド](Production-Environment-Setup.md)
- [実顧客データ向けOntology設計・構築ガイド](Customer-Data-Ontology-Design-Guide.md)
- [サンプルデータ再生成ガイド](reference/Sample-Data-Regeneration-Guide.md)
- [IQデモデータ投入・再構成ランブック](evaluation/Demo-Data-Deployment-Runbook.md)
- [Copilot Studio IQレイヤー別テスト質問集](evaluation/Copilot-Studio-IQ-Layer-Test-Catalog.md)
- [トラブルシューティング](troubleshooting/README.md)

ラボ本編はこれらの文書を置き換えるものではない。画面操作と合格条件を短い単位に分け、必要な詳細だけをリファレンスへ案内する。
