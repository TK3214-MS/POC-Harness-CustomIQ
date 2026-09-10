"""Unit tests: LiveAdapterSettings environment-variable parsing (Phase 4). See
docs/decisions/0013-live-adapter-verification-required-scaffold.md.
"""
from __future__ import annotations

from iq_platform.configuration.settings import TBD_AUTH_SCOPE_PLACEHOLDER, LiveAdapterSettings


def test_from_env_reads_all_expected_variables(monkeypatch):
    monkeypatch.setenv("ENTRA_TENANT_ID", "tenant-1")
    monkeypatch.setenv("ENTRA_CLIENT_ID", "client-1")
    monkeypatch.setenv("ENTRA_CLIENT_SECRET", "secret-1")
    monkeypatch.setenv("WORK_IQ_WORKSPACE_ID", "ws-1")
    monkeypatch.setenv("WORK_IQ_AUTH_SCOPE", "https://example.com/.default")

    settings = LiveAdapterSettings.from_env()
    assert settings.entra_tenant_id == "tenant-1"
    assert settings.work_iq_workspace_id == "ws-1"
    assert settings.work_iq_auth_scope == "https://example.com/.default"


def test_from_env_treats_empty_string_as_unset(monkeypatch):
    monkeypatch.setenv("ENTRA_TENANT_ID", "")
    settings = LiveAdapterSettings.from_env()
    assert settings.entra_tenant_id is None


def test_missing_fields_for_unknown_adapter_name_returns_only_entra_gaps():
    settings = LiveAdapterSettings()
    missing = settings.missing_fields_for("some_future_adapter")
    assert missing == ["ENTRA_TENANT_ID", "ENTRA_CLIENT_ID", "ENTRA_CLIENT_SECRET"]


def test_auth_scope_for_treats_tbd_placeholder_as_unset():
    settings = LiveAdapterSettings(work_iq_auth_scope=TBD_AUTH_SCOPE_PLACEHOLDER)
    assert settings.auth_scope_for("work_iq") is None


def test_auth_scope_for_returns_real_value_when_set():
    settings = LiveAdapterSettings(work_iq_auth_scope="https://example.com/.default")
    assert settings.auth_scope_for("work_iq") == "https://example.com/.default"
