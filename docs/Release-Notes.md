# リリースノート

> **これは pre-1.0 のリポジトリです。** バージョンタグや GitHub Release はまだ一つも作成されていません。以下は Phase 0 から Phase 6 までの単一継続ビルドにおける、実装内容の時系列サマリーです。存在しないバージョン履歴を作り出さないよう、意図的にこの形式で記録しています。

## Phase 0 — 前提整理

- ステークホルダーからの指示書を分解し、[docs/decisions/assumptions.md](decisions/assumptions.md)（採用した前提）と [docs/decisions/open-questions.md](decisions/open-questions.md)（未解決事項、後にすべて解決済みへ更新）を作成。
- Microsoft 製品仕様の検証状況を追跡する [docs/decisions/product-verification.md](decisions/product-verification.md) と、Capability Registry の初期版（`config/capabilities.yaml`）を作成。

## Phase 1 — リポジトリ骨格と契約

- リポジトリ構造、Pydantic ベースの契約群（Adapter、Industry Pack Manifest、MCP Tool Response、Agent Response、Capability）を実装。
- ADR-0001〜0007 を含む主要な設計判断を記録し、Contract テストを追加。
- 実装言語を Python 3.11+ に統一（[ADR-0002](decisions/0002-python-primary-language.md)）。

## Phase 2 — Manufacturing 垂直スライス

- Manufacturing 業界向けに、Mock/Simulated Adapter、MCP Backend（FastAPI）、Local Orchestrator、Demo CLI の最初の垂直スライスを実装。
- Local Preview Mode でエンドツーエンドのデモシナリオが動作することを確認。

## Phase 3 — 残り4業界とオーケストレーターの汎化

- Financial Services / Retail / Healthcare / Public Sector の Industry Pack を追加し、5業界すべてが同一スキーマで実装される状態に。
- Manufacturing 固有ロジックが `iq_platform/` 側に直接書かれていた問題を是正し、Industry Pack 固有のロジックを各パック内のプラグインモジュールへ移動（[ADR-0011](decisions/0011-generic-orchestrator-and-semantic-adapter.md)）。
- Industry Pack 切り替え時の状態非漏洩を確認する end-to-end テストを追加。

## Phase 4 — Live Adapter スキャフォールド

- Work IQ / Foundry IQ / Fabric IQ の Live Adapter を「verification_required スキャフォールド」として実装（[ADR-0013](decisions/0013-live-adapter-verification-required-scaffold.md)）。`mode` は `unavailable` と `verification_required` のみを取り、`live` には到達しない設計。
- `azure-identity` の `ClientSecretCredential` による実際の Microsoft Entra ID 認証を実装（この部分のみ検証済みパターン）。
- [docs/setup/live-adapters-configuration.md](setup/live-adapters-configuration.md) を作成（Entra ID アプリ登録手順は実施可能、製品固有部分は TBD）。

## Phase 5 — デプロイ基盤

- MCP Backend を Azure Container Apps にデプロイするための azd/Bicep/コンテナ構成を実装（[ADR-0012](decisions/0012-mcp-backend-deployment-target.md)）。
- ACR admin ユーザー無効化 + User-Assigned Managed Identity + AcrPull の最小権限構成。Bicep は `az bicep build` でのコンパイル検証済み。
- 実 Azure サブスクリプションに対する `azd up` の実行は未実施のまま。

## Phase 6 — セルフガイドデモ、評価エンジン、ギャップ充足

- 30分セルフガイドデモ一式（[docs/self-guided-demo/](self-guided-demo/)）を作成。
- 評価エンジン（`iq_platform/evaluation/rubric_evaluator.py`、`demo-cli evaluate`）と完了サマリー生成（`demo-cli generate-summary`）を実装。
- 合成データ検証スクリプト（`scripts/validation/validate_synthetic_data.py`）を追加し CI に組み込み。
- Demo CLI の残り2コマンド（`setup` / `cleanup`）を実装し、全10コマンドが揃った状態に。
- 統合・セキュリティ・単体テストを72件追加(64件→136件)し、MCP Tool 許可リスト機能(`MCP_BACKEND_ALLOWED_TOOLS`)を追加。ドキュメント間リンク検証テストを追加(136件→137件)。

## 今後の見通し

上記のうち、実 Microsoft 製品 API 統合・実 Azure デプロイの検証・Terraform 実装・Web UI などは、いずれも次フェーズ以降の未着手項目です。網羅的な一覧は [docs/Known-Limitations.md](Known-Limitations.md) を参照してください。
