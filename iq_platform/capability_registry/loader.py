"""Load and validate config/capabilities.yaml into a CapabilityRegistry."""
from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import ValidationError

from iq_platform.contracts.capability import CapabilityRegistry


class CapabilityRegistryError(RuntimeError):
    """Raised when config/capabilities.yaml is missing, malformed, or fails schema validation."""


def load_capability_registry(path: str | Path) -> CapabilityRegistry:
    registry_path = Path(path)
    if not registry_path.exists():
        raise CapabilityRegistryError(f"Capability registry not found at {registry_path}")

    with registry_path.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle)

    if raw is None:
        raise CapabilityRegistryError(f"Capability registry at {registry_path} is empty")

    try:
        return CapabilityRegistry.model_validate(raw)
    except ValidationError as exc:
        raise CapabilityRegistryError(
            f"Capability registry at {registry_path} failed schema validation:\n{exc}"
        ) from exc
