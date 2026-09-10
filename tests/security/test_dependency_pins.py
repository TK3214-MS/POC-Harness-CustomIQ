"""Security test: dependency version pinning (instruction §22.5 / §24 -
dependency lock file verification). The container's runtime requirements must
be exactly pinned so builds are reproducible and auditable.
"""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_mcp_backend_runtime_requirements_are_exactly_pinned():
    requirements_path = REPO_ROOT / "services" / "mcp-backend" / "requirements.txt"
    lines = [
        line.strip()
        for line in requirements_path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    assert lines, "requirements.txt must not be empty"
    for line in lines:
        assert "==" in line, f"Dependency not exactly pinned: {line}"
