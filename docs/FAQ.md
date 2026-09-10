# よくある質問（FAQ）

> このドキュメントは 2026-09-10 時点（Phase 6、ギャップ充足作業込み）の実装状況に基づきます。実装状況は変化するため、疑わしい場合は [README.md](../README.md) のチェックリストと [docs/Known-Limitations.md](Known-Limitations.md) を優先してください。

## Q. これは今日、実際の Microsoft 365 / Copilot のデータに接続されていますか？

**いいえ。** このリポジトリのデフォルトかつ現時点で唯一検証済みの実行モードは **Local Preview Mode** です。Work IQ / Foundry IQ / Fabric IQ に相当する処理はすべてローカルの Mock/Simulated Adapter が模擬しており、実際の Microsoft 365 テナントや Copilot、実際の業務データには一切接続していません。合成データ（架空の企業・人物・顧客データ）のみを使用します。

Live Adapter という仕組みは実装されていますが、これは「実 API に接続して動く」という意味ではありません。詳細は次の質問を参照してください。

## Q. 「verification_required」モードとは何ですか？なぜ「live」にならないのですか？

Work IQ / Foundry IQ / Fabric IQ の Live Adapter は、`mode` プロパティが次の5値のいずれかを取ります: `live` / `mock` / `simulated` / `unavailable` / `verification_required`。

このリポジトリでは、環境変数（Entra ID の設定含む）が未設定であれば `unavailable`、設定済みであれば `verification_required` になりますが、**`live` には絶対に到達しません**。理由は、Work IQ / Foundry IQ / Fabric IQ という Microsoft 製品自体の存在・API 仕様・認証スコープが未検証だからです（[docs/decisions/product-verification.md](decisions/product-verification.md)）。

実装済みなのは (1) 環境変数の存在確認による `unavailable` → `verification_required` の遷移と、(2) `azure-identity` の `ClientSecretCredential` による実際の Microsoft Entra ID 認証、の2点のみです。`query()` メソッドは製品 API のリクエスト/レスポンス形状を推測することを避けるため、常に `LiveAdapterNotYetVerifiedError` を送出します。設計判断の詳細は [ADR-0013](decisions/0013-live-adapter-verification-required-scaffold.md) を参照してください。

## Q. 今、実際に何が動きますか？

- **Local Preview Mode** での全機能。
- **5つの Industry Pack すべて**（Manufacturing / Financial Services / Retail / Healthcare / Public Sector）— Industry Pack を切り替えてもプラットフォームのコードは一切変更されません。
- **Demo CLI の全10コマンド**: `setup` / `health` / `validate` / `load-data` / `select-industry` / `run-demo` / `evaluate` / `generate-summary` / `reset` / `cleanup`。
- **137件のテスト**（contract / end-to-end / evaluation / integration / security / unit / validation の7カテゴリ）が `pytest tests/ -v` ですべて成功します。
- MCP Backend（FastAPI）を `fastapi.testclient.TestClient` 経由でプロセス内から呼び出す統合。
- Bicep テンプレートのコンパイル検証（`az bicep build`）と、CI 上での MCP Backend コンテナイメージのビルド検証。

## Q. これを今日 Azure にデプロイできますか？

**部分的にのみ可能で、実行自体はまだ検証されていません。** MCP Backend を Azure Container Apps にデプロイするための azd/Bicep 構成一式（[deployment/azd/](../deployment/azd/)、[deployment/bicep/](../deployment/bicep/)、[deployment/containers/](../deployment/containers/)）は実装済みで、Bicep は `az bicep build` でのコンパイルに成功しています。しかし、実際の Azure サブスクリプションに対して `azd up` を実行した実績はまだありません。

実際にデプロイしたい場合は、[docs/deployment/Step-by-Step-Deployment-Guide.md](deployment/Step-by-Step-Deployment-Guide.md) の手順に従ってください。Terraform（[deployment/terraform/](../deployment/terraform/)）は README のスタブのみで未実装です（[ADR-0008](decisions/0008-deployment-tooling-priority.md) により優先度最低）。

