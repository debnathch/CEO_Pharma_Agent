"""Observability contracts: structured events, spans, metrics."""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class EventType(str, Enum):
    REQUEST_ACCEPTED = "request_accepted"
    WORKFLOW_STARTED = "workflow_started"
    AGENT_SELECTED = "agent_selected"
    AGENT_EXECUTION_STARTED = "agent_execution_started"
    TOOL_INVOKED = "tool_invoked"
    PROVIDER_CALL_COMPLETED = "provider_call_completed"
    PROVIDER_CALL_FAILED = "provider_call_failed"
    VALIDATION_FAILED = "validation_failed"
    APPROVAL_REQUESTED = "approval_requested"
    AGENT_EXECUTION_COMPLETED = "agent_execution_completed"
    FINAL_RESPONSE_RETURNED = "final_response_returned"
    EVALUATION_COMPLETED = "evaluation_completed"


class ObservabilityEvent(BaseModel):
    event_id: str = Field(..., description="Unique event identifier")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    event_type: EventType
    request_id: Optional[str] = None
    execution_id: Optional[str] = None
    correlation_id: str
    agent_id: Optional[str] = None
    agent_version: Optional[str] = None
    workflow_step: Optional[str] = None
    status: Optional[str] = None
    duration_ms: Optional[float] = None
    error_category: Optional[str] = None
    provider: Optional[str] = None
    model: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class TraceSpan(BaseModel):
    span_id: str
    trace_id: str
    parent_span_id: Optional[str] = None
    name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_ms: Optional[float] = None
    attributes: dict[str, Any] = Field(default_factory=dict)
    events: list[ObservabilityEvent] = Field(default_factory=list)


class MetricSummary(BaseModel):
    total_requests: int = 0
    successful_executions: int = 0
    partial_executions: int = 0
    failed_executions: int = 0
    agent_invocation_counts: dict[str, int] = Field(default_factory=dict)
    agent_success_rates: dict[str, float] = Field(default_factory=dict)
    average_duration_ms: float = 0.0
    p95_duration_ms: float = 0.0
    provider_mode: str = "mock"
    provider_available: bool = True
    active_evaluations_count: int = 0
