"""Environment-driven settings for Live Adapters (Phase 4).

All fields are optional and default to None - a missing value means "not
configured yet", not an error. See .env.example for the full placeholder list
and docs/setup/live-adapters-configuration.md for how to obtain real values.
"""
from __future__ import annotations

import os

from pydantic import BaseModel

#: Placeholder value used in .env.example for *_AUTH_SCOPE variables. Treated
#: as "not yet verified" rather than a real scope - see
#: docs/decisions/product-verification.md.
TBD_AUTH_SCOPE_PLACEHOLDER = "TBD-VERIFY-AGAINST-CURRENT-MICROSOFT-DOCUMENTATION"


class LiveAdapterSettings(BaseModel):
    # Microsoft Entra ID (shared across all Live Adapters for authentication)
    entra_tenant_id: str | None = None
    entra_client_id: str | None = None
    entra_client_secret: str | None = None

    # Copilot Studio ("GitHub Copilot harness")
    copilot_studio_environment_id: str | None = None
    copilot_studio_agent_id: str | None = None
    copilot_studio_auth_scope: str | None = None

    # Work IQ
    work_iq_workspace_id: str | None = None
    work_iq_auth_scope: str | None = None

    # Foundry IQ
    foundry_iq_project_endpoint: str | None = None
    foundry_iq_knowledge_base_id: str | None = None
    foundry_iq_auth_scope: str | None = None

    # Fabric IQ
    fabric_workspace_id: str | None = None
    fabric_ontology_id: str | None = None
    fabric_iq_auth_scope: str | None = None

    @classmethod
    def from_env(cls) -> LiveAdapterSettings:
        return cls(
            entra_tenant_id=os.environ.get("ENTRA_TENANT_ID") or None,
            entra_client_id=os.environ.get("ENTRA_CLIENT_ID") or None,
            entra_client_secret=os.environ.get("ENTRA_CLIENT_SECRET") or None,
            copilot_studio_environment_id=os.environ.get("COPILOT_STUDIO_ENVIRONMENT_ID") or None,
            copilot_studio_agent_id=os.environ.get("COPILOT_STUDIO_AGENT_ID") or None,
            copilot_studio_auth_scope=os.environ.get("COPILOT_STUDIO_AUTH_SCOPE") or None,
            work_iq_workspace_id=os.environ.get("WORK_IQ_WORKSPACE_ID") or None,
            work_iq_auth_scope=os.environ.get("WORK_IQ_AUTH_SCOPE") or None,
            foundry_iq_project_endpoint=os.environ.get("FOUNDRY_IQ_PROJECT_ENDPOINT") or None,
            foundry_iq_knowledge_base_id=os.environ.get("FOUNDRY_IQ_KNOWLEDGE_BASE_ID") or None,
            foundry_iq_auth_scope=os.environ.get("FOUNDRY_IQ_AUTH_SCOPE") or None,
            fabric_workspace_id=os.environ.get("FABRIC_WORKSPACE_ID") or None,
            fabric_ontology_id=os.environ.get("FABRIC_ONTOLOGY_ID") or None,
            fabric_iq_auth_scope=os.environ.get("FABRIC_IQ_AUTH_SCOPE") or None,
        )

    def missing_entra_fields(self) -> list[str]:
        missing = []
        if not self.entra_tenant_id:
            missing.append("ENTRA_TENANT_ID")
        if not self.entra_client_id:
            missing.append("ENTRA_CLIENT_ID")
        if not self.entra_client_secret:
            missing.append("ENTRA_CLIENT_SECRET")
        return missing

    def missing_fields_for(self, adapter_name: str) -> list[str]:
        """Required env vars (beyond the shared Entra ID ones) for a given
        Live Adapter, using the same names as .env.example."""
        missing = list(self.missing_entra_fields())
        if adapter_name == "work_iq":
            if not self.work_iq_workspace_id:
                missing.append("WORK_IQ_WORKSPACE_ID")
        elif adapter_name == "foundry_iq":
            if not self.foundry_iq_project_endpoint:
                missing.append("FOUNDRY_IQ_PROJECT_ENDPOINT")
            if not self.foundry_iq_knowledge_base_id:
                missing.append("FOUNDRY_IQ_KNOWLEDGE_BASE_ID")
        elif adapter_name == "fabric_iq":
            if not self.fabric_workspace_id:
                missing.append("FABRIC_WORKSPACE_ID")
            if not self.fabric_ontology_id:
                missing.append("FABRIC_ONTOLOGY_ID")
        elif adapter_name == "copilot_studio" and not self.copilot_studio_environment_id:
            missing.append("COPILOT_STUDIO_ENVIRONMENT_ID")
        return missing

    def auth_scope_for(self, adapter_name: str) -> str | None:
        """Returns the configured OAuth scope for the given adapter, or None
        if it hasn't been set to a real (non-placeholder) value yet. The
        correct scope for each Microsoft product is unverified - see
        docs/decisions/product-verification.md - so we never assume a default
        like Microsoft Graph's '.default' scope is correct for these products."""
        scope = {
            "work_iq": self.work_iq_auth_scope,
            "foundry_iq": self.foundry_iq_auth_scope,
            "fabric_iq": self.fabric_iq_auth_scope,
            "copilot_studio": self.copilot_studio_auth_scope,
        }.get(adapter_name)
        if not scope or scope == TBD_AUTH_SCOPE_PLACEHOLDER:
            return None
        return scope

