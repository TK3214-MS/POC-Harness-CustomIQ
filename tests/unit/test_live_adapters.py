"""Unit tests for Live Adapter scaffolds (Phase 4). See
docs/decisions/0013-live-adapter-verification-required-scaffold.md.

These tests never make real network calls - Entra ID token acquisition is
monkeypatched.
"""
from __future__ import annotations

import pytest
from azure.core.credentials import AccessToken
from azure.core.exceptions import ClientAuthenticationError
from azure.identity import ClientSecretCredential

from iq_platform.adapters.errors import LiveAdapterNotYetVerifiedError
from iq_platform.adapters.knowledge.live_adapter import FoundryIQLiveAdapter
from iq_platform.adapters.semantic.live_adapter import FabricIQLiveAdapter
from iq_platform.adapters.work_context.live_adapter import WorkIQLiveAdapter
from iq_platform.configuration.settings import LiveAdapterSettings
from iq_platform.contracts.capability import AdapterMode


def _settings(**overrides) -> LiveAdapterSettings:
    base = {
        "entra_tenant_id": "11111111-1111-1111-1111-111111111111",
        "entra_client_id": "22222222-2222-2222-2222-222222222222",
        "entra_client_secret": "fake-secret-value",
    }
    base.update(overrides)
    return LiveAdapterSettings(**base)


@pytest.mark.parametrize(
    "adapter_cls,required_field",
    [
        (WorkIQLiveAdapter, "WORK_IQ_WORKSPACE_ID"),
        (FoundryIQLiveAdapter, "FOUNDRY_IQ_PROJECT_ENDPOINT"),
        (FabricIQLiveAdapter, "FABRIC_WORKSPACE_ID"),
    ],
)
def test_missing_configuration_yields_unavailable_mode(adapter_cls, required_field):
    settings = _settings()  # Entra ID present, but product-specific field missing
    adapter = adapter_cls(settings)
    assert adapter.mode == AdapterMode.UNAVAILABLE

    diagnostics = adapter.validate_configuration()
    assert not diagnostics.configuration_valid
    assert required_field in diagnostics.missing_configuration

    health = adapter.health_check()
    assert health.healthy is False
    assert "Missing required configuration" in health.message


@pytest.mark.parametrize(
    "adapter_cls,extra_fields",
    [
        (WorkIQLiveAdapter, {"work_iq_workspace_id": "ws-1"}),
        (
            FoundryIQLiveAdapter,
            {"foundry_iq_project_endpoint": "https://example.com", "foundry_iq_knowledge_base_id": "kb-1"},
        ),
        (FabricIQLiveAdapter, {"fabric_workspace_id": "fw-1", "fabric_ontology_id": "onto-1"}),
    ],
)
def test_full_configuration_yields_verification_required_mode_never_live(adapter_cls, extra_fields):
    settings = _settings(**extra_fields)
    adapter = adapter_cls(settings)
    assert adapter.mode == AdapterMode.VERIFICATION_REQUIRED

    diagnostics = adapter.validate_configuration()
    assert diagnostics.configuration_valid

    # Auth scope still the TBD placeholder (unset) by default -> health check
    # must say so rather than attempting a call with a guessed scope.
    health = adapter.health_check()
    assert health.healthy is False
    assert "OAuth scope" in health.message


def test_health_check_reports_successful_auth_when_scope_configured_and_token_acquired(monkeypatch):
    settings = _settings(work_iq_workspace_id="ws-1", work_iq_auth_scope="https://example.com/.default")
    adapter = WorkIQLiveAdapter(settings)

    def fake_get_token(self, *scopes, **kwargs):
        return AccessToken("fake-token", 9999999999)

    monkeypatch.setattr(ClientSecretCredential, "get_token", fake_get_token)

    health = adapter.health_check()
    assert health.healthy is False  # never healthy - the product API contract is still unverified
    assert "authentication succeeded" in health.message


def test_health_check_reports_auth_failure_clearly(monkeypatch):
    settings = _settings(work_iq_workspace_id="ws-1", work_iq_auth_scope="https://example.com/.default")
    adapter = WorkIQLiveAdapter(settings)

    def fake_get_token(self, *scopes, **kwargs):
        raise ClientAuthenticationError(message="invalid_client")

    monkeypatch.setattr(ClientSecretCredential, "get_token", fake_get_token)

    health = adapter.health_check()
    assert health.healthy is False
    assert "authentication failed" in health.message.lower()


def test_query_always_raises_not_yet_verified():
    settings = _settings(work_iq_workspace_id="ws-1")
    adapter = WorkIQLiveAdapter(settings)
    with pytest.raises(LiveAdapterNotYetVerifiedError):
        adapter.query("search_work_items", {})


def test_capabilities_reflect_current_mode():
    settings = _settings()
    adapter = WorkIQLiveAdapter(settings)
    caps = adapter.capabilities()
    assert caps.mode == AdapterMode.UNAVAILABLE
    assert "search_work_items" in caps.supported_operations
