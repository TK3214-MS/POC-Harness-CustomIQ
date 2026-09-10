"""Security test: synthetic data validation (instruction §23). Wraps
scripts/validation/validate_synthetic_data.py so it runs as part of the normal
test suite, not just CI.
"""
from __future__ import annotations

from pathlib import Path

from iq_platform.orchestration.industry_pack_loader import load_plugin_module

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_no_non_synthetic_data_patterns_in_industry_packs():
    module = load_plugin_module(REPO_ROOT / "scripts" / "validation" / "validate_synthetic_data.py")
    findings = module.scan()
    assert findings == [], f"Possible non-synthetic data patterns found: {findings}"
