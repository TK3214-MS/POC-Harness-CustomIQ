# Industry IQ Platform Accelerator

> **状態: 開発中 (Phase 6 まで実装済み)。** Local Preview Mode で5業界すべての E2E デモが実行可能です。Live Adapter は verification_required スキャフォールドのみ（実 Microsoft 製品 API 統合は未実装）。実 Azure デプロイは未検証。

## これは何か

複数業界(Manufacturing / Financial Services / Retail / Healthcare / Public Sector)へ、共通のエージェント基盤・契約(Adapter / Industry Pack / MCP Tool / Agent Response)を変更せずに、Industry Pack の差し替えだけで展開できる Enterprise Intelligence Platform のアクセラレータです。

**エージェント/オーケストレーション層は GitHub Copilot harness(Microsoft Copilot Studio 上で実行されるハーネス)を採用する設計です。** ただし Copilot Studio 自体の製品仕様は[未検証](docs/decisions/product-verification.md)であり本開発環境には実テナントへのアクセスがないため、本リポジトリでは `GenericLocalOrchestrator`(CLI から呼び出す Local Preview Mode 専用の代替)で Adapter・Industry Pack・MCP Backend の開発とデモを進めています。これは本番アーキテクチャの一部ではなく、恒久的な代替でもありません。詳細は [ADR-0014](docs/decisions/0014-local-orchestrator-is-not-a-harness-replacement.md) と [docs/architecture/architecture-guide.md](docs/architecture/architecture-guide.md) セクション2.1を参照してください。同様に、追加のカスタム UI(`apps/demo-ui/`)も作っていません — Local Preview Mode の利用者インターフェースは CLI のみです([docs/decisions/assumptions.md](docs/decisions/assumptions.md) A3)。

詳細な設計方針・非目標・成功条件は元の指示書（本リポジトリのセットアップ時にステークホルダーから提供されたもの）に基づき、以下のドキュメントに分解して記録しています。

- [docs/decisions/assumptions.md](docs/decisions/assumptions.md) — 採用した前提・デフォルト
- [docs/decisions/open-questions.md](docs/decisions/open-questions.md) — 未解決だった論点と回答
- [docs/decisions/product-verification.md](docs/decisions/product-verification.md) — 未検証の Microsoft 製品仕様の一覧（絶対に事実として扱わないこと）
- [docs/architecture/architecture-guide.md](docs/architecture/architecture-guide.md) — レイヤー構成、Adapter パターン、実行モードの説明
- [docs/decisions/](docs/decisions/) — 各 ADR (0001〜)

## 現在の実装状況（Phase 6 まで実装済み、ギャップ充足作業込み）

- [x] Phase 0: 前提・未解決事項・Capability Registry 初期版
- [x] Phase 1: リポジトリ骨格、契約（Pydantic モデル）、Capability Registry ローダー、ADR、Contract テスト
- [x] Phase 2: Manufacturing の Local Preview 垂直スライス(Mock/Simulated Adapter、MCP Backend、Local Orchestrator、Demo CLI、E2E テスト)
- [x] Phase 3: 残り4業界の Industry Pack(Financial Services / Retail / Healthcare / Public Sector)+ Orchestrator の汎化 + Industry Pack 切り替えテスト
- [x] Phase 4: Live Adapter(Copilot Studio / Work IQ / Foundry IQ / Fabric IQ)を verification_required スキャフォールドとして実装(実 Entra ID 認証コードは実装・単体テスト済み、実テナントでの検証は未実施。製品 API 自体は未検証のため `query()` は常に例外を送出)
- [x] Phase 5: MCP Backend の azd/Bicep/コンテナデプロイ基盤(実デプロイは未検証。テスト用 Azure サブスクリプション接続後にユーザーが検証)
- [x] Phase 6: 30分セルフガイドデモ一式([docs/self-guided-demo/](docs/self-guided-demo/))、評価エンジン(`demo-cli evaluate`)、完了サマリー生成(`demo-cli generate-summary`)、合成データ検証スクリプト、CLI 全10コマンド実装完了(`setup`/`cleanup` 含む)、統合・セキュリティ・単体・ドキュメントリンク検証テスト73件追加(64→137件)、MCP Tool 許可リスト機能、ドキュメント一式(設定・コスト・ガバナンス・トラブルシューティング・Industry Pack Guide・MCP Guide・Observability Guide・FAQ・Known Limitations・Release Notes・実 Azure デプロイ手順書)、Workshop Guide・Executive/Technical Presentation(Markdown 形式)。

このチェックリストで「未着手」と書かれている項目を、他のドキュメントで「完成」と記載しないでください。

## 30分デモへのエントリポイント

```bash
python3 -m venv .venv && source .venv/bin/activate && pip install -e ".[dev]"
./scripts/demo/run-demo-cli.sh health
```

その後は [docs/self-guided-demo/README.md](docs/self-guided-demo/README.md) から開始してください。

## 実行モードについて

- **Local Preview Mode**: Azure/Microsoft SaaS 環境なしで、すべての IQ レイヤーをローカルの Mock/Simulated Adapter で模擬し、`GenericLocalOrchestrator` が GitHub Copilot harness の代替として動作します。**Microsoft SaaS サービスの動作検証ではありません。**
- **Hybrid Mode**: 一部のサービスのみ実環境（テスト用 Azure サブスクリプション）に接続します。
- **Full SaaS Mode**: 利用可能な Microsoft サービスを実環境に接続します。ただし利用可能性は必ず Capability Registry と Health Check で判定し、自動的に仮定しません。

## セキュリティ・合成データに関する注記

- サンプルデータはすべて架空データです（実在企業・実在人物・実在顧客データは含みません）。検証方法は [docs/decisions/product-verification.md](docs/decisions/product-verification.md) 相当のプロセスに準じ、Phase 2 以降で `sample-data/` に実データを追加する際に合成データ検証スクリプトを適用します。
- Microsoft 製品の仕様・ライセンス・価格・リージョン・GA/Preview 状態について、未検証の内容は必ず `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION` と明記します。

## 開発環境のセットアップ

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
ruff check .
pytest tests/ -v
```

## Local Preview デモを実行する(Phase 3: 5業界すべて対応)

```bash
./scripts/demo/run-demo-cli.sh health
./scripts/demo/run-demo-cli.sh validate
./scripts/demo/run-demo-cli.sh select-industry financial-services
./scripts/demo/run-demo-cli.sh load-data --industry retail --scale demo
./scripts/demo/run-demo-cli.sh run-demo --industry healthcare
./scripts/demo/run-demo-cli.sh reset
```

`run-demo` は選択中(または `--industry` で指定した)Industry Pack の代表シナリオを実行し、Mock/Simulation の開示、Responsible AI 通知、実行結果(`AgentResponse`)、`scripts/demo/output/last_run.json` への保存を行います。実際の出力例(Manufacturing)は [docs/architecture/sample-outputs/](docs/architecture/sample-outputs/) を参照してください。

## ライセンス

[MIT License](LICENSE)
