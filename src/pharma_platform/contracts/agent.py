"""Standardized agent contracts and schemas."""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class AgentStatus(str, Enum):
    SUCCESS = "success"
    PARTIAL = "partial"
    NEEDS_INPUT = "needs_input"
    NOT_IMPLEMENTED = "not_implemented"
    APPROVAL_REQUIRED = "approval_required"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ImplementationStatus(str, Enum):
    FULL = "full"
    PARTIAL = "partial"
    SKELETON = "skeleton"


class AgentCapability(BaseModel):
    name: str = Field(..., description="Unique capability identifier within the agent")
    description: str = Field(..., description="Human-readable description of what capability does")
    input_schema_name: str = Field(..., description="Identifier of the input schema")
    output_schema_name: str = Field(..., description="Identifier of the output schema")
    is_implemented: bool = Field(default=False, description="Whether this capability is implemented")
    requires_approval: bool = Field(default=False, description="Whether capability requires human approval")


class AgentManifest(BaseModel):
    agent_id: str = Field(..., description="Stable, unique agent identifier (e.g. ethical_sales)")
    display_name: str = Field(..., description="Human-readable display name")
    description: str = Field(..., description="High-level description of agent scope")
    domain: str = Field(..., description="Department or business domain")
    version: str = Field(default="0.1.0", description="Semver version of the agent")
    capabilities: list[AgentCapability] = Field(default_factory=list, description="Declared capabilities")
    implementation_status: ImplementationStatus = Field(
        default=ImplementationStatus.SKELETON, description="Current implementation readiness"
    )
    required_permissions: list[str] = Field(default_factory=list, description="Required permissions")
    supported_tools: list[str] = Field(default_factory=list, description="Tools accessible by this agent")
    readiness_info: dict[str, Any] = Field(default_factory=dict, description="Metadata on test/eval status")


class AgentContext(BaseModel):
    user_id: str = Field(default="exec-01", description="Identifier of the requesting user")
    user_role: str = Field(default="CEO", description="Role of the user (e.g., CEO, SalesDirector)")
    department: Optional[str] = Field(default="Executive", description="Department of the user")
    session_id: Optional[str] = Field(default=None, description="UI session or conversation ID")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Arbitrary execution context")


class AgentRequest(BaseModel):
    request_id: str = Field(..., description="Unique request identifier")
    execution_id: str = Field(..., description="Execution identifier for this specific invocation")
    correlation_id: str = Field(..., description="Correlation ID spanning the entire request graph")
    capability: str = Field(..., description="Capability to invoke")
    parameters: dict[str, Any] = Field(default_factory=dict, description="Input parameters")
    context: AgentContext = Field(default_factory=AgentContext, description="Caller context")
    deadline: Optional[datetime] = Field(default=None, description="Optional deadline for execution")


class EvidenceReference(BaseModel):
    source_system: str = Field(..., description="Source system (e.g., Marg ERP, Ordering Portal, Synthetic Fixture)")
    entity_type: str = Field(..., description="Entity type (e.g., Invoice, Ledger, Shipment, Employee)")
    entity_id: str = Field(..., description="Identifier of entity")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), description="Timestamp of the evidence record"
    )
    authoritative: bool = Field(default=True, description="Whether this source is authoritative for this entity")
    details: dict[str, Any] = Field(default_factory=dict, description="Supporting data snippet")


class AgentResult(BaseModel):
    execution_id: str = Field(..., description="Execution identifier matching the request")
    agent_id: str = Field(..., description="Stable agent identifier that produced this result")
    version: str = Field(..., description="Agent version")
    status: AgentStatus = Field(..., description="Outcome status")
    structured_data: dict[str, Any] = Field(default_factory=dict, description="Typed output payload")
    summary: str = Field(..., description="Human-readable grounded summary")
    evidence: list[EvidenceReference] = Field(default_factory=list, description="Linked evidence references")
    warnings: list[str] = Field(default_factory=list, description="Warnings or caveats")
    error_details: Optional[dict[str, Any]] = Field(default=None, description="Safe error details if failed")
    duration_ms: float = Field(default=0.0, description="Duration in milliseconds")
    data_mode: str = Field(default="synthetic", description="Explicit labeling of data mode")
    source_freshness: Optional[str] = Field(default=None, description="Timestamp or freshness label of underlying data")
