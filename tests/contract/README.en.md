# tests/contract/

[![日本語](https://img.shields.io/badge/%E3%81%82-%E6%97%A5%E6%9C%AC%E8%AA%9E-5B6670?style=for-the-badge)](README.md) [![English](https://img.shields.io/badge/A-English-087F8C?style=for-the-badge)](README.en.md)

Validates consistency between shared contracts and Industry Packs.

- `IndustryPackManifest` and every pack's `manifest.yaml`
- `MCPToolResponse` and Tool responses
- Capability Registry schema
- Columns, keys, and relationship references in synthetic demo data
- Agent instructions and production content for Copilot Studio

```bash
pytest tests/contract -q
```
