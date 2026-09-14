# GitHub Pages公開

このサイトはMkDocs Materialで構築し、GitHub ActionsからGitHub Pagesへ公開します。

## 初回だけ行う設定

1. GitHub repositoryの **Settings > Pages** を開く。
2. **Build and deployment > Source**で **GitHub Actions**を選択する。
3. Actionsの実行とPages deploymentを許可するrepository policyを確認する。

## ローカル確認

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
mkdocs serve
```

表示されたローカルURLをブラウザーで開きます。公開前の最終検証は次を実行します。

```bash
mkdocs build --strict
```

## 公開

`docs/**`、`mkdocs.yml`、`pyproject.toml`、Pages workflowのいずれかを`main`へ反映すると、`.github/workflows/pages.yml`がサイトを構築して公開します。Pull Requestではstrict buildだけを実行し、公開しません。Actions画面の`Deploy labs to GitHub Pages`から手動実行もできます。

公開先:

```text
https://tk3214-ms.github.io/POC-Harness-CustomIQ/
```

## 失敗時

- `mkdocs build --strict`をローカルで再現する。
- navに登録したファイルが存在するか確認する。
- `docs/`外のsourceへ相対リンクしていないか確認する。source codeはGitHubの`blob/main` URLを使う。
- repositoryのPages sourceがGitHub Actionsになっているか確認する。
- workflowの`pages: write`と`id-token: write`がdeploy jobにあるか確認する。
