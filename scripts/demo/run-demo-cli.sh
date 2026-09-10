#!/usr/bin/env bash
# Convenience launcher for the Demo CLI (apps/demo-cli/demo_cli/cli.py) without
# requiring it to be pip-installed. See docs/decisions/0009 and 0010 for why
# Industry Pack / app code isn't statically packaged in Phase 2.
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
export PYTHONPATH="${REPO_ROOT}:${REPO_ROOT}/apps/demo-cli:${REPO_ROOT}/services/mcp-backend:${PYTHONPATH:-}"
exec python3 -m demo_cli.cli "$@"
