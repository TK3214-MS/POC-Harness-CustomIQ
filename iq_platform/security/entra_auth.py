"""Shared Microsoft Entra ID authentication helper for Live Adapters (Phase 4).

Uses azure-identity's ClientSecretCredential - a real, documented, GA
authentication pattern - independent of any specific Work IQ/Foundry IQ/Fabric
IQ API contract (which is unverified, see docs/decisions/product-verification.md).
This lets a Live Adapter prove its credentials work even before the actual
product API integration can be implemented.
"""
from __future__ import annotations

from azure.core.exceptions import ClientAuthenticationError
from azure.identity import ClientSecretCredential

from iq_platform.configuration.settings import LiveAdapterSettings


class EntraAuthConfigurationError(RuntimeError):
    """Raised when required Entra ID configuration is missing."""


class EntraAuthFailedError(RuntimeError):
    """Raised when token acquisition fails (bad credentials, network, etc.).
    Never includes the client secret in its message."""


def build_credential(settings: LiveAdapterSettings) -> ClientSecretCredential:
    missing = settings.missing_entra_fields()
    if missing:
        raise EntraAuthConfigurationError(f"Missing required Entra ID configuration: {missing}")
    return ClientSecretCredential(
        tenant_id=settings.entra_tenant_id,
        client_id=settings.entra_client_id,
        client_secret=settings.entra_client_secret,
    )


def acquire_token(settings: LiveAdapterSettings, scope: str) -> str:
    """Acquire an access token for the given scope (e.g.
    'https://graph.microsoft.com/.default'). Raises EntraAuthConfigurationError
    or EntraAuthFailedError - never returns a fabricated token."""
    credential = build_credential(settings)
    try:
        token = credential.get_token(scope)
    except ClientAuthenticationError as exc:
        raise EntraAuthFailedError(f"Entra ID authentication failed for scope '{scope}': {exc.__class__.__name__}") from exc
    return token.token
