"""Capability Registry loader/validator for config/capabilities.yaml.

See docs/decisions/0007-capability-registry-authority.md.
"""
from iq_platform.capability_registry.loader import CapabilityRegistryError, load_capability_registry

__all__ = ["CapabilityRegistryError", "load_capability_registry"]
