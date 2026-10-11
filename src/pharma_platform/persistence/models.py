"""SQLAlchemy ORM models for platform persistence."""

from datetime import datetime, timezone

from sqlalchemy import JSON, Boolean, Column, DateTime, Float, Integer, String, Text

from pharma_platform.persistence.database import Base


class ExecutionRecordModel(Base):
    """Persisted record of an orchestrator/agent execution."""

    __tablename__ = "execution_records"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String(64), index=True, nullable=False)
    execution_id = Column(String(64), unique=True, index=True, nullable=False)
    correlation_id = Column(String(64), index=True, nullable=False)
    user_query = Column(Text, nullable=False)
    workflow_status = Column(String(32), default="success", nullable=False)
    agents_invoked = Column(JSON, default=list)
    duration_ms = Column(Float, default=0.0)
    provider_mode = Column(String(32), default="mock")
    model_identifier = Column(String(64), default="default")
    structured_data = Column(JSON, default=dict)
    summary = Column(Text, default="")
    evidence_count = Column(Integer, default=0)
    warnings = Column(JSON, default=list)
    error_category = Column(String(64), nullable=True)
    data_mode = Column(String(32), default="synthetic")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)


class FeedbackRecordModel(Base):
    """User or reviewer feedback attached to an execution."""

    __tablename__ = "feedback_records"

    id = Column(Integer, primary_key=True, index=True)
    feedback_id = Column(String(64), unique=True, index=True, nullable=False)
    execution_id = Column(String(64), index=True, nullable=False)
    rating = Column(String(32), nullable=False)
    comment = Column(Text, nullable=True)
    reviewer_id = Column(String(64), default="reviewer-01")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class EvaluationRunModel(Base):
    """Persisted results of an evaluation suite run."""

    __tablename__ = "evaluation_runs"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(String(64), unique=True, index=True, nullable=False)
    dataset_version = Column(String(32), default="v1.0.0")
    model_mode = Column(String(32), default="mock")
    model_identifier = Column(String(64), default="mock-deterministic-v1")
    total_cases = Column(Integer, default=0)
    passed_cases = Column(Integer, default=0)
    failed_cases = Column(Integer, default=0)
    pass_rate = Column(Float, default=0.0)
    category_scores = Column(JSON, default=dict)
    results_json = Column(JSON, default=list)
    regression_detected = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)


class ImprovementProposalModel(Base):
    """Proposed continuous improvements to prompts, routing, or agent capabilities."""

    __tablename__ = "improvement_proposals"

    id = Column(Integer, primary_key=True, index=True)
    proposal_id = Column(String(64), unique=True, index=True, nullable=False)
    title = Column(String(256), nullable=False)
    description = Column(Text, nullable=False)
    target_agent_id = Column(String(64), nullable=False)
    proposal_type = Column(String(64), nullable=False)
    failure_category = Column(String(64), nullable=False)
    rationale = Column(Text, nullable=False)
    proposed_changes = Column(JSON, default=dict)
    status = Column(String(32), default="draft", nullable=False)
    reviewed_by = Column(String(64), nullable=True)
    review_comments = Column(Text, nullable=True)
    regression_suite_passed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)


class AuditEventModel(Base):
    """Audit log of sensitive or policy-relevant operations."""

    __tablename__ = "audit_events"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String(64), unique=True, index=True, nullable=False)
    action = Column(String(64), nullable=False)
    user_id = Column(String(64), nullable=False)
    details = Column(JSON, default=dict)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
