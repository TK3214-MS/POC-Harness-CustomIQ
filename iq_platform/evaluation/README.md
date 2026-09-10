# iq_platform/evaluation/

Grounding / Citation correctness / Retrieval relevance / Entity accuracy / Hallucination resistance 等の評価ロジック（instruction §22.6）。

**状態: 一部実装済み（Phase 6）。** [rubric_evaluator.py](rubric_evaluator.py) が各 Industry Pack の `evaluations/rubric.yaml` に対する基準ごとの自動チェック（citation_presence, relationship_presence, mock_disclosure, human_in_the_loop, no_prohibited_action 等）を実装（`demo-cli evaluate` から呼び出される）。未知の criterion id は `not_automatically_checked` として正直に報告し、誤って pass 扱いにしない。Retrieval relevance の定量評価、Hallucination resistance の本格的な検証は未実装（チェックはあくまでヒューリスティックな代理指標）。
