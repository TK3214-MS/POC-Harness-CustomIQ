"""Fabric IQ Live Adapter (Phase 4 verification-required scaffold).

See iq_platform/adapters/live_base.py and
docs/decisions/0013-live-adapter-verification-required-scaffold.md.
"""
from __future__ import annotations

from typing import ClassVar

from iq_platform.adapters.live_base import BaseLiveAdapter


class FabricIQLiveAdapter(BaseLiveAdapter):
    adapter_name = "fabric_iq_live_adapter"
    settings_key = "fabric_iq"
    supported_operations: ClassVar[list[str]] = [
        "list_entity_types",
        "search_entities",
        "get_entity",
        "get_relationships",
        "query_semantic_model",
        "get_metrics",
    ]
