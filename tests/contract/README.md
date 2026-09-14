# tests/contract/

共有契約とIndustry Pack間の整合性を検証します。

- `IndustryPackManifest`と全packの`manifest.yaml`
- `MCPToolResponse`とTool response
- Capability Registry schema
- 合成demo dataの列、key、relationship参照
- Copilot Studio向けagent instructionとproduction content

```bash
pytest tests/contract -q
```
