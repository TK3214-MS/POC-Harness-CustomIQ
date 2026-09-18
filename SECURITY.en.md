# Security Policy

[![日本語](https://img.shields.io/badge/%E3%81%82-%E6%97%A5%E6%9C%AC%E8%AA%9E-5B6670?style=for-the-badge)](SECURITY.md) [![English](https://img.shields.io/badge/A-English-087F8C?style=for-the-badge)](SECURITY.en.md)

## Baseline Policy (Currently Confirmed Scope)

- Do not store secrets in source code or the repository. `.env` is listed in `.gitignore`, and `.env.example` contains only fictitious values.
- For production-like use, use a secret store such as Azure Key Vault.
- Do not automatically execute instructions found in retrieved documents. A dedicated prompt-injection test suite has not been implemented.
- Destructive or high-impact operations must follow the approval policy of the customer's business system and the MCP Tool human-approval rules.

## Reporting a Vulnerability

This accelerator is still under development and has not been released publicly. If you discover a vulnerability, contact the repository administrator directly instead of opening an issue.

## Security Controls Currently Implemented

The following controls are implemented in this repository and can be verified in the codebase. Only implemented controls are listed here so they remain distinct from aspirational or planned controls.

- **Secret commit prevention**: `.env` is listed in `.gitignore`, and `.env.example` contains only placeholders and fictitious values.
- **Heuristic secret scanning**: `scripts/security/scan_secrets.py` detects strings that resemble secrets with regular expressions and runs in the `lint-and-test` CI job in `.github/workflows/ci.yml`.
- **Synthetic-data-only validation**: `scripts/validation/validate_synthetic_data.py` heuristically checks Industry Pack content for denylisted real names and email, telephone, and SSN-like patterns. It runs in CI.
- **Non-root container execution**: The MCP Backend container image ([deployment/containers/mcp-backend/Dockerfile](deployment/containers/mcp-backend/Dockerfile)) runs as the non-root `iiq` user (UID 1000) and defines a `HEALTHCHECK` instruction.
- **Least-privilege ACR configuration**: Azure Container Registry has its admin user disabled and grants only AcrPull to a user-assigned managed identity ([deployment/bicep/resources.bicep](deployment/bicep/resources.bicep)).
- **Bounded dependency versions**: [pyproject.toml](pyproject.toml) uses major-version bounds such as `pydantic>=2.6,<3`, `fastapi>=0.115,<1`, and `azure-identity>=1.19,<2`. The container image's `services/mcp-backend/requirements.txt` contains runtime dependencies only and excludes development tools such as pytest and Ruff.
- **MCP Tool allowlist**: The comma-separated `MCP_BACKEND_ALLOWED_TOOLS` environment variable explicitly limits the Tools exposed by the MCP Backend. Unapproved Tool names are rejected with a structured error (`services/mcp-backend/mcp_backend/registry.py`).

## Security Controls Not Yet Implemented

The following items are not currently implemented and require separate work before production-like use.

- **MCP Backend request authentication**: `MCP_BACKEND_API_KEY` exists as a placeholder in `.env.example`, but neither API-key nor OAuth request authentication is integrated into middleware.
- **Dependency vulnerability scanning**: Automated vulnerability scanning such as `pip-audit` or Dependabot is not configured.
- **Prompt-injection test suite**: No dedicated tests exercise intentional attack scenarios. The design rule against automatically executing instructions in retrieved documents is represented in code, but automated tests do not yet validate it.
- **Governance-tool integration such as Microsoft Purview or DLP**: External integration for data classification, DLP policy enforcement, and audit trails is not implemented.

Confirm these items for each environment before production deployment.

For MCP Backend-specific implementation and pre-publication checks, see the [MCP Security Guide](docs/mcp/MCP-Security-Guide.en.md).
