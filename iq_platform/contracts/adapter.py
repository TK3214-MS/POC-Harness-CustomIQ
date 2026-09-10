"""Common Adapter interface shared by Work Context, Knowledge, Semantic, and MCP Tool adapters.

See docs/decisions/0003-adapter-contract-and-mode-enum.md and instruction section 6.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from iq_platform.contracts.capability import AdapterMode


class AdapterHealth(BaseModel):
    healthy: bool
    mode: AdapterMode
    message: str
    checked_at: datetime


class AdapterDiagnostics(BaseModel):
    adapter_name: str
    mode: AdapterMode
    configuration_valid: bool
    missing_configuration: list[str] = Field(default_factory=list)
    details: dict[str, Any] = Field(default_factory=dict)


class AdapterCapabilities(BaseModel):
    adapter_name: str
    supported_operations: list[str]
    mode: AdapterMode


class Adapter(ABC):
    """Every IQ layer adapter (Work Context, Knowledge, Semantic, MCP Tool) implements this.

    Concrete adapters are instantiated with a fixed ``mode`` (see AdapterMode); an
    adapter never silently changes mode based on a failed auth check - callers must
    read ``health_check()``/``get_diagnostics()`` to see why it isn't live.
    """

    @abstractmethod
    def health_check(self) -> AdapterHealth: ...

    @abstractmethod
    def capabilities(self) -> AdapterCapabilities: ...

    @property
    @abstractmethod
    def mode(self) -> AdapterMode: ...

    @abstractmethod
    def query(self, operation: str, parameters: dict[str, Any]) -> dict[str, Any]: ...

    @abstractmethod
    def validate_configuration(self) -> AdapterDiagnostics: ...

    @abstractmethod
    def get_diagnostics(self) -> AdapterDiagnostics: ...
