"""Unit tests: Industry Pack loader (manifest + dynamic plugin loading). See
docs/decisions/0010-industry-pack-plugin-loading.md.
"""
from __future__ import annotations

import pytest

from iq_platform.orchestration.industry_pack_loader import load_manifest, load_plugin_module


def test_load_manifest_raises_for_missing_directory(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_manifest(tmp_path / "does-not-exist")


def test_load_plugin_module_raises_for_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_plugin_module(tmp_path / "missing_module.py")


def test_load_plugin_module_executes_and_returns_the_module(tmp_path):
    module_path = tmp_path / "sample_plugin.py"
    module_path.write_text("MARKER = 'loaded'\n\n\ndef greet():\n    return 'hello'\n", encoding="utf-8")

    module = load_plugin_module(module_path)
    assert module.MARKER == "loaded"
    assert module.greet() == "hello"


def test_load_plugin_module_does_not_collide_across_same_named_files(tmp_path):
    """Two different Industry Packs each having e.g. a generator.py must not
    clobber each other's loaded module in sys.modules."""
    pack_a = tmp_path / "pack_a"
    pack_b = tmp_path / "pack_b"
    pack_a.mkdir()
    pack_b.mkdir()
    (pack_a / "generator.py").write_text("VALUE = 'a'\n", encoding="utf-8")
    (pack_b / "generator.py").write_text("VALUE = 'b'\n", encoding="utf-8")

    module_a = load_plugin_module(pack_a / "generator.py")
    module_b = load_plugin_module(pack_b / "generator.py")
    assert module_a.VALUE == "a"
    assert module_b.VALUE == "b"
