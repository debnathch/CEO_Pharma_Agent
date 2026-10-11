"""Distributed Tracing and Span context abstraction."""

import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Any, AsyncIterator, Optional

from pharma_platform.contracts.observability import TraceSpan


class TraceContext:
    """Manages spans for request execution."""

    def __init__(self, trace_id: Optional[str] = None) -> None:
        self.trace_id = trace_id or str(uuid.uuid4())
        self.spans: list[TraceSpan] = []

    def start_span(
        self, name: str, parent_span_id: Optional[str] = None, attributes: Optional[dict[str, Any]] = None
    ) -> TraceSpan:
        span_id = str(uuid.uuid4())[:8]
        span = TraceSpan(
            span_id=span_id,
            trace_id=self.trace_id,
            parent_span_id=parent_span_id,
            name=name,
            start_time=datetime.now(timezone.utc),
            attributes=attributes or {},
        )
        self.spans.append(span)
        return span

    def finish_span(self, span: TraceSpan) -> None:
        span.end_time = datetime.now(timezone.utc)
        duration_sec = (span.end_time - span.start_time).total_seconds()
        span.duration_ms = round(duration_sec * 1000.0, 2)


@asynccontextmanager
async def trace_span(
    tracer: TraceContext, name: str, parent_span_id: Optional[str] = None, attributes: Optional[dict[str, Any]] = None
) -> AsyncIterator[TraceSpan]:
    """Async context manager for tracing execution spans."""
    span = tracer.start_span(name, parent_span_id, attributes)
    try:
        yield span
    finally:
        tracer.finish_span(span)
