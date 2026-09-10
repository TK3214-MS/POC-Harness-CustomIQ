"""Contract tests validating every Industry Pack's manifest.yaml against the
shared IndustryPackManifest schema (instruction §22.2: '全Industry Packが同一
schemaに準拠'). Also checks that the plugin paths declared in each manifest
actually exist on disk.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from iq_platform.orchestration.industry_pack_loader import load_manifest

REPO_ROOT = Path(__file__).resolve().parents[2]
INDUSTRY_PACKS_DIR = REPO_ROOT / "industry-packs"

ALL_PACK_IDS = ["manufacturing", "financial-services", "retail", "healthcare", "public-sector"]


@pytest.mark.parametrize("pack_id", ALL_PACK_IDS)
def test_manifest_conforms_to_schema(pack_id: str):
    manifest = load_manifest(INDUSTRY_PACKS_DIR / pack_id)
    assert manifest.id == pack_id


@pytest.mark.parametrize("pack_id", ALL_PACK_IDS)
def test_manifest_plugin_and_content_paths_exist(pack_id: str):
    pack_dir = INDUSTRY_PACKS_DIR / pack_id
    manifest = load_manifest(pack_dir)
    for field_name in (
        "ontology_path",
        "semantic_model_path",
        "sample_data_path",
        "knowledge_path",
        "work_context_path",
        "mcp_tools_path",
        "semantic_relationships_path",
        "scenario_module_path",
        "agent_instructions_path",
        "demo_prompts_path",
        "expected_results_path",
        "evaluation_path",
        "terminology_path",
        "responsible_ai_path",
    ):
        path_value = getattr(manifest, field_name)
        assert (pack_dir / path_value).exists(), f"{pack_id}: {field_name}={path_value} does not exist"


@pytest.mark.parametrize("pack_id", ALL_PACK_IDS)
def test_pack_has_at_least_one_prohibited_action_or_approval_rule(pack_id: str):
    """Every pack must declare at least one guardrail (instruction §2/§8)."""
    manifest = load_manifest(INDUSTRY_PACKS_DIR / pack_id)
    assert manifest.prohibited_actions or manifest.human_approval_rules
