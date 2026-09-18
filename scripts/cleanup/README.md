# scripts/cleanup/

[![日本語](https://img.shields.io/badge/%E3%81%82-%E6%97%A5%E6%9C%AC%E8%AA%9E-087F8C?style=for-the-badge)](README.md) [![English](https://img.shields.io/badge/A-English-5B6670?style=for-the-badge)](README.en.md)

デモ環境のリセット・クリーンアップスクリプト（`reset` / `cleanup` コマンド、instruction §28）。

**状態: 実装済み。** [cleanup-azure.sh](cleanup-azure.sh) は実際にデプロイされたAzureリソースを`azd down --purge --force`で削除する破壊的スクリプトです。環境名の手入力確認を必須とし、自動実行やテストからは呼び出しません。
