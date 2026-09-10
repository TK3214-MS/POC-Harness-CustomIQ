"""Foundry IQ Live Adapter (Phase 4 verification-required scaffold).

See iq_platform/adapters/live_base.py and
docs/decisions/0013-live-adapter-verification-required-scaffold.md.
"""
from __future__ import annotations

from typing import ClassVar

from iq_platform.adapters.live_base import BaseLiveAdapter


class FoundryIQLiveAdapter(BaseLiveAdapter):
    adapter_name = "foundry_iq_live_adapter"
    settings_key = "foundry_iq"
    supported_operations: ClassVar[list[str]] = [
        "search_knowledge",
        "get_document",
        "get_citations",
        "evaluate_retrieval",
        "list_knowledge_bases",
    ]
