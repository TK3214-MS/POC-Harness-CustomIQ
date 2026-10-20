from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]


def command(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ, GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
               GIT_TERMINAL_PROMPT="0")
    return subprocess.run(args, cwd=repo, env=env, capture_output=True, text=True, check=check)


def git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return command(repo, "git", *args, check=check)


def guard(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return command(repo, sys.executable, "scripts/security/check_private_demo.py", *args, check=check)


def write(repo: Path, name: str, content: str) -> Path:
    path = repo / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    root = tmp_path / "source"
    root.mkdir()
    git(root, "init", "-b", "main")
    git(root, "config", "user.name", "Guard Test")
    git(root, "config", "user.email", "guard@example.invalid")
    git(root, "config", "commit.gpgsign", "false")
    shutil.copytree(REPO_ROOT / ".githooks", root / ".githooks")
    (root / "scripts/security").mkdir(parents=True)
    shutil.copy2(REPO_ROOT / "scripts/security/check_private_demo.py", root / "scripts/security")
    shutil.copy2(REPO_ROOT / ".gitignore", root)
    git(root, "add", ".")
    git(root, "commit", "-m", "Initial public source")
    remote = tmp_path / "remote.git"
    git(root, "init", "--bare", str(remote))
    git(root, "remote", "add", "origin", str(remote))
    guard(root, "--install")
    return root


@pytest.mark.parametrize("name", [
    "nissan-iq-demo/data/raw/example.csv",
    "nissan-iq-demo/data/raw/日本語\nデータ.csv",
    "tests/contract/nissan_iq/test_private.py",
])
def test_shared_ignore_and_force_added_commit_are_blocked(repo: Path, name: str) -> None:
    write(repo, name, "fixture-only private material\n")
    assert git(repo, "check-ignore", name).returncode == 0
    git(repo, "add", "-f", name)
    result = git(repo, "commit", "-m", "Must not commit private fixture", check=False)
    assert result.returncode != 0
    assert "private path" in result.stderr


@pytest.mark.parametrize("name", [
    "archive/nissan-iq-demo/record.csv",
    "NISSAN-IQ-DEMO/record.csv",
    "archive/nissan_iq/test_fixture.py",
])
def test_nested_and_case_variant_paths_are_blocked(repo: Path, name: str) -> None:
    write(repo, name, "fixture-only private material\n")
    git(repo, "add", "-f", name)
    result = guard(repo, "--staged", check=False)
    assert result.returncode != 0
    assert "private path" in result.stderr


def test_renamed_copy_is_blocked_even_after_original_is_removed(repo: Path) -> None:
    source = write(repo, "nissan-iq-demo/data/raw/source.csv", "unique private fixture,1234\n")
    guard(repo, "--install")
    write(repo, "renamed.csv", source.read_text(encoding="utf-8"))
    source.unlink()
    git(repo, "add", "renamed.csv")
    result = git(repo, "commit", "-m", "Must not commit renamed fixture", check=False)
    assert result.returncode != 0
    assert "copy of private content: renamed.csv" in result.stderr


def test_normal_code_commit_and_push_succeed(repo: Path) -> None:
    write(repo, "public.py", "print('public source')\n")
    git(repo, "add", "public.py")
    git(repo, "commit", "-m", "Public code")
    git(repo, "push", "origin", "main")
    assert git(repo, "rev-parse", "HEAD").stdout == git(
        repo, "ls-remote", "origin", "refs/heads/main"
    ).stdout.split()[0] + "\n"


@pytest.mark.parametrize("destination", ["main", "refs/tags/private-fixture"])
def test_push_checks_deleted_files_in_ancestor_commits(repo: Path, destination: str) -> None:
    name = "nissan-iq-demo/data/raw/private.csv"
    write(repo, name, "private history fixture\n")
    git(repo, "add", "-f", name)
    git(repo, "-c", "core.hooksPath=/dev/null", "commit", "-m", "Bypassed commit guard")
    private_commit = git(repo, "rev-parse", "HEAD").stdout.strip()
    git(repo, "rm", name)
    git(repo, "commit", "-m", "Remove private fixture from latest tree")
    if destination.startswith("refs/tags/"):
        git(repo, "tag", "-a", "private-fixture", private_commit, "-m", "Private fixture tag")
    result = git(repo, "push", "origin", destination, check=False)
    assert result.returncode != 0
    assert "private path" in result.stderr
    assert git(repo, "ls-remote", "origin").stdout == ""
    history = guard(repo, "--history", "HEAD", check=False)
    assert history.returncode != 0


def test_push_blocks_renamed_private_blob_after_commit_hook_bypass(repo: Path) -> None:
    content = "private copy fixture,9876\n"
    write(repo, "nissan-iq-demo/data/raw/private.csv", content)
    guard(repo, "--install")
    write(repo, "public-looking.csv", content)
    git(repo, "add", "public-looking.csv")
    git(repo, "-c", "core.hooksPath=/dev/null", "commit", "-m", "Bypassed commit guard")
    result = git(repo, "push", "origin", "main", check=False)
    assert result.returncode != 0
    assert "copy of private content" in result.stderr
    assert git(repo, "ls-remote", "origin").stdout == ""


def test_checkpoint_refs_cannot_be_pushed(repo: Path) -> None:
    ref = "refs/agents/fixture/checkpoints/turn/0"
    git(repo, "update-ref", ref, "HEAD")
    result = git(repo, "push", "origin", f"{ref}:{ref}", check=False)
    assert result.returncode != 0
    assert "non-branch/tag ref" in result.stderr
    assert git(repo, "ls-remote", "origin").stdout == ""


def test_non_commit_tag_is_rejected(repo: Path) -> None:
    blob = git(repo, "rev-parse", "HEAD:.gitignore").stdout.strip()
    git(repo, "tag", "blob-fixture", blob)
    result = git(repo, "push", "origin", "refs/tags/blob-fixture", check=False)
    assert result.returncode != 0
    assert "operation refused" in result.stderr
    assert git(repo, "ls-remote", "origin").stdout == ""


def test_normal_tag_and_remote_branch_deletion_succeed(repo: Path) -> None:
    git(repo, "tag", "-a", "public-fixture", "-m", "Public fixture")
    git(repo, "push", "origin", "main", "refs/tags/public-fixture")
    git(repo, "push", "origin", "--delete", "refs/tags/public-fixture")
    assert "refs/tags/public-fixture" not in git(repo, "ls-remote", "origin").stdout


def test_corrupt_fingerprint_cache_fails_closed(repo: Path) -> None:
    write(repo, ".git/private-demo-blobs", "invalid-object-id\n")
    result = guard(repo, "--staged", check=False)
    assert result.returncode != 0
    assert "Invalid private blob cache" in result.stderr


@pytest.mark.parametrize("existing", ["custom-hooks-path", "legacy-hook"])
def test_install_does_not_silently_replace_existing_hooks(repo: Path, existing: str) -> None:
    if existing == "custom-hooks-path":
        git(repo, "config", "core.hooksPath", "custom-hooks")
    else:
        git(repo, "config", "--unset", "core.hooksPath")
        hook = write(repo, ".git/hooks/pre-commit", "#!/bin/sh\nexit 1\n")
        hook.chmod(0o755)
    result = guard(repo, "--install", check=False)
    assert result.returncode != 0
    assert "Existing" in result.stderr


def test_private_demo_excluded_from_docker_context() -> None:
    patterns = (REPO_ROOT / ".dockerignore").read_text(encoding="utf-8").splitlines()
    assert "nissan-iq-demo/" in patterns
    assert "**/nissan-iq-demo/" in patterns


def test_history_ci_and_pages_checks_use_full_history() -> None:
    for name in ("ci.yml", "pages.yml"):
        workflow = (REPO_ROOT / ".github/workflows" / name).read_text(encoding="utf-8")
        assert "fetch-depth: 0" in workflow
        assert "python3 scripts/security/check_private_demo.py --history HEAD" in workflow
