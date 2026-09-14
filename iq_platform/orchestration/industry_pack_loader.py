"""Loads an Industry Pack's manifest and dynamically imports its plugin modules
(data generator, MCP tools) by file path.

Industry Pack directories (e.g. industry-packs/manufacturing/) use kebab-case
top-level names that are not valid Python package identifiers, and are meant to
be swappable content rather than statically imported code.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import yaml

from iq_platform.contracts.manifest import IndustryPackManifest


def load_manifest(pack_dir: str | Path) -> IndustryPackManifest:
    pack_dir = Path(pack_dir)
    manifest_path = pack_dir / "manifest.yaml"
    if not manifest_path.exists():
        raise FileNotFoundError(f"No manifest.yaml found in {pack_dir}")
    with manifest_path.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle)
    return IndustryPackManifest.model_validate(raw)


def load_plugin_module(module_path: str | Path) -> ModuleType:
    """Dynamically import a single-file Industry Pack plugin module (e.g. a data
    generator or MCP tools module) by file path, without requiring it to live
    under a dotted Python package."""
    module_path = Path(module_path)
    if not module_path.exists():
        raise FileNotFoundError(f"Plugin module not found: {module_path}")
    module_name = f"iiq_industry_pack_plugin_{module_path.stem}_{abs(hash(str(module_path)))}"
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load plugin module from {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module
