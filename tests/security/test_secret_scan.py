"""Security test: repo-wide secret scan (instruction §22.5). Wraps
scripts/security/scan_secrets.py so it runs as part of the normal test suite,
not just CI.
"""
from __future__ import annotations

from pathlib import Path

from iq_platform.orchestration.industry_pack_loader import load_plugin_module

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_no_secret_patterns_in_repository():
    module = load_plugin_module(REPO_ROOT / "scripts" / "security" / "scan_secrets.py")
    findings = module.scan()
    assert findings == [], f"Possible secrets found: {findings}"
