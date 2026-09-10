# Presenter Notes（発表者向けメモ）

## 開始前に

- このデモは Local Preview Mode 前提です。「これは本物の Microsoft サービスですか？」という質問には、はっきり「いいえ、ローカルの Mock/Simulated 実装です」と答えてください。曖昧にしないこと。
- 実行速度は非常に速い（実測で CLI コマンド一式が約2秒）ため、各ステップで一呼吸置いて出力を説明する時間を意識的に取ってください。

## よくある質問と回答例

**Q: Copilot Studio や Foundry IQ は実際に接続されていますか？**
A: いいえ。Local Preview Mode では Work IQ・Foundry IQ・Fabric IQ はすべてローカルの Mock/Simulated Adapter です。Live Adapter（`iq_platform/adapters/*/live_adapter.py`）自体は実装していますが、Microsoft 製品の API 仕様自体が未検証のため、実際の API 呼び出しは一切行いません（[ADR-0013](../decisions/0013-live-adapter-verification-required-scaffold.md)）。

**Q: 別の業界に切り替えるのにどれくらいコードを変更しますか？**
A: ゼロです。`industry-packs/` 配下のデータ・設定を差し替えるだけで、`iq_platform/` の共通コードは一切変更しません。これは [tests/end-to-end/test_industry_pack_switching.py](../../tests/end-to-end/test_industry_pack_switching.py) で自動テストされています。

**Q: このデータは実在企業/実在患者のものですか？**
A: いいえ、完全に合成データです。`scripts/validation/validate_synthetic_data.py` で実在企業名・PII パターンを検出するチェックを実施しています（ただし完全な保証ではなく、ヒューリスティックなスキャンです）。

**Q: 本番環境ではどう変わりますか？**
A: Hybrid/Full SaaS Mode では、実際の Copilot Studio・Work IQ・Foundry IQ・Fabric IQ に接続します。ただし、それらの製品固有の設定手順は本アクセラレータではまだ検証できていません（[docs/setup/live-adapters-configuration.md](../setup/live-adapters-configuration.md)）。テスト用 Azure サブスクリプションが用意でき次第、設定・検証を進める予定です。

**Q: コストはどれくらいですか？**
A: Local Preview Mode 自体はローカル実行のため実コストはありません。実 Azure へのデプロイ時の価格は本アクセラレータでは確定値を記載していません（Microsoft の公式最新情報を確認してください）。

## 見せ方のコツ

- `run-demo` の出力をそのままターミナルで見せるのではなく、`scripts/demo/output/last_run.json` をエディタで開いて `AgentResponse` の構造そのものを見せると、契約ベースの設計思想が伝わりやすいです。
- Industry Pack 切り替え（22〜26分）は、実行前後で `industry-packs/<A>/manifest.yaml` と `industry-packs/<B>/manifest.yaml` を並べて見せると効果的です。
- 禁止事項（`prohibited_actions`）と人間承認ルール（`human_approval_rules`）は、Responsible AI の観点で必ず言及してください。
