# scripts/cleanup/

デモ環境のリセット・クリーンアップスクリプト（`reset` / `cleanup` コマンド、instruction §28）。

**状態: 一部実装済み(Phase 5)。** ローカルデモ出力のリセットは `apps/demo-cli` の `reset` コマンドで実装済み(Phase 2)。[cleanup-azure.sh](cleanup-azure.sh) は実際にデプロイされた Azure リソースを `azd down --purge --force` で削除する破壊的スクリプトで、環境名の手入力確認を必須とし、自動実行やテストからは呼び出されない。
