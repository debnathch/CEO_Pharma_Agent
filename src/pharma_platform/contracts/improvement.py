"""Continuous improvement contracts and governance models."""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class FeedbackRating(str, Enum):
    HELPFUL = "helpful"
    INCORRECT = "incorrect"
    INCOMPLETE = "incomplete"
    UNSUPPORTED = "unsupported"


class FailureCategory(str, Enum):
    ROUTING_MISCLASSIFICATION = "routing_misclassification"
    DATA_INCONSISTENCY = "data_inconsistency"
    MISSING_EVIDENCE = "missing_evidence"
    UNSUPPORTED_CAPABILITY = "unsupported_capability"
    SCHEMA_VALIDATION_FAILURE = "schema_validation_failure"
    TIMEOUT_OR_UNAVAILABLE = "timeout_or_unavailable"
    POLICY_VIOLATION_ATTEMPT = "policy_violation_attempt"


class ProposalStatus(str, Enum):
    DRAFT = "draft"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    RELEASED = "released"
    ROLLED_BACK = "rolled_back"


class ProposalType(str, Enum):
    PROMPT_REFINEMENT = "prompt_refinement"
    ROUTING_KEYWORD_UPDATE = "routing_keyword_update"
    POLICY_RULE_ADDITION = "policy_rule_addition"
    NEW_CAPABILITY_STUB = "new_capability_stub"
    DATA_SOURCE_MAPPING = "data_source_mapping"


class FeedbackRecord(BaseModel):
    feedback_id: str
    execution_id: str
    rating: FeedbackRating
    comment: Optional[str] = None
    reviewer_id: str = "reviewer-01"
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ImprovementProposal(BaseModel):
    proposal_id: str
    title: str
    description: str
    target_agent_id: str
    proposal_type: ProposalType
    failure_category: FailureCategory
    rationale: str
    proposed_changes: dict[str, Any]
    status: ProposalStatus = ProposalStatus.DRAFT
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    review_comments: Optional[str] = None
    regression_suite_passed: bool = False
    baseline_run_id: Optional[str] = None
    candidate_run_id: Optional[str] = None
