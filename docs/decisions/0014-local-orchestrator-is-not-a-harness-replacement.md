# ADR-0014: `GenericLocalOrchestrator` は GitHub Copilot harness(Copilot Studio)の Local Preview 代替であり、恒久的な設計選択ではない

- ステータス: Accepted
- 日付: 2026-09-10

## コンテキスト

指示書は、エージェント/オーケストレーション層として **GitHub Copilot harness(Microsoft Copilot Studio 上で実行されるハーネス)を採用すること**を前提としている。しかし、この製品自体の存在・名称・API 仕様・MCP Tool 登録方法は [docs/decisions/product-verification.md](product-verification.md) の通り未検証であり、本開発環境には実際の Copilot Studio テナント/環境へのアクセスがない([docs/decisions/open-questions.md](open-questions.md) Q3)。

この制約の下で、Adapter・Industry Pack・MCP Backend・評価エンジンといった他のレイヤーの開発とデモを止めないため、`iq_platform/orchestration/generic_orchestrator.py` に `GenericLocalOrchestrator` を実装した([ADR-0011](0011-generic-orchestrator-and-semantic-adapter.md))。

このレビューの過程で、複数のドキュメント([docs/architecture/architecture-guide.md](../architecture/architecture-guide.md) セクション2.1 が特に該当)がこの関係性を曖昧にしか説明しておらず、「`GenericLocalOrchestrator` が実質的にオーケストレーション層の設計そのものである」かのように読める余地があることが判明した。これは指示書の意図(GitHub Copilot harness の採用)を正しく反映していない表現であり、本 ADR で明確化する。

## 決定

1. **`GenericLocalOrchestrator` は Local Preview Mode 専用の代替実装であり、本番アーキテクチャの一部ではない。** 実際のデプロイでは、Industry Pack が提供する MCP Tool・Agent instructions・Ontology を Copilot Studio 上の GitHub Copilot harness に登録し、ハーネス自身がタスク分解・Tool 選択・結果統合を行うことを前提とする。
2. **`GenericLocalOrchestrator` を将来的に本番のオーケストレーション層として「格上げ」する計画は存在しない。** Copilot Studio が利用可能になった段階で行うべき作業は、`GenericLocalOrchestrator` の機能拡張ではなく、(a) MCP Backend を Copilot Studio から呼び出し可能な形で公開する、(b) 各 Industry Pack の `agent_instructions_path` の内容を Copilot Studio 上のエージェント設定に反映する、(c) Work IQ / Foundry IQ / Fabric IQ の Live Adapter を実 API 接続へ更新する、の3点である。
3. **Copilot Studio harness に専用の `Adapter` クラスは作らない。** これは IQ レイヤーの Adapter ではなくハーネス/オーケストレーターそのものであるため([ADR-0013](0013-live-adapter-verification-required-scaffold.md) 決定5)。設定値の存在確認のみを `demo-cli health` に実装する。
4. **`apps/demo-ui/` のような追加のカスタム UI は、Copilot Studio harness の代替として作らない。** Local Preview Mode の利用者インターフェースは `apps/demo-cli/` の CLI のみとし([docs/decisions/assumptions.md](assumptions.md) A3)、UI 相当の体験は本番では Copilot Studio 側が提供する想定である。`apps/demo-ui/` は現在 README のみのプレースホルダーであり、これを本格実装する計画はない。

## 影響

- [docs/architecture/architecture-guide.md](../architecture/architecture-guide.md) セクション2.1 を本 ADR を参照する形で書き直し、「GitHub Copilot harness が本来の対象であり、`GenericLocalOrchestrator` は Local Preview Mode 専用の代替である」ことを明記する。
- [docs/self-guided-demo/Architecture-Explained.md](../self-guided-demo/Architecture-Explained.md) の対応表(レイヤーごとの「デモでの役割」「本番での役割」)は、この決定と整合しているため変更不要。
- 今後、新しいドキュメントで `GenericLocalOrchestrator` や `apps/demo-cli/` を説明する際は、必ず「Local Preview Mode 専用の代替であり、本番では GitHub Copilot harness(Copilot Studio)が担う」旨を明示すること。
