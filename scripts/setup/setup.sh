#!/usr/bin/env bash
# One-shot environment bootstrap for local development (instruction §28 `setup`).
# Safe to re-run (idempotent): creates .venv only if missing, always reinstalls
# the package in editable mode so dependency changes are picked up.
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

PYTHON_BIN="${PYTHON_BIN:-python3}"

if ! "$PYTHON_BIN" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)' 2>/dev/null; then
  echo "Error: $PYTHON_BIN is older than the required Python 3.11+."
  echo "Set PYTHON_BIN to a newer interpreter, e.g.:"
  echo "  PYTHON_BIN=/opt/homebrew/bin/python3.12 ./scripts/setup/setup.sh"
  exit 1
fi

if [ ! -d .venv ]; then
  echo "Creating virtual environment (.venv) with $PYTHON_BIN..."
  "$PYTHON_BIN" -m venv .venv
else
  echo ".venv already exists, reusing it."
fi

# shellcheck disable=SC1091
source .venv/bin/activate

echo "Installing project (editable) with dev extras..."
pip install --upgrade pip -q
pip install -e ".[dev]" -q

echo "Running lint and contract+unit test suite to confirm the environment is healthy..."
ruff check .
pytest tests/ -q

echo
echo "Setup complete. Activate the environment in new shells with:"
echo "  source .venv/bin/activate"
echo "Then try:"
echo "  ./scripts/demo/run-demo-cli.sh health"
