# iq_platform/configuration/

環境固有値（`.env` / `config/environments/`）の読み込みと検証を行う設定管理層。

**状態: 一部実装済み（Phase 4）。** `settings.py` の `LiveAdapterSettings` が Live Adapter 用の環境変数（Entra ID、Work IQ/Foundry IQ/Fabric IQ/Copilot Studio の設定値）を読み込み検証する。`config/environments/`（実行モード別設定）は未実装（Phase 5）。

`config/capabilities.yaml` の読み込みは `iq_platform/capability_registry/` が担当します（役割が異なるため分離）。
