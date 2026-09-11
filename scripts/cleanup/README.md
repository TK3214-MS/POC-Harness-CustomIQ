# scripts/cleanup/

デモ環境のリセット・クリーンアップスクリプト（`reset` / `cleanup` コマンド、instruction §28）。

**状態: 実装済み。** [cleanup-azure.sh](cleanup-azure.sh) は実際にデプロイされたAzureリソースを`azd down --purge --force`で削除する破壊的スクリプトです。環境名の手入力確認を必須とし、自動実行やテストからは呼び出しません。
