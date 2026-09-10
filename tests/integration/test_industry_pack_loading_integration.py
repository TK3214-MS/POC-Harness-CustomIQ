"""Integration smoke tests: every Industry Pack's plugin modules load and
expose the expected interface, independent of running a full scenario. See
instruction §22.3 (Industry Pack switching) and ADR-0010/0011.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from iq_platform.orchestration.industry_pack_loader import load_manifest, load_plugin_module

REPO_ROOT = Path(__file__).resolve().parents[2]
INDUSTRY_PACKS_DIR = REPO_ROOT / "industry-packs"

ALL_PACK_IDS = ["manufacturing", "financial-services", "retail", "healthcare", "public-sector"]


@pytest.mark.parametrize("pack_id", ALL_PACK_IDS)
def test_data_generator_plugin_interface(pack_id: str):
    pack_dir = INDUSTRY_PACKS_DIR / pack_id
    manifest = load_manifest(pack_dir)
    module = load_plugin_module(pack_dir / manifest.sample_data_path)
    assert hasattr(module, "generate_dataset")
    dataset = module.generate_dataset(seed=1, scale="demo")
    assert isinstance(dataset, dict) and dataset


@pytest.mark.parametrize("pack_id", ALL_PACK_IDS)
def test_tools_plugin_interface(pack_id: str):
    pack_dir = INDUSTRY_PACKS_DIR / pack_id
    manifest = load_manifest(pack_dir)
    module = load_plugin_module(pack_dir / manifest.mcp_tools_path)
    assert hasattr(module, "TOOL_FUNCTIONS")
    assert hasattr(module, "TOOL_DESCRIPTIONS")
    assert set(module.TOOL_FUNCTIONS.keys()) == set(module.TOOL_DESCRIPTIONS.keys())
    assert len(module.TOOL_FUNCTIONS) > 0


@pytest.mark.parametrize("pack_id", ALL_PACK_IDS)
def test_semantics_plugin_interface(pack_id: str):
    pack_dir = INDUSTRY_PACKS_DIR / pack_id
    manifest = load_manifest(pack_dir)
    module = load_plugin_module(pack_dir / manifest.semantic_relationships_path)
    assert hasattr(module, "get_relationships")
    assert hasattr(module, "get_metrics")


@pytest.mark.parametrize("pack_id", ALL_PACK_IDS)
def test_scenario_plugin_interface(pack_id: str):
    pack_dir = INDUSTRY_PACKS_DIR / pack_id
    manifest = load_manifest(pack_dir)
    module = load_plugin_module(pack_dir / manifest.scenario_module_path)
    assert hasattr(module, "run_scenario")
