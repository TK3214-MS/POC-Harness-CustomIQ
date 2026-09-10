"""Security test: secrets must never leak into log-visible fields (instruction
§24 - never leave Secret/Token/PII in production logs). Verifies that a fake
Entra ID client secret never appears in AdapterHealth/AdapterDiagnostics
output, even on authentication failure.
"""
from __future__ import annotations

import pytest
from azure.core.exceptions import ClientAuthenticationError
from azure.identity import ClientSecretCredential

from iq_platform.adapters.work_context.live_adapter import WorkIQLiveAdapter
from iq_platform.configuration.settings import LiveAdapterSettings

_FAKE_SECRET = "super-secret-value-should-never-appear-in-logs"


def _settings_with_secret() -> LiveAdapterSettings:
    return LiveAdapterSettings(
        entra_tenant_id="11111111-1111-1111-1111-111111111111",
        entra_client_id="22222222-2222-2222-2222-222222222222",
        entra_client_secret=_FAKE_SECRET,
        work_iq_workspace_id="ws-1",
        work_iq_auth_scope="https://example.com/.default",
    )


@pytest.mark.parametrize("outcome", ["auth_failure", "auth_success"])
def test_secret_never_appears_in_health_check_output(monkeypatch, outcome):
    settings = _settings_with_secret()
    adapter = WorkIQLiveAdapter(settings)

    if outcome == "auth_failure":

        def fake_get_token(self, *scopes, **kwargs):
            raise ClientAuthenticationError(message="invalid_client")
    else:
        from azure.core.credentials import AccessToken

        def fake_get_token(self, *scopes, **kwargs):
            return AccessToken("fake-token", 9999999999)

    monkeypatch.setattr(ClientSecretCredential, "get_token", fake_get_token)

    health = adapter.health_check()
    assert _FAKE_SECRET not in health.message

    diagnostics = adapter.get_diagnostics()
    assert _FAKE_SECRET not in str(diagnostics.model_dump())
