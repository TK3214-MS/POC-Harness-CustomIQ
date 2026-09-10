# ADR-0010: Industry Pack コードはプラグインとして動的ロードする（静的 Python パッケージにしない）

- ステータス: Accepted
- 日付: 2026-09-08

## コンテキスト

`industry-packs/` 配下のフォルダ名（`financial-services`, `public-sector` 等）はケバブケースであり、指示書 §15 の記述に従う必要がある一方、Python の `import` 文はハイフンを含む識別子をサポートしない（[ADR-0009](0009-python-package-naming.md) と同様の制約）。

加えて、指示書 §2 の最重要目的は「業界切り替え時にプラットフォームコードを直接変更しない」ことであり、Industry Pack 内のコード（データ生成ロジック、MCP Tool 実装）は本質的に差し替え可能な「設定 + プラグイン」として扱うべきで、プラットフォームに静的にコンパイル/インポートされるコードとして扱うべきではない。

## 決定

Industry Pack 内の実行可能な Python コード（例: `data/generator.py`, `tools/manufacturing_tools.py`）は、`iq_platform.orchestration.industry_pack_loader.load_plugin_module()` が `importlib.util.spec_from_file_location` を使ってファイルパスから実行時に動的ロードする。`manifest.yaml` の `sample_data_path` / `mcp_tools_path` がロード対象のパスを示す。ドット区切りの Python パッケージとして静的にインポートすることはしない。

プラグインモジュールは以下の安定インターフェースを実装しなければならない。

- データ生成モジュール: `generate_dataset(seed: int, scale: str) -> dict`
- MCP Tool モジュール: `TOOL_FUNCTIONS: dict[str, Callable[[dict, dict], dict]]`, `TOOL_DESCRIPTIONS: dict[str, str]`

## 影響

- 新しい Industry Pack を追加しても、プラットフォームコードや `pyproject.toml` のパッケージ探索設定を変更する必要がない。
- このインターフェース自体が契約であり、変更する際は Contract/Integration テストで検証する。動的インポート境界をまたぐ静的型チェックは本質的に弱くなるため、実行時テストに依存する。
- `services/mcp-backend/` の `ToolRegistry` は、どの Industry Pack の `TOOL_FUNCTIONS` を渡されても同じように動作する（[ADR-0006](0006-mcp-tool-response-contract.md) のレスポンス契約と組み合わせて機能する）。
