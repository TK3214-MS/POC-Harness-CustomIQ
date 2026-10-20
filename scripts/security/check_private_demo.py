#!/usr/bin/env python3
"""Reject private demo paths and known private blobs before commit or push."""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PRIVATE_DIRS = ("nissan-iq-demo", "tests/contract/nissan_iq")


def git(*args: str) -> bytes:
    return subprocess.run(
        ["git", "-C", str(REPO_ROOT), *args], capture_output=True, check=True
    ).stdout


def is_private_path(path: str) -> bool:
    parts = path.replace("\\", "/").casefold().split("/")
    return "nissan-iq-demo" in parts or "nissan_iq" in parts


def private_blobs() -> set[str]:
    algorithm = git("rev-parse", "--show-object-format").decode().strip()
    cache = REPO_ROOT / os.fsdecode(git("rev-parse", "--git-path", "private-demo-blobs").strip())
    known = set(cache.read_text(encoding="ascii").splitlines()) if cache.exists() else set()
    length = hashlib.new(algorithm).digest_size * 2
    if any(re.fullmatch(rf"[0-9a-f]{{{length}}}", oid) is None for oid in known):
        raise ValueError(f"Invalid private blob cache: {cache}")
    current: set[str] = set()
    for directory in PRIVATE_DIRS:
        base = REPO_ROOT / directory
        if base.is_symlink():
            raise ValueError(f"Private directory must not be a symlink: {directory}")
        if not base.exists():
            continue
        for parent, directories, filenames in os.walk(base, onerror=raise_walk_error):
            links = [name for name in directories if (Path(parent) / name).is_symlink()]
            for name in filenames + links:
                path = Path(parent) / name
                content = os.fsencode(os.readlink(path)) if path.is_symlink() else path.read_bytes()
                digest = hashlib.new(algorithm)
                digest.update(f"blob {len(content)}\0".encode())
                digest.update(content)
                current.add(digest.hexdigest())
    # Keep fingerprints after the original files are moved or deleted; never store their contents.
    if current - known:
        with cache.open("a", encoding="ascii") as handle:
            handle.write("".join(f"{oid}\n" for oid in sorted(current - known)))
    return known | current


def raise_walk_error(error: OSError) -> None:
    raise error


def inspect_entries(raw: bytes, known: set[str], context: str) -> list[str]:
    findings = []
    for entry in raw.split(b"\0"):
        if not entry:
            continue
        metadata, name = entry.split(b"\t", 1)
        oid = metadata.split()[1].decode() if context == "index" else metadata.split()[2].decode()
        path = os.fsdecode(name)
        if is_private_path(path):
            findings.append(f"{context}: private path: {path}")
        elif oid in known:
            findings.append(f"{context}: copy of private content: {path}")
    return findings


def inspect_history(refs: list[str], known: set[str]) -> list[str]:
    commits = [
        git("rev-parse", "--verify", "--end-of-options", f"{ref}^{{commit}}").decode().strip()
        for ref in refs
    ]
    if not commits:
        return []
    for commit in git("rev-list", *commits).decode().splitlines():
        findings = inspect_entries(git("ls-tree", "-r", "-z", commit), known, commit[:12])
        if findings:
            return findings
    return []


def inspect_push(lines: list[str], known: set[str]) -> list[str]:
    refs = []
    for line in lines:
        fields = line.split()
        if len(fields) != 4:
            raise ValueError("Malformed pre-push input")
        _, local_oid, remote_ref, _ = fields
        if re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", local_oid) is None:
            raise ValueError("Invalid push object ID")
        if set(local_oid) == {"0"}:
            continue
        if not remote_ref.startswith(("refs/heads/", "refs/tags/")):
            return [f"Push of non-branch/tag ref is forbidden: {remote_ref}"]
        refs.append(local_oid)
    return inspect_history(refs, known)


def install_hooks() -> None:
    existing = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "config", "--get", "core.hooksPath"],
        capture_output=True, text=True, check=False,
    )
    if existing.returncode not in (0, 1):
        raise ValueError(f"Cannot read core.hooksPath: {existing.stderr.strip()}")
    if existing.returncode == 0 and existing.stdout.strip() != ".githooks":
        raise ValueError("Existing core.hooksPath differs; integrate the hooks manually before proceeding")
    hooks_dir = REPO_ROOT / os.fsdecode(git("rev-parse", "--git-path", "hooks").strip())
    if not existing.stdout.strip() and hooks_dir.exists():
        active = [path.name for path in hooks_dir.iterdir() if path.is_file()
                  and not path.name.endswith(".sample") and os.access(path, os.X_OK)]
        if active:
            raise ValueError(f"Existing hooks must be integrated first: {', '.join(sorted(active))}")
    for name in ("pre-commit", "pre-push"):
        hook = REPO_ROOT / ".githooks" / name
        hook.chmod(hook.stat().st_mode | 0o111)
    private_blobs()
    git("config", "--local", "core.hooksPath", ".githooks")
    print("Installed pre-commit/pre-push guards (core.hooksPath=.githooks).")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--install", action="store_true")
    mode.add_argument("--staged", action="store_true")
    mode.add_argument("--pre-push", action="store_true")
    mode.add_argument("--history", nargs="+", metavar="REF")
    args = parser.parse_args()
    try:
        if args.install:
            install_hooks()
            return 0
        known = private_blobs()
        if args.staged:
            findings = inspect_entries(git("ls-files", "--stage", "-z"), known, "index")
        elif args.pre_push:
            findings = inspect_push(sys.stdin.read().splitlines(), known)
        else:
            findings = inspect_history(args.history, known)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"Private demo guard failed; operation refused: {error}", file=sys.stderr)
        if isinstance(error, subprocess.CalledProcessError) and error.stderr:
            print(os.fsdecode(error.stderr).strip(), file=sys.stderr)
        return 1
    if findings:
        print("Private demo material detected; operation refused:", file=sys.stderr)
        for finding in findings[:20]:
            print(f"  {finding}", file=sys.stderr)
        return 1
    print("Private demo guard passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
