"""Shared base for Live Adapters (Phase 4).

See docs/decisions/0013-live-adapter-verification-required-scaffold.md. No
Live Adapter in this repo ever reaches AdapterMode.LIVE - the underlying
Microsoft product API contracts (Work IQ / Foundry IQ / Fabric IQ) are
unverified (docs/decisions/product-verification.md), so query() always raises
rather than guessing a request/response shape. What IS real and testable
here: environment-variable-driven configuration presence, and genuine
Microsoft Entra ID authentication via azure-identity.
"""
from __future__ import annotations

from abc import ABC
from datetime import UTC, datetime
from typing import Any, ClassVar

from iq_platform.adapters.errors import LiveAdapterNotYetVerifiedError
from iq_platform.configuration.settings import LiveAdapterSettings
from iq_platform.contracts.adapter import (
    Adapter,
    AdapterCapabilities,
    AdapterDiagnostics,
    AdapterHealth,
)
from iq_platform.contracts.capability import AdapterMode
from iq_platform.security.entra_auth import EntraAuthConfigurationError, EntraAuthFailedError, acquire_token


class BaseLiveAdapter(Adapter, ABC):
    #: Subclasses must set these class attributes.
    adapter_name: str = ""
    settings_key: str = ""
    supported_operations: ClassVar[list[str]] = []

    def __init__(self, settings: LiveAdapterSettings | None = None):
        self._settings = settings or LiveAdapterSettings.from_env()

    def _missing_configuration(self) -> list[str]:
        return self._settings.missing_fields_for(self.settings_key)

    @property
    def mode(self) -> AdapterMode:
        return AdapterMode.UNAVAILABLE if self._missing_configuration() else AdapterMode.VERIFICATION_REQUIRED

    def capabilities(self) -> AdapterCapabilities:
        return AdapterCapabilities(
            adapter_name=self.adapter_name, supported_operations=self.supported_operations, mode=self.mode
        )

    def health_check(self) -> AdapterHealth:
        missing = self._missing_configuration()
        if missing:
            return AdapterHealth(
                healthy=False,
                mode=self.mode,
                message=(
                    f"Missing required configuration: {missing}. "
                    "See docs/setup/live-adapters-configuration.md."
                ),
                checked_at=datetime.now(UTC),
            )

        scope = self._settings.auth_scope_for(self.settings_key)
        if scope is None:
            return AdapterHealth(
                healthy=False,
                mode=self.mode,
                message=(
                    "Configuration present, but the OAuth scope for this product has not been verified yet "
                    "(still the TBD placeholder). See docs/setup/live-adapters-configuration.md."
                ),
                checked_at=datetime.now(UTC),
            )

        try:
            acquire_token(self._settings, scope)
        except (EntraAuthConfigurationError, EntraAuthFailedError) as exc:
            return AdapterHealth(healthy=False, mode=self.mode, message=str(exc), checked_at=datetime.now(UTC))

        return AdapterHealth(
            healthy=False,  # never "healthy" - the product API contract itself is still unverified
            mode=self.mode,
            message=(
                "Microsoft Entra ID authentication succeeded for the configured scope, but the underlying "
                "product API contract has not been verified against current Microsoft documentation - see "
                "docs/decisions/product-verification.md. This adapter will not call any endpoint until that "
                "verification is done and this code is updated."
            ),
            checked_at=datetime.now(UTC),
        )

    def validate_configuration(self) -> AdapterDiagnostics:
        missing = self._missing_configuration()
        return AdapterDiagnostics(
            adapter_name=self.adapter_name,
            mode=self.mode,
            configuration_valid=not missing,
            missing_configuration=missing,
            details={
                "note": (
                    "configuration_valid means required environment variables are present - it does NOT mean "
                    "the product API contract has been verified (see docs/decisions/product-verification.md)."
                )
            },
        )

    def get_diagnostics(self) -> AdapterDiagnostics:
        return self.validate_configuration()

    def query(self, operation: str, parameters: dict[str, Any]) -> dict[str, Any]:
        raise LiveAdapterNotYetVerifiedError(
            f"{self.adapter_name}.query('{operation}') is not implemented: the Microsoft product API contract "
            "has not been verified against current documentation (see docs/decisions/product-verification.md)."
        )
