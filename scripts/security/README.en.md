# scripts/security/

[![日本語](https://img.shields.io/badge/%E3%81%82-%E6%97%A5%E6%9C%AC%E8%AA%9E-5B6670?style=for-the-badge)](README.md) [![English](https://img.shields.io/badge/A-English-087F8C?style=for-the-badge)](README.en.md)

Contains scripts for security validation, such as secret scanning.

**Implemented:** [scan_secrets.py](scan_secrets.py) is a heuristic, regular-expression-based secret detection script that runs in CI.

**Not implemented:** Dependency vulnerability scanning and dedicated prompt injection tests. Ruff runs static analysis in CI.
