# ガバナンスガイド (Governance Guide)

このガイドは、本アクセラレータにおけるデータガバナンス・監査証跡・Human-in-the-Loop（人間による承認）の**現状の実装範囲**を正直に記載するものです。「未実装」と明記した項目を、他のドキュメントで完成扱いにしないでください（[.github/copilot-instructions.md](../../.github/copilot-instructions.md)）。

## 1. データ分類の方針: 合成データのみ

本リポジトリの `sample-data/` および各 Industry Pack の `data/generator.py` が生成するデータは、**すべて架空（合成）** です。実在の企業名・実在の人物名・実在の顧客データは一切含まれません。

これは次の2つのスクリプトで強制されています。

- [scripts/validation/validate_synthetic_data.py](../../scripts/validation/validate_synthetic_data.py) — Industry Pack のコンテンツ（データジェネレータ、ナレッジ文書、work-context フィクスチャ）に対し、実在企業名の denylist（`Microsoft` / `Amazon` / `Toyota` / `JPMorgan` 等）およびメールアドレス・電話番号・SSN 様パターンをスキャンします。
- [scripts/security/scan_secrets.py](../../scripts/security/scan_secrets.py) — シークレットの混入をヒューリスティックにスキャンします（データそのものではなくソースコード対象）。

**重要な限界**: これらは正規表現・denylist ベースのヒューリスティックスキャンであり、「完全に合成データであることの法的・コンプライアンス上の保証」ではありません。新しい denylist 用語やパターンでの回避は検出できない可能性があります。実運用でのデータ投入前には、必ず人手によるレビューも併用してください。

## 2. Microsoft Purview / DLP 統合について

**現状: 一切実装されていません。**

- `config/capabilities.yaml` の `governance.purview` に相当する Capability エントリは、統合コードを一切持たない TBD 状態のプレースホルダーです。
- データ分類ラベル（Sensitivity Label）の付与・伝播、DLP（Data Loss Prevention）ポリシーの適用、Purview 監査ログとの連携は、コード・設計のいずれのレベルでも未着手です。
- Microsoft Purview がこのアクセラレータのユースケース（エージェントが取得したコンテンツへのラベル継承等）にどう適用されるか自体が [docs/decisions/product-verification.md](../decisions/product-verification.md) の通り未検証です。

将来的に実装する場合に必要になる代表的な作業（すべて未着手・TBD）:

- Purview アカウントとの接続、Sensitivity Label の読み取り/適用 API 統合
- ラベル付きソースから取得したコンテンツへのラベル継承ロジック（`AgentResponse.documents_and_citations` 等への反映）
- DLP ポリシー違反時のブロック/警告フロー
- Purview 側の監査ログとこのリポジトリの `correlation_id` ベースのログとの相関付け

## 3. 監査証跡（Audit Trail）

現状実装されている監査証跡は、`correlation_id` を付与した構造化ログのみです（[iq_platform/observability/logging_config.py](../../iq_platform/observability/logging_config.py)）。

- すべてのログ行に `correlation_id` を含めるフォーマッタ（`_CorrelationIdFormatter`）を使用し、`extra={"correlation_id": ...}` が渡されない場合は `-` を出力します。
- `AgentResponse`（[iq_platform/contracts/agent_response.py](../../iq_platform/contracts/agent_response.py)）の `trace_or_correlation_id` フィールドが、各エージェント実行と上記ログ行を紐づける識別子です。
- 現状は標準出力へのロギングのみで、Application Insights 等の集中管理された観測性基盤への送信・長期保管・改ざん防止（tamper-evidence）は実装されていません（`.env.example` の `APPLICATIONINSIGHTS_CONNECTION_STRING` はプレースホルダーのままです）。
- 監査証跡としての要件（誰が・いつ・どの承認を行ったか等の構造化された記録）を満たす専用の監査ログストアは未実装です。

## 4. Human-in-the-Loop（人間承認）の要件

エージェントの最終回答契約 `iq_platform.contracts.agent_response.AgentResponse`（[ADR-0005](../decisions/0005-agent-response-contract.md)）は `human_in_the_loop_requirements: list[str]` フィールドを持ち、そのシナリオ実行で人間の承認が必要となるアクションを明示します。このフィールドは必須フィールドとして定義されており、省略した `AgentResponse` は構築できません。

さらに各 Industry Pack の `manifest.yaml` は、業界固有の承認ルールを次の2つの配列で宣言します（実例: [industry-packs/manufacturing/manifest.yaml](../../industry-packs/manufacturing/manifest.yaml)）。

- `prohibited_actions` — エージェントが自動実行してはならないアクションの一覧（例: 「品質問題を人間のレビューなしに自動クローズすること」）
- `human_approval_rules` — 承認が必要なアクションごとの `action` / `reason`（なぜ承認が必要か）/ `required_approver_role`（必要な承認者ロール）の組。Manufacturing パックの例では `close_quality_issue`（`quality_engineer` の承認が必要）と `approve_engineering_change`（`engineering_lead` の承認が必要）を宣言しています。

これらは `tests/end-to-end/test_industry_pack_switching.py` で「禁止アクションを示す文言がエージェントの推奨アクションに混入していないか」を機械的に検証していますが、**実際に人間の承認ワークフロー（承認 UI、承認履歴の記録、承認者ロールの認証・認可）自体は実装されていません**。現状は「モデル/シナリオロジックが禁止アクションを自動実行しない」ことと「承認が必要である旨を回答に含める」ことまでが実装範囲です。

## 5. 実運用でガバナンスを満たすために追加が必要なもの（すべて未実装・TBD）

実際の本番環境でこのアクセラレータを使う場合、少なくとも次の項目の追加実装が必要です。現時点ではいずれも設計・コードとも未着手です。

| 項目 | 現状 | 備考 |
|---|---|---|
| Microsoft Purview 統合（分類ラベル・DLP） | 未実装（`config/capabilities.yaml` に TBD プレースホルダーのみ） | 製品仕様自体が未検証（[docs/decisions/product-verification.md](../decisions/product-verification.md)） |
| データ保持ポリシー（Retention Policy） | 未実装 | Log Analytics のログ保持は30日固定（[deployment/bicep/resources.bicep](../../deployment/bicep/resources.bicep)）だが、これはコスト設定であってガバナンス上のポリシーではない |
| 承認ワークフローの実装（UI・承認履歴・ロールベース認可） | 未実装 | `manifest.yaml` の `human_approval_rules` は宣言のみで、実行系との連携なし |
| 監査ログの集中管理・改ざん防止 | 未実装 | 標準出力への `correlation_id` ロギングのみ |
| 依存関係の脆弱性スキャン（pip-audit / Dependabot 等） | 未実装 | [docs/troubleshooting/README.md](../troubleshooting/README.md) にも既知のギャップとして記載 |
| プロンプトインジェクション対策のテストスイート | 未実装 | 同上 |
| 実データ投入時の法務・コンプライアンスレビュープロセス | 未実装 | 現状のヒューリスティックスキャン（本ガイド1節）は代替になりません |

関連: [docs/security/README.md](../security/README.md)（セキュリティ観点の詳細）、[SECURITY.md](../../SECURITY.md)（脆弱性報告方針）、[docs/decisions/0007-capability-registry-authority.md](../decisions/0007-capability-registry-authority.md)（Capability Registry のガバナンス）。
