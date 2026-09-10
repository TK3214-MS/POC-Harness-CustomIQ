"""Unit test: Mock Foundry IQ Adapter's application_confidence calculation
(instruction §5.3 - accelerator-derived, not a native Microsoft score).
"""
from __future__ import annotations

from iq_platform.adapters.knowledge.mock_adapter import MockKnowledgeAdapter


def test_application_confidence_is_zero_when_no_results_match(tmp_path):
    knowledge_dir = tmp_path / "knowledge"
    knowledge_dir.mkdir()
    (knowledge_dir / "doc_one.md").write_text("This document is about widgets.", encoding="utf-8")

    adapter = MockKnowledgeAdapter(knowledge_dir)
    result = adapter.query("search_knowledge", {"query": "completely unrelated topic xyz"})
    assert result["results"] == []
    assert result["application_confidence"] == 0.0


def test_application_confidence_increases_with_more_matching_documents(tmp_path):
    knowledge_dir = tmp_path / "knowledge"
    knowledge_dir.mkdir()
    (knowledge_dir / "doc_one.md").write_text("widgets widgets widgets are great widgets", encoding="utf-8")
    (knowledge_dir / "doc_two.md").write_text("a brief mention of widgets", encoding="utf-8")

    adapter = MockKnowledgeAdapter(knowledge_dir)
    result = adapter.query("search_knowledge", {"query": "widgets"})
    assert len(result["results"]) == 2
    assert 0.0 < result["application_confidence"] <= 1.0
    # Every result must disclose its adapter_mode alongside the score.
    assert all(r["adapter_mode"] == "mock" for r in result["results"])
