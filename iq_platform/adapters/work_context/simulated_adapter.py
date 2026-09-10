"""Simulated Work IQ Adapter - reads synthetic work-context fixtures from an
Industry Pack. Never connects to real Microsoft 365 data. See instruction §5.2.
"""
from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from iq_platform.contracts.adapter import (
    Adapter,
    AdapterCapabilities,
    AdapterDiagnostics,
    AdapterHealth,
)
from iq_platform.contracts.capability import AdapterMode

_SUPPORTED_OPERATIONS = ["search_messages", "search_meetings", "search_work_items", "get_people_context"]


class SimulatedWorkContextAdapter(Adapter):
    def __init__(self, fixtures_path: str | Path):
        self._fixtures_path = Path(fixtures_path)
        self._fixtures: dict[str, Any] = {}
        if self._fixtures_path.exists():
            with self._fixtures_path.open("r", encoding="utf-8") as handle:
                self._fixtures = json.load(handle)

    def health_check(self) -> AdapterHealth:
        healthy = self._fixtures_path.exists()
        return AdapterHealth(
            healthy=healthy,
            mode=self.mode,
            message=(
                "Simulated Work IQ fixtures loaded"
                if healthy
                else f"Fixtures not found at {self._fixtures_path}"
            ),
            checked_at=datetime.now(UTC),
        )

    def capabilities(self) -> AdapterCapabilities:
        return AdapterCapabilities(
            adapter_name="simulated_work_context_adapter",
            supported_operations=_SUPPORTED_OPERATIONS,
            mode=self.mode,
        )

    @property
    def mode(self) -> AdapterMode:
        return AdapterMode.SIMULATED

    def query(self, operation: str, parameters: dict[str, Any]) -> dict[str, Any]:
        if operation == "get_people_context":
            return {"results": self._fixtures.get("people", [])}
        if operation not in _SUPPORTED_OPERATIONS:
            return {"error": f"Unsupported operation '{operation}'", "results": []}

        items = self._fixtures.get("messages" if operation != "search_meetings" else "meetings", [])
        keywords = [k.lower() for k in parameters.get("keywords", [])]
        if not keywords:
            matches = items
        else:
            matches = [
                item
                for item in items
                if any(kw in " ".join(item.get("tags", [])).lower() or kw in str(item).lower() for kw in keywords)
            ]
        return {"results": matches}

    def validate_configuration(self) -> AdapterDiagnostics:
        missing = [] if self._fixtures_path.exists() else [f"fixtures file: {self._fixtures_path}"]
        return AdapterDiagnostics(
            adapter_name="simulated_work_context_adapter",
            mode=self.mode,
            configuration_valid=not missing,
            missing_configuration=missing,
        )

    def get_diagnostics(self) -> AdapterDiagnostics:
        return self.validate_configuration()
