#!/usr/bin/env python3
"""Lightweight, offline secret-pattern scanner (instruction §22.5 / §24).

Scans tracked source files for patterns that commonly indicate a leaked
secret (API keys, private key headers, connection strings with embedded
keys, etc.). This is a heuristic safety net, NOT a replacement for a real
secret-scanning service - false negatives are expected for novel secret
formats. Exits non-zero if any match is found.

Usage:
    python3 scripts/security/scan_secrets.py
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

_EXCLUDED_DIR_PARTS = {".git", ".venv", "__pycache__", ".pytest_cache", ".ruff_cache", "node_modules"}
_EXCLUDED_FILENAMES = {"scan_secrets.py"}  # this file legitimately contains the patterns below

_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("AWS Access Key ID", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("Generic private key header", re.compile(r"-----BEGIN (RSA |EC |OPENSSH |)PRIVATE KEY-----")),
    ("Azure Storage connection string with AccountKey", re.compile(r"AccountKey=[A-Za-z0-9+/=]{20,}")),
    ("Slack token", re.compile(r"xox[baprs]-[0-9A-Za-z-]{10,}")),
    ("Generic 'apikey=' assignment with a long value", re.compile(r"(?i)api[_-]?key\s*[:=]\s*['\"][A-Za-z0-9_\-]{20,}['\"]")),
    ("Hardcoded password assignment with a non-placeholder value", re.compile(r"(?i)password\s*=\s*['\"](?!changeme|placeholder|example|synthetic)[^'\"\s]{8,}['\"]")),
]


def _tracked_files() -> list[Path]:
    """Tracked + untracked-but-not-gitignored files, so the scan is useful even
    before anything has been committed. Falls back to a plain filesystem walk
    if git is unavailable or unusable in the current environment (e.g. no git
    installed, or restricted sandbox), so the scan still runs somewhere."""
    try:
        result = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "ls-files", "--cached", "--others", "--exclude-standard"],
            capture_output=True,
            text=True,
            check=True,
        )
        return [REPO_ROOT / line for line in result.stdout.splitlines() if line]
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return [
            path
            for path in REPO_ROOT.rglob("*")
            if path.is_file() and not any(part in _EXCLUDED_DIR_PARTS for part in path.relative_to(REPO_ROOT).parts)
        ]


def _is_excluded(path: Path) -> bool:
    if path.name in _EXCLUDED_FILENAMES:
        return True
    return any(part in _EXCLUDED_DIR_PARTS for part in path.parts)


def scan() -> list[str]:
    findings: list[str] = []
    for path in _tracked_files():
        if _is_excluded(path) or not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for label, pattern in _PATTERNS:
            for match in pattern.finditer(text):
                line_number = text.count("\n", 0, match.start()) + 1
                findings.append(f"{path.relative_to(REPO_ROOT)}:{line_number}: possible {label}")
    return findings


def main() -> int:
    findings = scan()
    if findings:
        print(f"Found {len(findings)} possible secret(s):")
        for finding in findings:
            print(f"  - {finding}")
        return 1
    print("No secret patterns found (heuristic scan only - not a guarantee).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
