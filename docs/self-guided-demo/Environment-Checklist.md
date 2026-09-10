# Environment Checklist（開始前チェックリスト）

デモ開始前に、以下を上から順に実行して確認してください。

```bash
cd <このリポジトリのルート>
source .venv/bin/activate
```

- [ ] `python3 --version` が 3.11 以上
- [ ] `pip show fastapi pydantic pyyaml uvicorn azure-identity` が全てエラーなく表示される（未インストールなら `pip install -e ".[dev]"`）
- [ ] `ruff check .` が `All checks passed!` を返す
- [ ] `pytest tests/ -v` が全件成功する
- [ ] `./scripts/demo/run-demo-cli.sh health` が実行でき、以下が表示される
  - `Industry Pack: Manufacturing - Ready`
  - `Work IQ (simulated): Ready` / `Foundry IQ (mock): Ready` / `Fabric IQ (mock): Ready`
  - `MCP Backend: Ready (mock)`
  - Live Adapters セクションで `unavailable`（認証情報未設定の場合、これが正常な状態です）
- [ ] `./scripts/demo/run-demo-cli.sh validate` が5業界すべて `OK` を返す
- [ ] `python3 scripts/security/scan_secrets.py` が `No secret patterns found` を返す
- [ ] `python3 scripts/validation/validate_synthetic_data.py` が `No denylisted names...` を返す
- [ ] 実顧客・実患者・実市民・実金融機関・実行政機関のデータが含まれていないことを確認済み（上記スキャンは補助であり保証ではない、instruction §23）
- [ ] 実行モードが Local Preview であることを認識している（Hybrid/Full SaaS ではない）

すべてチェックできたら [30-Minute-Demo-Guide.md](30-Minute-Demo-Guide.md) に進んでください。

いずれかが失敗する場合は、そのまま続行せず [Troubleshooting.md](Troubleshooting.md) を参照してください。
