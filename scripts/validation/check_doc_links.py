#!/usr/bin/env python3
"""Scan all Markdown files in the repository for relative links and verify
that every link target actually exists on disk.

Only relative links are checked (http(s)://, mailto:, and other schemes are
skipped, since those cannot be verified without network access and are out
of scope for this heuristic check). Links are resolved relative to the
directory containing the Markdown file that references them. A leading
'#' fragment (anchor) is stripped before resolution; anchors themselves are
not validated (that would require parsing heading slugs, which is out of
scope for this script).

Exit code is non-zero if any broken link is found. This is wired into CI
(.github/workflows/ci.yml, "Markdown link check" step) and also wrapped by
tests/validation/test_doc_links.py so it runs as part of the normal test
suite.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# Directories that should never be scanned for markdown or link targets.
_EXCLUDED_DIR_NAMES = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    "node_modules",
    "industry_iq_platform.egg-info",
}

_LINK_PATTERN = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def _is_excluded(path: Path) -> bool:
    return any(part in _EXCLUDED_DIR_NAMES for part in path.parts)


def _markdown_files() -> list[Path]:
    return [p for p in REPO_ROOT.rglob("*.md") if not _is_excluded(p)]


def _is_checkable_relative_link(target: str) -> bool:
    if not target:
        return False
    if target.startswith("#"):
        # Same-file anchor only; not checked (no heading-slug parsing here).
        return False
    for scheme in ("http://", "https://", "mailto:", "vscode:", "file://"):
        if target.startswith(scheme):
            return False
    return True


def find_broken_links() -> list[tuple[Path, str]]:
    broken: list[tuple[Path, str]] = []
    for md_file in _markdown_files():
        text = md_file.read_text(encoding="utf-8", errors="ignore")
        for match in _LINK_PATTERN.finditer(text):
            target = match.group(1).strip()
            if not _is_checkable_relative_link(target):
                continue
            # Strip a trailing anchor (e.g. "foo.md#section") before resolving.
            path_part = target.split("#", 1)[0]
            if not path_part:
                continue
            # Strip a title in quotes if present (e.g. "foo.md \"Title\"").
            path_part = path_part.split(" ", 1)[0]
            resolved = (md_file.parent / path_part).resolve()
            try:
                resolved.relative_to(REPO_ROOT)
            except ValueError:
                # Link escapes the repo root entirely - flag it too.
                broken.append((md_file, target))
                continue
            if not resolved.exists():
                broken.append((md_file, target))
    return broken


def main() -> int:
    broken = find_broken_links()
    if not broken:
        print("No broken relative links found in any Markdown file.")
        return 0

    print(f"Found {len(broken)} broken relative link(s):\n")
    for md_file, target in broken:
        rel = md_file.relative_to(REPO_ROOT)
        print(f"  {rel}: -> {target}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
