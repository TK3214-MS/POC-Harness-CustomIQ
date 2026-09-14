#!/usr/bin/env python3
"""Synthetic data validation scanner (instruction §23).

Scans Industry Pack data assets (data generators, sample data, knowledge
documents, and work context fixtures) for patterns that would indicate real company names, real
person names, real contact info, or non-synthetic identifiers slipped in.
This is a heuristic denylist/pattern scan, NOT a guarantee of "fully
synthetic" - combine with manual review per instruction §23.

Usage:
    python3 scripts/validation/validate_synthetic_data.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
INDUSTRY_PACKS_DIR = REPO_ROOT / "industry-packs"

# Known-name denylist: real company/brand names that must never appear in
# synthetic sample data. Extend this list as new packs/entities are added.
_DENYLIST_TERMS = [
    "Microsoft",
    "Amazon",
    "Google",
    "Apple Inc",
    "Walmart",
    "Toyota",
    "JPMorgan",
    "Goldman Sachs",
    "Mayo Clinic",
    "Cleveland Clinic",
]

_EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
_ALLOWED_EMAIL_DOMAINS = {"example.com", "example.org", "example.net"}
_PHONE_PATTERN = re.compile(r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b")
_SSN_LIKE_PATTERN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")

_SCAN_EXTENSIONS = {".py", ".md", ".json", ".yaml", ".yml"}
_DATA_DIRECTORIES = {"data", "knowledge", "sample-data", "work-context"}


def _iter_pack_files():
    for pack_dir in INDUSTRY_PACKS_DIR.iterdir():
        if not pack_dir.is_dir():
            continue
        for directory_name in _DATA_DIRECTORIES:
            data_dir = pack_dir / directory_name
            if not data_dir.exists():
                continue
            for path in data_dir.rglob("*"):
                if path.is_file() and path.suffix in _SCAN_EXTENSIONS:
                    yield path


def scan() -> list[str]:
    findings: list[str] = []
    for path in _iter_pack_files():
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        rel = path.relative_to(REPO_ROOT)

        for term in _DENYLIST_TERMS:
            if term.lower() in text.lower():
                findings.append(f"{rel}: possible real company/brand name '{term}'")

        for match in _EMAIL_PATTERN.finditer(text):
            domain = match.group(0).split("@", 1)[1].lower()
            if domain not in _ALLOWED_EMAIL_DOMAINS:
                findings.append(f"{rel}: email with non-reserved domain '{match.group(0)}'")

        for match in _PHONE_PATTERN.finditer(text):
            findings.append(f"{rel}: possible real-looking phone number '{match.group(0)}'")

        for match in _SSN_LIKE_PATTERN.finditer(text):
            findings.append(f"{rel}: SSN-like identifier pattern '{match.group(0)}'")

    return findings


def main() -> int:
    if not INDUSTRY_PACKS_DIR.exists():
        print(f"No industry-packs directory found at {INDUSTRY_PACKS_DIR}")
        return 0

    findings = scan()
    if findings:
        print(f"Found {len(findings)} possible non-synthetic data pattern(s):")
        for finding in findings:
            print(f"  - {finding}")
        print()
        print("This is a heuristic scan only - also perform the manual review checklist (instruction section 23).")
        return 1

    print("No denylisted names, non-reserved email domains, or PII-like patterns found.")
    print("This is a heuristic scan only - it does not guarantee data is fully synthetic (instruction section 23).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
