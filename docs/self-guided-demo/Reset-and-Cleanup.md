# Reset and Cleanup（リセット・後片付け）

## ローカルデモ出力のリセット（Local Preview Mode、常に安全）

```bash
./scripts/demo/run-demo-cli.sh reset
```

`scripts/demo/output/`（生成データセット、実行結果、評価結果、完了サマリー、選択中の Industry Pack 状態）をすべて削除します。ソースコードやドキュメントには一切影響しません。何度でも安全に再実行できます。

## 実 Azure リソースのクリーンアップ（Hybrid/Full SaaS Mode を試した場合のみ）

**警告: 破壊的操作です。** 実際に `azd up` でデプロイした場合のみ必要です。Local Preview Mode のみを使った場合は不要です。

```bash
./scripts/cleanup/cleanup-azure.sh
```

このスクリプトは azd 環境名の手入力確認を必須とし、確認が一致しない限り何も削除しません。詳細は [scripts/cleanup/README.md](../../scripts/cleanup/README.md) を参照してください。

## デモ後のチェック

- [ ] `scripts/demo/output/` が空、または削除済み
- [ ] `.env` に実際の Secret を設定していた場合、共有前に削除したか確認
- [ ] 実 Azure リソースをデプロイしていた場合、`cleanup-azure.sh` を実行したか確認
