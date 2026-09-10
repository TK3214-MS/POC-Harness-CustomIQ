# ADR-0009: Python パッケージ命名規則（標準ライブラリとの衝突回避）

- ステータス: Accepted
- 日付: 2026-09-08

## コンテキスト

指示書 §15 のリポジトリ構成では、最上位フォルダ名として `platform/` および `platform/capability-registry/` が指定されている。しかし、Python の標準ライブラリには `platform` という名前のモジュールが既に存在し、OS/バージョン判定のために `pip`、`setuptools`、その他多数のサードパーティライブラリが依存している。

[ADR-0002](0002-python-primary-language.md) により全コンポーネントを Python で実装することが決まったため、この衝突は理論上の懸念ではなく実際のリスクになった。開発時にリポジトリルートを `sys.path`（または `pytest` の `pythonpath`）に追加するフローでは、同名のトップレベルパッケージ `platform/` を作ると標準ライブラリの `platform` モジュールを覆い隠し（shadowing）、無関係なツールやライブラリの `import platform` を壊す可能性がある。

また、Python の `import` 文はハイフンを含む識別子をサポートしないため、`capability-registry` はそのままではインポートできない。

## 決定

- 実装上のトップレベル Python パッケージ名は `platform/` ではなく **`iq_platform/`** とする。
- `platform/capability-registry/` は **`iq_platform/capability_registry/`**（アンダースコア）とする。
- それ以外の、Python パッケージとして直接 `import` されないコンテナフォルダ（`industry-packs/`, `sample-data/`, `apps/demo-cli/`, `apps/demo-ui/`, `services/mcp-backend/` 等）は、指示書どおりケバブケースの名称を維持する。これらのフォルダ内部に Python コードを置く場合（例: `services/mcp-backend/` 内の FastAPI アプリ）は、内部のインポート可能なパッケージ名を snake_case（例: `mcp_backend`）にする。

## 影響

- 指示書の記述（`platform/...`）と物理フォルダ名（`iq_platform/...`）が完全一致しなくなる。この対応関係は本 ADR と [docs/architecture/architecture-guide.md](../architecture/architecture-guide.md) の「命名規則に関する注意」に明記する。
- 今後、指示書を参照しながら実装する開発者・エージェントは、`platform/` という記述を見たら `iq_platform/` に読み替える。
- `config/`（YAML データのみ、Python パッケージではない）は標準ライブラリと衝突しないため、そのままの名称を維持する。
