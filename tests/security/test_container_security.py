"""Security test: MCP Backend container hardening (instruction §24 - never run
as root, health check present, least-privilege registry pull).
"""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DOCKERFILE_PATH = REPO_ROOT / "deployment" / "containers" / "mcp-backend" / "Dockerfile"


def test_dockerfile_exists():
    assert DOCKERFILE_PATH.exists()


def test_dockerfile_never_runs_as_root():
    text = DOCKERFILE_PATH.read_text(encoding="utf-8")
    user_directives = [line.strip() for line in text.splitlines() if line.strip().upper().startswith("USER ")]
    assert user_directives, "Dockerfile must set a non-root USER"
    assert user_directives[-1].split()[-1] != "root", f"Last USER directive must not be root: {user_directives}"


def test_dockerfile_has_healthcheck():
    text = DOCKERFILE_PATH.read_text(encoding="utf-8")
    assert "HEALTHCHECK" in text


def test_bicep_registry_uses_managed_identity_not_admin_user():
    resources_bicep = (REPO_ROOT / "deployment" / "bicep" / "resources.bicep").read_text(encoding="utf-8")
    assert "adminUserEnabled: false" in resources_bicep
