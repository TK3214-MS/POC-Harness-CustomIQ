from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
PACKS_DIR = REPO_ROOT / "industry-packs"
PACK_IDS = (
    "manufacturing",
    "financial-services",
    "retail",
    "healthcare",
    "public-sector",
)


@pytest.mark.parametrize("pack_id", PACK_IDS)
def test_pack_has_enterprise_knowledge_corpus(pack_id: str):
    knowledge_files = list((PACKS_DIR / pack_id / "knowledge").glob("*.md"))

    assert len(knowledge_files) >= 8
    for path in knowledge_files:
        content = path.read_text(encoding="utf-8")
        assert content.startswith("# ")
        assert "synthetic" in content.lower() or "合成" in content


@pytest.mark.parametrize("pack_id", PACK_IDS)
def test_pack_has_cross_channel_work_iq_samples(pack_id: str):
    work_iq_files = list((PACKS_DIR / pack_id / "sample-data" / "work-iq").glob("*.md"))

    assert len(work_iq_files) >= 4
    corpus = "\n".join(path.read_text(encoding="utf-8") for path in work_iq_files)
    assert "SharePoint" in corpus
    assert "Teams" in corpus
    assert "Outlook" in corpus
    assert "会議" in corpus


@pytest.mark.parametrize("pack_id", PACK_IDS)
def test_agent_instructions_target_copilot_studio_and_iq_tools(pack_id: str):
    instructions = (
        PACKS_DIR / pack_id / "agents" / "investigation_agent_instructions.md"
    ).read_text(encoding="utf-8")

    for required_term in (
        "Copilot Studio",
        "Fabric IQ",
        "Foundry IQ",
        "Work IQ",
        "MCP Backend",
        "人手承認",
        "参照元",
    ):
        assert required_term in instructions