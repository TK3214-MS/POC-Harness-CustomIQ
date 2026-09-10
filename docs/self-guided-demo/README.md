# 30分セルフガイドデモ

Industry IQ Platform Accelerator を、Azure/Microsoft SaaS 環境なしで（Local Preview Mode）30分で一巡できる自己学習用ガイド一式です。

## まずこれを読む順序

1. [Prerequisites.md](Prerequisites.md) — 何が必要か
2. [Environment-Checklist.md](Environment-Checklist.md) — 開始前チェックリスト
3. [30-Minute-Demo-Guide.md](30-Minute-Demo-Guide.md) — 本編（タイムライン付き）
4. 困ったら [Troubleshooting.md](Troubleshooting.md)
5. 終わったら [Reset-and-Cleanup.md](Reset-and-Cleanup.md)

## このガイド一式に含まれるもの

| ファイル | 内容 |
|---|---|
| [Prerequisites.md](Prerequisites.md) | 必要なソフトウェア・知識レベル |
| [Environment-Checklist.md](Environment-Checklist.md) | 開始前の健全性確認手順 |
| [30-Minute-Demo-Guide.md](30-Minute-Demo-Guide.md) | 本編タイムライン（0〜30分） |
| [Industry-Pack-Selection.md](Industry-Pack-Selection.md) | 5業界の選び方・切り替え方 |
| [Copilot-Studio-Setup.md](Copilot-Studio-Setup.md) | Copilot Studio 接続（Hybrid/Full SaaS 用、Local Preview では不要） |
| [Foundry-IQ-Setup.md](Foundry-IQ-Setup.md) | Foundry IQ 接続（同上） |
| [Fabric-IQ-Setup.md](Fabric-IQ-Setup.md) | Fabric IQ 接続（同上） |
| [Work-IQ-Demo-Preparation.md](Work-IQ-Demo-Preparation.md) | Work IQ 接続（同上） |
| [MCP-Backend-Setup.md](MCP-Backend-Setup.md) | MCP Backend の起動方法（ローカル/コンテナ） |
| [Demo-Prompts.md](Demo-Prompts.md) | 各業界の実行コマンドとデモプロンプト一覧 |
| [Expected-Results.md](Expected-Results.md) | 実行結果として何が表示されるべきか |
| [Troubleshooting.md](Troubleshooting.md) | よくあるエラーと対処 |
| [Reset-and-Cleanup.md](Reset-and-Cleanup.md) | リセット・後片付け手順 |
| [Presenter-Notes.md](Presenter-Notes.md) | 発表者向けメモ（想定質問等） |
| [Architecture-Explained.md](Architecture-Explained.md) | デモ中に説明するアーキテクチャの要点 |
| [Demo-Completion-Summary.md](Demo-Completion-Summary.md) | 完了サマリーの読み方・生成方法 |

## 重要な注意

このデモは既定で **Local Preview Mode** です。Local Preview Mode uses synthetic data and local adapters. It does not validate the availability, behavior, security, licensing, or performance of Microsoft SaaS services.

Hybrid Mode / Full SaaS Mode を試す場合は、[Copilot-Studio-Setup.md](Copilot-Studio-Setup.md) 等を参照してください（Phase 4 時点では Microsoft 製品固有の手順は `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION` のプレースホルダーです。[docs/decisions/product-verification.md](../decisions/product-verification.md) を参照）。

## 設計上の所要時間について

このガイドは **設計上30分** で完了できるよう構成されています。CLI コマンド自体の実行時間は数秒程度です（2026-09-10 に実測: `health`→`validate`→`select-industry`→`load-data`→`run-demo`→`evaluate`→`generate-summary` の一連のコマンドで約2秒）。ただし、人間の発表者が各セクションを読みながら説明する実際のプレゼンテーション時間は未実測です。実測した場合は [Demo-Completion-Summary.md](Demo-Completion-Summary.md) の記録形式に従って記録してください。

