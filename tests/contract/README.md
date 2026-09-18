# tests/contract/

[![日本語](https://img.shields.io/badge/%E3%81%82-%E6%97%A5%E6%9C%AC%E8%AA%9E-087F8C?style=for-the-badge)](README.md) [![English](https://img.shields.io/badge/A-English-5B6670?style=for-the-badge)](README.en.md)

共有契約とIndustry Pack間の整合性を検証します。

- `IndustryPackManifest`と全packの`manifest.yaml`
- `MCPToolResponse`とTool response
- Capability Registry schema
- 合成demo dataの列、key、relationship参照
- Copilot Studio向けagent instructionとproduction content

```bash
pytest tests/contract -q
```
