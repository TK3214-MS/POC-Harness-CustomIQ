"""Minimal shared logging setup. Full Observability Guide work (trace propagation,
cost driver capture, etc.) is deferred to a later phase - see
iq_platform/observability/README.md. This module just gives Phase 2's
orchestrator and MCP backend consistent, correlation-ID-aware logging.

Uses a custom Formatter (rather than a LogRecordFactory default) so that calls
which already pass `extra={"correlation_id": ...}` never collide with a
pre-set attribute - Python's logging raises KeyError if `extra` tries to
overwrite an attribute the record already has.
"""
from __future__ import annotations

import logging

_CONFIGURED = False


class _CorrelationIdFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        if not hasattr(record, "correlation_id"):
            record.correlation_id = "-"
        return super().format(record)


def configure_logging(level: int = logging.INFO) -> None:
    global _CONFIGURED
    if _CONFIGURED:
        return
    handler = logging.StreamHandler()
    handler.setFormatter(
        _CorrelationIdFormatter(
            "%(asctime)s %(levelname)s %(name)s [correlation_id=%(correlation_id)s] %(message)s"
        )
    )
    root = logging.getLogger()
    root.setLevel(level)
    root.addHandler(handler)
    _CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    configure_logging()
    return logging.getLogger(name)

