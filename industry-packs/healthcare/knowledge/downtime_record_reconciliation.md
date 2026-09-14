# システム停止時記録の照合手順（合成参考文書）

> 文書ID: `HC-KB-007` / 版: 1.0 / 所有者: health information operations lead / 見直し: 半年ごと。本書は架空の業務継続例である。

## 手順

1. 停止期間、影響システム、使用した代替記録、対象IDを記録する。
2. 復旧後、代替記録とシステム上のEncounter/ClinicalEventを照合する。
3. 重複、欠落、時刻差、記録者不明を一覧化する。
4. 訂正は`documentation_correction_and_addendum.md`に従い、原記録を保持する。
5. 照合完了者、確認者、未解決事項を記録する。

## 例外と承認

- 患者取り違え、重大な欠落、復旧後の重複はclinicianと情報管理責任者へエスカレーションする。
- エージェントは記録を統合・削除せず、臨床的意味を推測しない。

関連文書: `documentation_completeness_checklist.md`、`documentation_correction_and_addendum.md`。
