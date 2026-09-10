# ADR-0012: MCP Backend のデプロイ先は Azure Container Apps + ACR とする（Phase 5）

- ステータス: Accepted
- 日付: 2026-09-10

## コンテキスト

指示書 §15 はデプロイ方式の優先順位を azd → Bicep → Terraform と定めている（[ADR-0008](0008-deployment-tooling-priority.md)）。Phase 5 時点でデプロイ可能な実体は `services/mcp-backend/`（FastAPI コンテナ）のみであり、Work IQ / Foundry IQ / Fabric IQ の Live Adapter（Phase 4）はまだ存在しないため、これらのためのインフラは含めない。

## 決定

- ホスティング先は **Azure Container Apps**（`Microsoft.App/containerApps`）とする。理由: サーバーレススケール(0レプリカまでスケールダウン可能)、コンテナベースでこのアクセラレータのポータビリティ方針と合致、azd の `host: containerapp` テンプレートパターンと直接対応する。
- コンテナイメージは **Azure Container Registry (Basic SKU)** に保持し、**User-Assigned Managed Identity + AcrPull ロール**でプルする（Admin ユーザーは無効化、instruction §24 の least privilege に従う）。
- ログは **Log Analytics** に集約する（Container Apps Environment の必須要件でもある）。
- Ingress は **既定で internal-only**(`external: false`)とする。外部公開が必要な場合は明示的な承認を得てから `external: true` に変更する（instruction §24「破壊的・高影響な変更前に説明する」に準拠）。
- コンテナイメージの既定値はプレースホルダー(`mcr.microsoft.com/azuredocs/containerapps-helloworld:latest`)とし、実際の `services/mcp-backend` イメージへの置き換えは `azd deploy`（またはコンテナビルド後の再デプロイ）で行う想定とする。

## 検証状況

- `az bicep build` でのローカルコンパイルは成功（2026-09-10、警告1件のみ: ACR 名の最小長に関する静的解析上の注意、実害なし）。
- **実際の `azd up` / `azd provision` によるデプロイは実行していない**（本開発環境に実 Azure サブスクリプション認証情報がないため）。[docs/decisions/open-questions.md](open-questions.md) Q4 の回答（テスト用 Azure サブスクリプション使用）に基づき、Phase 5 以降でユーザーが実環境に対して検証することを想定する。
- Docker イメージのビルド検証（`docker build`）はこの開発環境に Docker がインストールされていないため未実施。CI（`.github/workflows/ci.yml`）でビルド検証を行う。

## 影響

- README・デプロイガイドには「Bicep テンプレートはコンパイル検証済みだが実デプロイ未検証」であることを明記する。
- Terraform は本 Phase では着手しない（[ADR-0008](0008-deployment-tooling-priority.md) の優先順位通り）。
- Work IQ / Foundry IQ / Fabric IQ Live Adapter 用のインフラ（Phase 4）は、実際に Adapter を実装し Microsoft 製品仕様を検証した後に追加する。
