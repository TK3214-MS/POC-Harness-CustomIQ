"""Capability Registry schema (config/capabilities.yaml).

See docs/decisions/0007-capability-registry-authority.md.
"""
from __future__ import annotations

from datetime import date
from enum import Enum

from pydantic import BaseModel, Field, model_validator

_TBD = "TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION"

#: Statuses that assert a capability has actually been checked against current
#: Microsoft documentation. Anything else (Mock Only / Unknown / Verify Before Use)
#: is allowed to stay unverified indefinitely.
_VERIFIED_STATUSES: frozenset[CapabilityStatus]


class CapabilityStatus(str, Enum):
    GA = "GA"
    PREVIEW = "Preview"
    PRIVATE_PREVIEW = "Private Preview"
    MOCK_ONLY = "Mock Only"
    UNKNOWN = "Unknown"
    VERIFY_BEFORE_USE = "Verify Before Use"


_VERIFIED_STATUSES = frozenset(
    {CapabilityStatus.GA, CapabilityStatus.PREVIEW, CapabilityStatus.PRIVATE_PREVIEW}
)


class AdapterMode(str, Enum):
    LIVE = "live"
    UNAVAILABLE = "unavailable"


class Capability(BaseModel):
    """One row of config/capabilities.yaml. Field names mirror instruction section 7."""

    capability_id: str
    display_name: str
    product: str
    status: CapabilityStatus
    last_verified_date: date | None = None
    documentation_reference: str
    required_license: str
    required_role: str
    required_admin_setting: str
    regional_availability: str
    supported_modes: list[AdapterMode]
    fallback_adapter: str | None = None
    known_limitations: list[str] = Field(default_factory=list)
    customer_facing_disclosure: str

    @model_validator(mode="after")
    def _verified_status_requires_real_evidence(self) -> Capability:
        """A status of GA/Preview/Private Preview is a claim that someone actually
        checked current Microsoft documentation. Refuse to accept that claim unless
        it carries a real verification date and a real (non-TBD) doc reference."""
        if self.status in _VERIFIED_STATUSES:
            if self.last_verified_date is None:
                raise ValueError(
                    f"{self.capability_id}: status '{self.status.value}' requires a real "
                    "last_verified_date (see docs/decisions/product-verification.md)."
                )
            if _TBD in self.documentation_reference:
                raise ValueError(
                    f"{self.capability_id}: status '{self.status.value}' cannot keep a "
                    "TBD documentation_reference."
                )
        return self


class CapabilityRegistry(BaseModel):
    schema_version: str
    capabilities: list[Capability]

    def get(self, capability_id: str) -> Capability | None:
        return next((c for c in self.capabilities if c.capability_id == capability_id), None)
