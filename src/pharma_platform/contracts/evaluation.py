"""Evaluation contracts and metric definitions."""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class EvaluationCategory(str, Enum):
    ROUTING_ACCURACY = "routing_accuracy"
    CONTRACT_VALIDITY = "contract_validity"
    DATA_CORRECTNESS = "data_correctness"
    EVIDENCE_COVERAGE = "evidence_coverage"
    GROUNDEDNESS = "groundedness"
    TASK_COMPLETION = "task_completion"
    SAFETY_POLICY = "safety_and_policy"
    ROBUSTNESS = "robustness"
    LATENCY_RESOURCE = "latency_and_resource"


class EvaluatorType(str, Enum):
    DETERMINISTIC = "deterministic"
    SCHEMA_VALIDATOR = "schema_validator"
    POLICY_VERIFIER = "policy_verifier"
    MODEL_BASED = "model_based"
    HUMAN_REVIEW = "human_review"


class EvaluationCase(BaseModel):
    case_id: str = Field(..., description="Unique case ID (e.g. TC-SALES-001)")
    name: str = Field(..., description="Descriptive name")
    category: EvaluationCategory = Field(...)
    target_agent: str = Field(..., description="Target agent under evaluation")
    user_query: str = Field(..., description="Input user prompt/query")
    expected_agents_routed: list[str] = Field(default_factory=list)
    expected_status: str = Field(default="success")
    required_keywords: list[str] = Field(default_factory=list)
    required_evidence_sources: list[str] = Field(default_factory=list)
    forbidden_claims_or_actions: list[str] = Field(default_factory=list)
    expected_structured_keys: list[str] = Field(default_factory=list)
    dataset_version: str = Field(default="v1.0.0")
    tags: list[str] = Field(default_factory=list)


class MetricResult(BaseModel):
    metric_name: str
    category: EvaluationCategory
    score: float = Field(..., description="Score typically normalized 0.0 to 1.0")
    threshold: float = Field(default=1.0)
    passed: bool
    details: str = ""


class EvaluationResult(BaseModel):
    run_id: str
    case_id: str
    category: EvaluationCategory
    passed: bool
    failure_reason: Optional[str] = None
    metric_results: list[MetricResult] = Field(default_factory=list)
    duration_ms: float = 0.0
    evaluator_type: EvaluatorType = EvaluatorType.DETERMINISTIC
    execution_reference: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class EvaluationRunSummary(BaseModel):
    run_id: str
    dataset_version: str
    model_mode: str
    model_identifier: str
    start_time: datetime
    end_time: datetime
    total_cases: int
    passed_cases: int
    failed_cases: int
    pass_rate: float
    category_scores: dict[str, float] = Field(default_factory=dict)
    results: list[EvaluationResult] = Field(default_factory=list)
    regression_detected: bool = False
    regression_details: list[str] = Field(default_factory=list)
