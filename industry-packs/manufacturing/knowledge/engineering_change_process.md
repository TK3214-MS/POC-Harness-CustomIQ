# Engineering Change Process (Synthetic Reference Document)

> This is a synthetic reference document created for the Industry IQ Platform Accelerator demo. It does not represent a real company's process and cites no real standards or certifications.

## Overview

An Engineering Change (EC) is opened when a quality issue requires a change to a part specification, process, or design to prevent recurrence.

## Lifecycle

An EC moves through the following statuses:

1. `proposed` - an engineer has proposed a change but it has not started.
2. `in_progress` - the change is being designed/evaluated.
3. `approved` - an engineering lead has approved the change.
4. `implemented` - the change has been rolled out to production.

## Human Approval Requirement

An EC may not move to `approved` status without sign-off from an engineering lead. This accelerator's agents may recommend that an EC be opened or followed up on, but never automatically approve or implement one (see `industry-packs/manufacturing/manifest.yaml` `human_approval_rules`).

## 品質問題の終結条件

関連するEngineering Changeがある品質問題は、ECが`approved`または`implemented`であること、追加検査結果が受入基準内であること、原因分析と是正処置の証跡が揃っていることをquality engineerが確認するまで終結できない。`proposed`または`in_progress`のECが残る場合、エージェントは不足項目を提示するだけで、品質問題を`resolved`へ変更しない。
