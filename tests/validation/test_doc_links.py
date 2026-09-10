"""Validation test: repo-wide Markdown relative-link check. Wraps
scripts/validation/check_doc_links.py so link rot is caught by the normal
test suite (and CI), not just when someone remembers to run the script by
hand.
"""
from __future__ import annotations

from pathlib import Path

from iq_platform.orchestration.industry_pack_loader import load_plugin_module

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_no_broken_relative_links_in_markdown_files():
    module = load_plugin_module(REPO_ROOT / "scripts" / "validation" / "check_doc_links.py")
    broken = module.find_broken_links()
    assert broken == [], f"Broken relative links found: {broken}"
