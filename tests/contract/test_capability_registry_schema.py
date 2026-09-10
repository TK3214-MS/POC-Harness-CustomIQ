"""Contract tests for config/capabilities.yaml against iq_platform.contracts.capability.

See docs/decisions/0007-capability-registry-authority.md.
"""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from iq_platform.capability_registry.loader import CapabilityRegistryError, load_capability_registry
from iq_platform.contracts.capability import CapabilityStatus

REGISTRY_PATH = Path(__file__).resolve().parents[2] / "config" / "capabilities.yaml"


def test_capability_registry_loads_and_validates():
    registry = load_capability_registry(REGISTRY_PATH)
    assert registry.schema_version
    assert len(registry.capabilities) > 0


def test_every_capability_has_a_known_status():
    registry = load_capability_registry(REGISTRY_PATH)
    for capability in registry.capabilities:
        assert capability.status in CapabilityStatus


def test_verified_status_capabilities_carry_real_evidence():
    """Any capability claiming GA/Preview/Private Preview must carry a real
    last_verified_date and a non-TBD documentation_reference. This is already
    enforced at load time by the Capability model validator - this test documents
    and double-checks the invariant on the current registry snapshot."""
    registry = load_capability_registry(REGISTRY_PATH)
    verified = {CapabilityStatus.GA, CapabilityStatus.PREVIEW, CapabilityStatus.PRIVATE_PREVIEW}
    for capability in registry.capabilities:
        if capability.status in verified:
            assert capability.last_verified_date is not None
            assert "TBD" not in capability.documentation_reference


def test_capability_lookup_by_id():
    registry = load_capability_registry(REGISTRY_PATH)
    assert registry.get("mcp_backend") is not None
    assert registry.get("no-such-capability") is None


def test_missing_registry_file_raises(tmp_path):
    with pytest.raises(CapabilityRegistryError):
        load_capability_registry(tmp_path / "does-not-exist.yaml")


def test_registry_missing_required_field_raises(tmp_path):
    bad_registry = tmp_path / "capabilities.yaml"
    bad_registry.write_text(yaml.safe_dump({"schema_version": "1.0.0"}), encoding="utf-8")
    with pytest.raises(CapabilityRegistryError):
        load_capability_registry(bad_registry)


def test_registry_rejects_ga_status_without_verification(tmp_path):
    """A capability cannot claim GA status without a real last_verified_date and
    documentation_reference - this is the core safety rail from ADR-0007."""
    bad_registry = tmp_path / "capabilities.yaml"
    bad_registry.write_text(
        yaml.safe_dump(
            {
                "schema_version": "1.0.0",
                "capabilities": [
                    {
                        "capability_id": "fake",
                        "display_name": "Fake",
                        "product": "Fake Product",
                        "status": "GA",
                        "last_verified_date": None,
                        "documentation_reference": "TBD - VERIFY AGAINST CURRENT MICROSOFT DOCUMENTATION",
                        "required_license": "n/a",
                        "required_role": "n/a",
                        "required_admin_setting": "n/a",
                        "regional_availability": "n/a",
                        "supported_modes": ["live"],
                        "customer_facing_disclosure": "n/a",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(CapabilityRegistryError):
        load_capability_registry(bad_registry)
