"""Contract tests for iq_platform.contracts.adapter.Adapter.

See docs/decisions/0003-adapter-contract-and-mode-enum.md.
"""
from __future__ import annotations

from datetime import UTC, datetime

import pytest

from iq_platform.contracts.adapter import (
    Adapter,
    AdapterCapabilities,
    AdapterDiagnostics,
    AdapterHealth,
)
from iq_platform.contracts.capability import AdapterMode


class _FakeAdapter(Adapter):
    """Minimal concrete Adapter used only to exercise the contract in tests."""

    def health_check(self) -> AdapterHealth:
        return AdapterHealth(
            healthy=True, mode=AdapterMode.MOCK, message="ok", checked_at=datetime.now(UTC)
        )

    def capabilities(self) -> AdapterCapabilities:
        return AdapterCapabilities(
            adapter_name="fake", supported_operations=["search_knowledge"], mode=AdapterMode.MOCK
        )

    @property
    def mode(self) -> AdapterMode:
        return AdapterMode.MOCK

    def query(self, operation: str, parameters: dict) -> dict:
        return {"operation": operation, "parameters": parameters}

    def validate_configuration(self) -> AdapterDiagnostics:
        return AdapterDiagnostics(adapter_name="fake", mode=AdapterMode.MOCK, configuration_valid=True)

    def get_diagnostics(self) -> AdapterDiagnostics:
        return AdapterDiagnostics(adapter_name="fake", mode=AdapterMode.MOCK, configuration_valid=True)


def test_concrete_adapter_can_be_instantiated_and_used():
    adapter = _FakeAdapter()
    assert adapter.mode == AdapterMode.MOCK
    assert adapter.health_check().healthy is True
    assert adapter.query("search_knowledge", {"q": "test"}) == {
        "operation": "search_knowledge",
        "parameters": {"q": "test"},
    }


def test_incomplete_adapter_cannot_be_instantiated():
    class _IncompleteAdapter(Adapter):
        def health_check(self):  # only one of six abstract methods implemented
            ...

    with pytest.raises(TypeError):
        _IncompleteAdapter()