## Q. 6つ目の業界（Industry Pack）を追加するにはどうすればよいですか？

各 Industry Pack が満たすべきスキーマ・ファイル構成・実装手順は [docs/industry-packs/Industry-Pack-Guide.md](industry-packs/Industry-Pack-Guide.md) を参照してください。既存の5パックはすべて同一のファイルレイアウト（`manifest.yaml`、`ontology/`、`data/generator.py`、`knowledge/`、`work-context/`、`tools/`、`semantics/`、`agents/`、`prompts/`、`expected-results/`、`evaluations/`、`terminology/`、`responsible-ai/`）に従っており、`iq_platform.contracts.manifest.IndustryPackManifest`（[ADR-0004](decisions/0004-industry-pack-manifest-schema.md)）で検証されます。新しいパックを追加する際は `iq_platform/` 配下のプラットフォームコードを変更する必要はありません（[ADR-0011](decisions/0011-generic-orchestrator-and-semantic-adapter.md)）。

## Q. なぜドキュメントは日本語のみなのですか？

これは Phase 0 で提起された未解決事項 Q1（英語のみか、英日併記か）への回答として、2026-09-08 に「当面は日本語のみ」と決定されたためです。詳細は [docs/decisions/open-questions.md](decisions/open-questions.md) の Q1 を参照してください。今後この方針が変わる場合は、同ドキュメントの該当行が更新されます。

## Q. 「Mock」「Simulated」「Live」の違いは何ですか？

`iq_platform.contracts.capability.AdapterMode` が定義する5値のうちの3つです。

- **Mock**: 固定または簡易ロジックで応答を生成する、実データ・実 API を一切使わないアダプター。
- **Simulated**: 合成データ（架空だが現実的な構造を持つデータ）を使ってより現実に近い応答を生成するアダプター。
- **Live**: 実際の Microsoft 製品 API に接続するアダプター。このリポジトリでは Work IQ / Foundry IQ / Fabric IQ の Live Adapter は前述のとおり `live` に到達しません。

すべての `AgentResponse` には `mock_or_simulation_disclosure` フィールドが必須であり、どのレイヤーが Mock/Simulated で動作したかを回答内で必ず開示します（[ADR-0005](decisions/0005-agent-response-contract.md)）。

## Q. テストはどこにあり、どう実行しますか？

`tests/contract/`、`tests/end-to-end/`、`tests/evaluation/`、`tests/integration/`、`tests/security/`、`tests/unit/`、`tests/validation/` の7カテゴリに分かれており、合計137件です。次のコマンドで全テストを実行できます。

```bash
pytest tests/ -v
```

Lint は `ruff check .`（自動修正は `ruff check . --fix`）です。

## Q. セキュリティ面で何が実装されていて、何が未実装ですか？

現時点で実装済みなのは、Secret のコミット防止（`.env` の gitignore、`.env.example` はプレースホルダー値のみ）、`scripts/security/scan_secrets.py` によるヒューリスティックな Secret スキャン、`scripts/validation/validate_synthetic_data.py` による合成データ限定チェック、コンテナの非 root 実行と `HEALTHCHECK`、ACR の admin ユーザー無効化 + User-Assigned Managed Identity + AcrPull の最小権限ロールです。未実装なのは、依存関係の脆弱性スキャン（pip-audit/Dependabot 等）、プロンプトインジェクションのテストスイート、MCP Backend へのリクエスト認証（API キー/OAuth）です。詳細は [SECURITY.md](../SECURITY.md) と [docs/Known-Limitations.md](Known-Limitations.md) を参照してください。

## Q. バージョン番号やリリースタグはありますか？

**ありません。** このリポジトリは pre-1.0 の単一継続ビルドであり、Phase 0 から Phase 6 まで連続的に実装が進められています。バージョンタグや GitHub Release はまだ一つも作成されていません。これまでの経緯は [docs/Release-Notes.md](Release-Notes.md) を参照してください。
