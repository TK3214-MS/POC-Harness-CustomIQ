"""Shared exceptions for Live Adapters (Phase 4).

See docs/decisions/0013-live-adapter-verification-required-scaffold.md.
"""
from __future__ import annotations


class LiveAdapterNotYetVerifiedError(RuntimeError):
    """Raised by every Live Adapter's query(). The underlying Microsoft
    product API contract (request/response shape, endpoint, scope) has not
    been verified against current Microsoft documentation - see
    docs/decisions/product-verification.md. This accelerator refuses to guess
    it, so no Live Adapter ever actually calls a product endpoint yet."""
