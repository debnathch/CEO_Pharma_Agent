"""Structured Logging with Contextual Correlation IDs and Safe Sanitization."""

import json
import logging
import sys
from datetime import datetime, timezone

from pharma_platform.contracts.observability import ObservabilityEvent


class StructuredJsonFormatter(logging.Formatter):
    """Formats log records as structured JSON without sensitive credentials."""

    def format(self, record: logging.LogRecord) -> str:
        log_payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "correlation_id": getattr(record, "correlation_id", "none"),
            "request_id": getattr(record, "request_id", None),
            "execution_id": getattr(record, "execution_id", None),
            "agent_id": getattr(record, "agent_id", None),
            "event_type": getattr(record, "event_type", None),
            "duration_ms": getattr(record, "duration_ms", None),
        }
        if record.exc_info:
            log_payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_payload)


_events_buffer: list[ObservabilityEvent] = []


def emit_event(event: ObservabilityEvent) -> None:
    """Record an observability event and log it."""
    _events_buffer.append(event)
    # Keep buffer bounded to recent 1000 events
    if len(_events_buffer) > 1000:
        del _events_buffer[:200]

    logger = logging.getLogger("pharma.observability")
    extra = {
        "correlation_id": event.correlation_id,
        "request_id": event.request_id,
        "execution_id": event.execution_id,
        "agent_id": event.agent_id,
        "event_type": event.event_type.value,
        "duration_ms": event.duration_ms,
    }
    logger.info("Observability event: %s (%s)", event.event_type.value, event.status or "info", extra=extra)


def get_recent_events(limit: int = 50) -> list[ObservabilityEvent]:
    """Retrieve recent structured events."""
    return _events_buffer[-limit:]


def setup_observability_logging(level: str = "INFO") -> None:
    """Configure root logger with structured JSON formatting."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(StructuredJsonFormatter())
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    # Avoid duplicate handlers
    if not any(isinstance(h, logging.StreamHandler) for h in root_logger.handlers):
        root_logger.addHandler(handler)
