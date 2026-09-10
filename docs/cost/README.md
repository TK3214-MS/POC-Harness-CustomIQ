# コスト分析 (Cost Analysis)

**このドキュメントに金額（$/円等）の見積もりは一切含まれません。** Azure Container Apps・Azure Container Registry・Log Analytics を含む、本リポジトリが参照するすべての Microsoft/Azure 製品の価格・課金体系は未検証です。価格に触れる箇所はすべて `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION` と明記し、[docs/decisions/product-verification.md](../decisions/product-verification.md) を一次情報源として参照してください。実際の見積もりが必要な場合は、Azure の公式価格ページ・Azure Pricing Calculator を確認日時付きで参照し、その結果を `product-verification.md` に追記してから初めてこのドキュメントを更新してください。

このドキュメントは、利用モードを4段階（Option A〜D）に分けて、それぞれのコスト要因（コストドライバー）と、現時点で判明している構成（SKU 等）を整理します。

## Option A: Local Preview Mode のみ

- **内容**: すべての IQ レイヤーをローカルの Mock/Simulated Adapter で模擬する、開発者ローカル PC 上での実行（[README.md](../../README.md) の「実行モードについて」を参照）。
- **Azure コスト**: なし。Azure リソースを一切作成しません。
- **前提コンポーネント**: ローカル Python 環境（`.venv`）のみ。
- **想定利用シーン**: 開発、5業界すべての E2E デモ、`demo-cli evaluate`/`generate-summary` によるルーブリック評価。現時点で最も広く検証されているモードです（[docs/architecture/architecture-guide.md](../architecture/architecture-guide.md) 8節）。

## Option B: MCP Backend を Azure Container Apps にデプロイ（現在の Phase 5 実装範囲）

- **内容**: `services/mcp-backend/` の FastAPI アプリを Azure Container Apps にデプロイした状態（[deployment/bicep/resources.bicep](../../deployment/bicep/resources.bicep)、[ADR-0012](../decisions/0012-mcp-backend-deployment-target.md)）。IQ レイヤー自体（Work IQ / Foundry IQ / Fabric IQ）は依然として Mock/Simulated のままです。
- **コストが発生しうる Azure リソース**（実デプロイは未検証、[docs/deployment/README.md](../deployment/README.md) 参照）:

  | リソース | 選定 SKU/構成（コスト関連ノブ） | 価格 |
  |---|---|---|
  | Azure Container Registry | `Basic` SKU、管理者ユーザー無効化（User-Assigned Managed Identity + `AcrPull` ロールでアクセス） | `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION` |
  | Azure Container Apps（`mcp-backend` コンテナ） | 1 コンテナあたり `0.5 vCPU` / `1Gi` メモリ、レプリカ数 `minReplicas: 0` 〜 `maxReplicas: 2`（サーバーレス、アイドル時にゼロスケール） | `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION` |
  | Log Analytics ワークスペース | `PerGB2018` SKU、保持期間 30日固定 | `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION` |

- **コストドライバー（定性的に判明している事項のみ）**:
  - Container Apps は `minReplicas: 0` のためアイドル時はゼロスケールし、リクエストが無い期間のコンピューティング課金は発生しにくい構成です（ただしスケールアウト/インの正確な課金境界は要確認）。
  - Ingress は既定で内部限定（`external: false`）のため、現状のデプロイ構成では外部向けの受信データ転送は発生しません。
  - Log Analytics の保持期間は30日固定で設定されており、これより長い保持が必要な場合は追加のコストドライバーになり得ます。
  - Container Registry は `Basic` SKU 固定で、ストレージ容量やスループットの上位 SKU（`Standard`/`Premium`）は選択されていません。
- **未検証の重要な前提**: 上記はいずれも Bicep 定義上の構成値であり、実際に `azd up` を実行してのコスト実測は一度も行われていません（[docs/deployment/README.md](../deployment/README.md)）。コンテナイメージも現状プレースホルダー（`mcr.microsoft.com/azuredocs/containerapps-helloworld:latest`）であり、実イメージのビルド・実行時のリソース使用量とは異なる可能性があります。

## Option C: Hybrid Mode（MCP Backend デプロイ + 一部 Live Adapter 接続）

- **内容**: Option B に加え、Work IQ / Foundry IQ / Fabric IQ のいずれか1つ以上を実 Microsoft SaaS 製品に接続する構成（[docs/decisions/open-questions.md](../decisions/open-questions.md) Q4 のテスト用 Azure サブスクリプションを利用）。
- **現状の実装範囲**: Live Adapter は `verification_required` スキャフォールドまでの実装であり（[ADR-0013](../decisions/0013-live-adapter-verification-required-scaffold.md)）、`query()` は常に例外を送出するため、この Option C は**設計上は想定されているが、実際に「動作する」Hybrid Mode としては未実現**です。
- **追加コスト**: 各 Microsoft 製品（Work IQ / Foundry IQ / Fabric IQ）自体のライセンス費用・従量課金は、製品の存在・仕様自体が [docs/decisions/product-verification.md](../decisions/product-verification.md) の通り未検証であるため、完全に `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION` です。
- **想定コストドライバー（製品仕様確定後に埋めるべき項目)**: ライセンス階層、API 呼び出し回数課金の有無、テナント/ワークスペース単位の固定費用など。いずれも現時点では不明です。

## Option D: Full SaaS Mode（全 IQ レイヤー + Copilot Studio harness を実接続）

- **内容**: すべての IQ レイヤー（Work IQ / Foundry IQ / Fabric IQ）に加え、GitHub Copilot harness（Microsoft Copilot Studio 相当）も実環境に接続するフルスタック構成。
- **現状**: **完全に未実現**です。Copilot Studio 自体の製品名・GA/Preview 状態・ライセンスモデルが未検証であること（[docs/decisions/product-verification.md](../decisions/product-verification.md)）に加え、Option C の Live Adapter 統合自体が未完了のため、Option D はこの2つの未検証事項の両方に依存してブロックされています。
- **コスト**: 完全に `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`。ライセンス費用の見積もりを行う前に、まず [docs/decisions/product-verification.md](../decisions/product-verification.md) のプロセスに従った製品検証が必須です。

## まとめ表

| Option | Azure/Microsoft コスト発生 | 実装状況 |
|---|---|---|
| A: Local Preview Mode | なし | 実装済み・テスト済み（5業界すべて） |
| B: MCP Backend デプロイのみ | あり（すべて TBD、Bicep 構成は判明） | インフラ実装済み・実デプロイ未検証 |
| C: Hybrid Mode（一部 Live Adapter 接続） | あり（完全に TBD） | Live Adapter は verification_required スキャフォールドのみ、`query()` 未実装のため機能としては未実現 |
| D: Full SaaS Mode | あり（完全に TBD） | 未実現（製品検証・Live Adapter 実装の両方が前提） |

関連ドキュメント: [docs/deployment/README.md](../deployment/README.md)（デプロイ実装状況）、[ADR-0008](../decisions/0008-deployment-tooling-priority.md)（デプロイツール優先順位）、[ADR-0012](../decisions/0012-mcp-backend-deployment-target.md)（MCP Backend のデプロイ先選定理由）、[docs/decisions/product-verification.md](../decisions/product-verification.md)（価格を含む未検証事項の一覧と検証プロセス）。
