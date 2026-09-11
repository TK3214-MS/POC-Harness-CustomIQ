# 既知の制限事項

- Fabric IQ、Foundry IQ、Work IQの実SaaSテナントへの接続検証は、このリポジトリのテスト環境では実施していません。実施手順は[本番環境構築ガイド](Production-Environment-Setup.md)を参照してください。
- Copilot StudioからMCP Backendへ接続する場合、実環境での受信認証、ネットワーク公開、TLS、allowlistを別途構成する必要があります。
- MCP BackendのAzureへの`azd`デプロイは、対象subscription・region・quota・RBACによって結果が変わるため、実環境での事前検証が必要です。
- Work IQ、Fabric IQ、Foundry IQはPreview機能を含みます。Preview機能を本番利用できるか、ライセンス、価格、リージョン、課金条件を構築時点の公式ドキュメントで確認してください。
- 本リポジトリはIQサービスのSaaS側データ登録、Ontology設計、Knowledge Base運用、Microsoft 365データ管理を代行しません。これらは各SaaS管理者が実施します。
