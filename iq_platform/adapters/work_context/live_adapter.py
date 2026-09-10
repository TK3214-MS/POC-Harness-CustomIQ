"""Work IQ Live Adapter (Phase 4 verification-required scaffold).

See iq_platform/adapters/live_base.py and
docs/decisions/0013-live-adapter-verification-required-scaffold.md.
"""
from __future__ import annotations

from typing import ClassVar

from iq_platform.adapters.live_base import BaseLiveAdapter


class WorkIQLiveAdapter(BaseLiveAdapter):
    adapter_name = "work_iq_live_adapter"
    settings_key = "work_iq"
    supported_operations: ClassVar[list[str]] = [
        "search_work_items",
        "search_messages",
        "search_meetings",
        "get_people_context",
        "get_project_context",
    ]
