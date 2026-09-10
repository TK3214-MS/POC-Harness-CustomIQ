# docs/architecture/sample-outputs/

実際に Local Preview Mode で `run-demo`（Manufacturing Quality Issue Investigation シナリオ）を実行して得られた `AgentResponse` の実例を保存する場所です。

- ここにあるファイルは、実際にコードを実行して得られた出力そのものです（手書きの想定例ではありません）。
- 再生成する場合: `./scripts/demo/run-demo-cli.sh run-demo` を実行し、`scripts/demo/output/last_run.json`（gitignore 対象）の内容をこのディレクトリにコピーしてください。
- `tests/end-to-end/test_manufacturing_e2e.py::test_committed_sample_output_matches_current_schema` が、このファイルが常に現在の `AgentResponse` スキーマと一致していることを検証します。
