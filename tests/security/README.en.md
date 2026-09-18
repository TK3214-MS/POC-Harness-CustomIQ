# tests/security/

[![日本語](https://img.shields.io/badge/%E3%81%82-%E6%97%A5%E6%9C%AC%E8%AA%9E-5B6670?style=for-the-badge)](README.md) [![English](https://img.shields.io/badge/A-English-087F8C?style=for-the-badge)](README.en.md)

Secret scanning, dependency pinning validation, container security (non-root/HEALTHCHECK/ACR admin disabled), MCP Tool allowlists, prevention of secret leakage in logs, synthetic data validation, and more (instruction §22.5).

**Status: Implemented.** Dependency vulnerability scanning (such as pip-audit) and prompt injection tests are not implemented. Verify the security settings for the MCP Backend and SaaS side before production deployment.
