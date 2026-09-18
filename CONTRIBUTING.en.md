# Contribution Guide

[![日本語](https://img.shields.io/badge/%E3%81%82-%E6%97%A5%E6%9C%AC%E8%AA%9E-5B6670?style=for-the-badge)](CONTRIBUTING.md) [![English](https://img.shields.io/badge/A-English-087F8C?style=for-the-badge)](CONTRIBUTING.en.md)

## Development Process

1. Record major design decisions in the document being changed or near the relevant code.
2. Do not present assumptions about Microsoft product specifications, licensing, pricing, regions, or GA/Preview status as established facts. When information is unknown, explicitly write `TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION`.
3. Add unresolved matters to the applicable procedure in the [Production Environment Setup Guide](docs/Production-Environment-Setup.en.md).
4. Mock or simulated implementations must always include an indication in the code, logs, or responses that clearly identifies them as mocks.
5. Do not describe unimplemented features as complete in READMEs or other documentation.
6. Run the relevant tests before committing, and do not delete or disable failing tests to claim success.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
ruff check .
pytest
```

## Coding Conventions

- Use Python 3.11+ for all implementation code.
- Use a Python package name that does not conflict with the standard library's `platform` module.
- Use `ruff` for linting.

## Test Addition Policy

Tests in this repository are divided into five categories under `tests/`. Add or update tests in at least one of the following categories, as appropriate for the change.

- `tests/contract/` — When changing the Industry Pack Manifest, MCP Tool Response, Capability Registry, or contracts for lab data and agent instructions.
- `tests/unit/` — When changing or adding the isolated behavior of a class or function, such as the current Industry Pack loader.
- `tests/integration/` — When changing behavior that combines multiple components, such as integration between the MCP Backend and an Industry Pack.
- `tests/security/` — When changing the behavior of security-related scripts, such as secret scanning or synthetic data validation.
- `tests/validation/` — When changing repository-wide static validation, such as Markdown link checks.

When adding a new Industry Pack, add its `manifest.yaml`, `mcp_tools_path`, tool contracts, and related contract tests. See the [Production Environment Setup Guide](docs/Production-Environment-Setup.en.md) for actual usage and connection procedures.

## Pre-Submission Validation Loop

Before opening a pull request, make sure at least all of the following commands succeed locally. They are equivalent to the CI `lint-and-test` job.

```bash
ruff check .
pytest tests/ -v
python3 scripts/security/scan_secrets.py
python3 scripts/validation/validate_synthetic_data.py
```

If any command fails, do not delete or disable tests to claim success. Fix the cause of the failure or report it honestly in your response.
