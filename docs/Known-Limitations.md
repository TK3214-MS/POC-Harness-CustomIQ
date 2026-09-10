# 既知の制限事項

このドキュメントは、このリポジトリの現時点（Phase 6、ギャップ充足作業込み）における未検証・未実装の項目を、隠さず一覧化するためのものです。README やその他のドキュメントで「完成」と記載されている項目であっても、ここに列挙されている制限は依然として有効です。新しい制限が判明した場合は、このファイルに追記してください。

1. **Live Adapter は実 Microsoft 製品 API に接続しません。** Work IQ / Foundry IQ / Fabric IQ / Copilot Studio の実際の製品 API 統合は、製品仕様が未検証であるため完全に未実装です（`query()` は常に例外を送出）。実務上の意味: このリポジトリだけでは実際の Microsoft 365 データ・Copilot・Fabric ワークスペースには一切アクセスできません。関連: [ADR-0013](decisions/0013-live-adapter-verification-required-scaffold.md)、[docs/decisions/product-verification.md](decisions/product-verification.md)。

2. **実 Azure への `azd up` デプロイは実行・検証されていません。** azd/Bicep のスキャフォールドは存在し Bicep はコンパイルに成功していますが、実サブスクリプションに対するデプロイ実績はありません。実務上の意味: 現状の IaC がそのまま本番相当の Azure 環境で動作するかは未確認です。関連: [docs/deployment/README.md](deployment/README.md)、[ADR-0012](decisions/0012-mcp-backend-deployment-target.md)。

3. **Docker イメージのビルドはローカル環境で検証されていません。** このリポジトリを構築した開発環境には Docker がインストールされておらず、`docker build` はローカルでは一度も実行されていません。CI（`.github/workflows/ci.yml` の `validate-deployment` ジョブ）でのみ実際のビルドが行われます。実務上の意味: Dockerfile はコードレビューベースで作成されており、GitHub Actions 上のビルド結果を信頼の根拠としてください。

4. **Terraform 実装は存在しません。** [deployment/terraform/](../deployment/terraform/) は README のスタブのみで、実際の Terraform コードは未着手です。実務上の意味: IaC ツールとして使えるのは azd/Bicep のみです。関連: [ADR-0008](decisions/0008-deployment-tooling-priority.md)。

5. **MCP Backend にリクエスト認証がありません。** `MCP_BACKEND_API_KEY` 環境変数はプレースホルダーとして `.env.example` に存在しますが、どのミドルウェアにも組み込まれていません。実務上の意味: 現状の MCP Backend はネットワーク経路上で誰でも呼び出せる前提のため、公開ネットワークにそのまま公開すべきではありません。

6. **依存関係の脆弱性スキャンやプロンプトインジェクションのテストはありません。** `pip-audit` や Dependabot のような自動脆弱性スキャン、および意図的なプロンプトインジェクション攻撃を検証するテストスイートは未実装です。実務上の意味: 依存パッケージの既知脆弱性やプロンプトインジェクション耐性は、このリポジトリのテストでは保証されません。

7. **Microsoft Purview / DLP / ガバナンスツールとの統合はありません。** データ分類・DLP ポリシー・監査証跡といったガバナンス機能との連携は未実装です。実務上の意味: 実際の機微データを扱う本番用途に転用する場合、別途ガバナンス統合が必要です。

8. **Application Insights / Azure Monitor との連携はありません。** 現状の観測性は `correlation_id` 付きのローカルロギング（`iq_platform/observability/logging_config.py`）のみで、Application Insights への送信は実装されていません。実務上の意味: 分散トレーシングやクラウド側の可観測性ダッシュボードは現時点では利用できません。`APPLICATIONINSIGHTS_CONNECTION_STRING` は `.env.example` に項目として存在しますが未配線です。

9. **各 Industry Pack のエンティティ種別は代表的なサブセットのみです。** 例えば Manufacturing は Factory / ProductionLine / Supplier / Part / QualityIssue / EngineeringChange の6種のみで、実際の製造業デプロイで想定されうる全エンティティ種別を網羅していません。実務上の意味: 各パックは代表シナリオを動かすための最小限の実装であり、本番相当の業務データモデルとしてそのまま使うことは想定されていません。

10. **Web UI は存在しません。** `apps/demo-ui/` はディレクトリとしては存在しますが、実装は行われておらず CLI（`apps/demo-cli/`）のみが利用可能です。実務上の意味: ブラウザベースの操作画面が必要な場合は別途実装が必要です。

11. **ドキュメントは現時点で日本語のみです。** 英語版ドキュメントは提供されていません。実務上の意味: 英語話者向けの展開には別途翻訳作業が必要です。関連: [docs/decisions/open-questions.md](decisions/open-questions.md) Q1。

12. **GitHub Copilot harness(Copilot Studio)への実接続はありません。これは最も本質的な制限です。** 指示書が前提とするオーケストレーション層は Copilot Studio 上で実行されるハーネスですが、製品仕様が未検証のため、`iq_platform/orchestration/generic_orchestrator.py` の `GenericLocalOrchestrator` を Local Preview Mode 専用の代替として使っています。これは本番アーキテクチャの一部ではなく、将来これを拡張して「本番オーケストレーター」に格上げする計画もありません。実務上の意味: 実際の Copilot Studio 上でこのアクセラレータの Industry Pack(MCP Tool・Agent instructions)を動かすには、別途 Copilot Studio 側の構成作業が必要で、その手順は本リポジトリでは検証できていません。関連: [ADR-0014](decisions/0014-local-orchestrator-is-not-a-harness-replacement.md)、[docs/architecture/architecture-guide.md](architecture/architecture-guide.md) セクション2.1。
