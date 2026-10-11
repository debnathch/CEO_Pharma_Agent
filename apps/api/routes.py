"""Versioned FastAPI API Routes for the Enterprise Pharmaceutical Ecosystem."""

from datetime import datetime, timezone
from typing import Any, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from pharma_platform.business_services import (
    BillingService,
    FinanceService,
    HRService,
    LogisticsService,
    ProcurementService,
    SalesService,
)
from pharma_platform.contracts.agent import AgentManifest
from pharma_platform.contracts.improvement import FeedbackRating
from pharma_platform.contracts.observability import MetricSummary
from pharma_platform.evaluation.runner import EvaluationRunner
from pharma_platform.improvement import FailureAnalyzer, FeedbackService, ProposalEngine
from pharma_platform.integrations import (
    HRSystemAdapter,
    IntegrationHealth,
    MargERPAdapter,
    OrderingPortalAdapter,
    SocialMediaAdapter,
    WhatsAppIngestionAdapter,
)
from pharma_platform.observability import get_metrics_collector, get_recent_events
from pharma_platform.orchestration.workflow import run_ceo_workflow
from pharma_platform.persistence.database import get_session
from pharma_platform.persistence.models import EvaluationRunModel, ExecutionRecordModel
from pharma_platform.providers.factory import get_llm_provider
from pharma_platform.registry.registry import get_agent_registry

router = APIRouter(prefix="/api/v1")


# Request/Response Models
class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Natural language prompt for CEO agent")
    context: dict[str, Any] = Field(default_factory=dict)
    correlation_id: Optional[str] = None


class ChatResponse(BaseModel):
    execution_id: str
    request_id: str
    correlation_id: str
    status: str
    summary: str
    agents_invoked: list[str]
    structured_data: dict[str, Any]
    evidence: list[dict[str, Any]]
    warnings: list[str]
    duration_ms: float
    provider_used: str
    model_used: str
    is_mock: bool
    data_mode: str = "synthetic"


class FeedbackSubmitRequest(BaseModel):
    execution_id: str
    rating: FeedbackRating
    comment: str = ""
    reviewer_id: str = "reviewer-01"


class ReviewProposalRequest(BaseModel):
    decision: str  # "approved" or "rejected"
    reviewer_id: str = "architect-01"
    comments: str = ""


# 1. Health & Readiness
@router.get("/health")
async def health_check():
    """Health status and basic service liveness."""
    provider = get_llm_provider()
    p_health = await provider.health_check()
    return {
        "status": "healthy",
        "service": "Enterprise Pharmaceutical Agentic AI Ecosystem",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "provider": p_health.model_dump(),
        "data_mode": "synthetic",
    }


@router.get("/readiness")
async def readiness_check():
    """Readiness probe checking registry and database."""
    registry = get_agent_registry()
    agents = registry.list_agents()
    return {
        "ready": len(agents) > 0,
        "registered_agents_count": len(agents),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# 2. CEO Chat & Daily Briefing
@router.post("/ceo/chat", response_model=ChatResponse)
async def ceo_chat(req: ChatRequest):
    """Submit a natural language inquiry to the CEO Master Agent."""
    state = await run_ceo_workflow(
        user_query=req.query,
        context=req.context or {"user_role": "CEO", "user_id": "exec-01"},
        correlation_id=req.correlation_id,
    )
    invoked = [r.get("agent_id") for r in state.get("agent_results", []) if r.get("agent_id")]

    return ChatResponse(
        execution_id=state["execution_id"],
        request_id=state["request_id"],
        correlation_id=state["correlation_id"],
        status=state["status"],
        summary=state["executive_summary"],
        agents_invoked=invoked,
        structured_data=state["aggregated_data"],
        evidence=state["all_evidence"],
        warnings=state["warnings"],
        duration_ms=state["duration_ms"],
        provider_used=state["provider_used"],
        model_used=state["model_used"],
        is_mock=state["is_mock"],
        data_mode="synthetic",
    )


@router.get("/ceo/daily-briefing", response_model=ChatResponse)
async def get_daily_briefing():
    """Retrieve synthesized daily executive morning briefing."""
    state = await run_ceo_workflow(
        user_query="Generate comprehensive morning daily briefing for the CEO",
        context={"user_role": "CEO", "user_id": "exec-01"},
    )
    invoked = [r.get("agent_id") for r in state.get("agent_results", []) if r.get("agent_id")]

    return ChatResponse(
        execution_id=state["execution_id"],
        request_id=state["request_id"],
        correlation_id=state["correlation_id"],
        status=state["status"],
        summary=state["executive_summary"],
        agents_invoked=invoked,
        structured_data=state["aggregated_data"],
        evidence=state["all_evidence"],
        warnings=state["warnings"],
        duration_ms=state["duration_ms"],
        provider_used=state["provider_used"],
        model_used=state["model_used"],
        is_mock=state["is_mock"],
        data_mode="synthetic",
    )


# 3. Executive Business Dashboard Summary
@router.get("/dashboard/summary")
async def get_dashboard_summary():
    """Consolidated synthetic business metrics across all pharmaceutical domains."""
    sales = SalesService.get_ethical_sales_summary()
    pcd = SalesService.get_pcd_sales_summary()
    billing = BillingService.get_billing_summary()
    finance_debtors = FinanceService.get_debtors_aging_summary()
    procurement = ProcurementService.get_inventory_status()
    logistics = LogisticsService.get_shipments_summary()
    hr = HRService.get_milestones_and_batches()

    provider = get_llm_provider()
    p_status = await provider.health_check()

    return {
        "as_of_date": "2026-10-10",
        "data_mode": "synthetic",
        "ethical_sales": {
            "total_achieved_mtd": sales["total_achieved_mtd"],
            "total_target_mtd": sales["total_target_mtd"],
            "overall_achievement_pct": sales["overall_achievement_pct"],
            "top_performing_hq": sales["top_performing_hq"],
        },
        "pcd_sales": {
            "total_revenue": pcd["total_revenue"],
            "pending_orders": pcd["total_pending_orders_val"],
            "distributor_count": pcd["distributor_count"],
        },
        "billing": {
            "total_invoiced_net": billing["total_invoiced_net"],
            "total_gross_profit": billing["total_gross_profit"],
            "overall_gross_margin_pct": billing["overall_gross_margin_pct"],
            "low_margin_alerts_count": billing["low_margin_invoices_count"],
        },
        "finance": {
            "total_debtors_outstanding": finance_debtors["total_debtors_outstanding"],
            "critical_overdue_90d": finance_debtors["aging_buckets"]["days_over_90"],
            "critical_debtor_count": finance_debtors["critical_risk_count"],
        },
        "procurement": {
            "low_stock_skus_count": procurement["low_stock_skus_count"],
            "total_skus": procurement["total_skus"],
            "alerts": [item["name"] for item in procurement["low_stock_alerts"]],
        },
        "logistics": {
            "total_shipments": logistics["total_shipments"],
            "delayed_shipments_count": logistics["delayed_shipments_count"],
            "in_transit_count": logistics["in_transit_count"],
        },
        "hr": {
            "total_employees": hr["total_employees"],
            "birthdays_count": len(hr["birthdays_today"]),
            "anniversaries_count": len(hr["anniversaries_today"]),
        },
        "provider_status": p_status.model_dump(),
    }


# 4. Agent Directory & Manifests
@router.get("/agents", response_model=list[AgentManifest])
async def list_agents():
    """List all registered agents in the ecosystem with their declared manifests."""
    registry = get_agent_registry()
    return registry.list_agents()


@router.get("/agents/{agent_id}", response_model=AgentManifest)
async def get_agent(agent_id: str):
    """Retrieve detailed manifest for a specific agent."""
    registry = get_agent_registry()
    agent = registry.get_optional(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_id}' not found in registry.")
    return agent.manifest


# 5. Mock Integrations Status
@router.get("/integrations/status", response_model=list[IntegrationHealth])
async def get_integrations_status():
    """Simulated status of all external enterprise systems."""
    adapters = [
        MargERPAdapter(),
        OrderingPortalAdapter(),
        WhatsAppIngestionAdapter(),
        SocialMediaAdapter(),
        HRSystemAdapter(),
    ]
    return [adapter.get_health() for adapter in adapters]


# 6. Execution History
@router.get("/executions")
async def list_executions(limit: int = Query(50, ge=1, le=200)):
    """Retrieve execution history records."""
    try:
        session = get_session()
        rows = (
            session.query(ExecutionRecordModel)
            .order_by(ExecutionRecordModel.id.desc())
            .limit(limit)
            .all()
        )
        session.close()
        return [
            {
                "id": r.id,
                "execution_id": r.execution_id,
                "request_id": r.request_id,
                "correlation_id": r.correlation_id,
                "user_query": r.user_query,
                "status": r.workflow_status,
                "agents_invoked": r.agents_invoked,
                "duration_ms": r.duration_ms,
                "provider_mode": r.provider_mode,
                "model_identifier": r.model_identifier,
                "summary": r.summary,
                "evidence_count": r.evidence_count,
                "warnings": r.warnings,
                "created_at": r.created_at.isoformat() if r.created_at else None,
                "data_mode": r.data_mode,
            }
            for r in rows
        ]
    except Exception:
        return []


@router.get("/executions/{execution_id}")
async def get_execution_detail(execution_id: str):
    """Retrieve specific execution record by execution ID."""
    session = get_session()
    row = session.query(ExecutionRecordModel).filter_by(execution_id=execution_id).first()
    session.close()
    if not row:
        raise HTTPException(status_code=404, detail=f"Execution '{execution_id}' not found.")
    return {
        "execution_id": row.execution_id,
        "request_id": row.request_id,
        "correlation_id": row.correlation_id,
        "user_query": row.user_query,
        "status": row.workflow_status,
        "agents_invoked": row.agents_invoked,
        "duration_ms": row.duration_ms,
        "provider_mode": row.provider_mode,
        "model_identifier": row.model_identifier,
        "structured_data": row.structured_data,
        "summary": row.summary,
        "evidence_count": row.evidence_count,
        "warnings": row.warnings,
        "created_at": row.created_at.isoformat() if row.created_at else None,
    }


# 7. Observability Metrics & Events
@router.get("/observability/metrics", response_model=MetricSummary)
async def get_observability_metrics():
    """Retrieve real aggregated telemetry metrics."""
    provider = get_llm_provider()
    p_status = await provider.health_check()
    collector = get_metrics_collector()
    return collector.get_summary(
        provider_mode=provider.provider_name,
        provider_available=p_status.is_available,
    )


@router.get("/observability/events")
async def get_observability_events(limit: int = 50):
    """Retrieve recent structured trace events."""
    events = get_recent_events(limit)
    return [e.model_dump(mode="json") for e in events]


# 8. Evaluation Framework
@router.get("/evaluations")
async def list_evaluation_runs(limit: int = 20):
    """List recent evaluation suite runs."""
    try:
        session = get_session()
        rows = (
            session.query(EvaluationRunModel)
            .order_by(EvaluationRunModel.id.desc())
            .limit(limit)
            .all()
        )
        session.close()
        return [
            {
                "run_id": r.run_id,
                "dataset_version": r.dataset_version,
                "model_mode": r.model_mode,
                "model_identifier": r.model_identifier,
                "total_cases": r.total_cases,
                "passed_cases": r.passed_cases,
                "failed_cases": r.failed_cases,
                "pass_rate": r.pass_rate,
                "category_scores": r.category_scores,
                "regression_detected": r.regression_detected,
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
            for r in rows
        ]
    except Exception:
        return []


@router.post("/evaluations/run")
async def run_evaluation_suite(dataset_version: str = "v1.0.0"):
    """Execute complete evaluation suite against the active platform."""
    summary = await EvaluationRunner.run_evaluation_suite(dataset_version=dataset_version)
    return summary.model_dump(mode="json")


@router.get("/evaluations/{run_id}")
async def get_evaluation_run(run_id: str):
    """Retrieve full details of an evaluation run including per-case metric outcomes."""
    session = get_session()
    row = session.query(EvaluationRunModel).filter_by(run_id=run_id).first()
    session.close()
    if not row:
        raise HTTPException(status_code=404, detail=f"Evaluation run '{run_id}' not found.")
    return {
        "run_id": row.run_id,
        "dataset_version": row.dataset_version,
        "model_mode": row.model_mode,
        "model_identifier": row.model_identifier,
        "total_cases": row.total_cases,
        "passed_cases": row.passed_cases,
        "failed_cases": row.failed_cases,
        "pass_rate": row.pass_rate,
        "category_scores": row.category_scores,
        "results": row.results_json,
        "regression_detected": row.regression_detected,
        "created_at": row.created_at.isoformat() if row.created_at else None,
    }


# 9. Feedback & Continuous Improvement
@router.post("/feedback")
async def submit_feedback(req: FeedbackSubmitRequest):
    """Submit human reviewer feedback for an execution."""
    res = FeedbackService.submit_feedback(
        execution_id=req.execution_id,
        rating=req.rating,
        comment=req.comment,
        reviewer_id=req.reviewer_id,
    )
    return res.model_dump(mode="json")


@router.get("/feedback")
async def list_feedback():
    """Retrieve human feedback list."""
    records = FeedbackService.list_feedback()
    return [r.model_dump(mode="json") for r in records]


@router.get("/improvement-proposals")
async def list_proposals():
    """List continuous improvement proposals with their review and release status."""
    proposals = ProposalEngine.list_proposals()
    failure_analysis = FailureAnalyzer.analyze_recent_failures()
    return {
        "proposals": [p.model_dump(mode="json") for p in proposals],
        "failure_analysis": failure_analysis,
    }


@router.post("/improvement-proposals/{proposal_id}/review")
async def review_proposal(proposal_id: str, req: ReviewProposalRequest):
    """Review and approve/reject an improvement proposal (Human-in-the-loop gate)."""
    updated = ProposalEngine.review_proposal(
        proposal_id=proposal_id,
        decision=req.decision,
        reviewer_id=req.reviewer_id,
        comments=req.comments,
    )
    if not updated:
        raise HTTPException(status_code=404, detail=f"Proposal '{proposal_id}' not found.")
    return updated.model_dump(mode="json")


# 10. Simulated Approval Queue (Foundation Phase Demonstration)
@router.get("/approvals")
async def get_simulated_approvals():
    """Demonstration approval queue for high-risk write actions.

    All entries are strictly simulated demonstrations.
    """
    return [
        {
            "id": "APPR-PO-001",
            "type": "purchase_order_submission",
            "title": "Emergency Reorder PO: Amoxicillin-CV 625mg (1,850 units)",
            "requester": "Procurement Agent",
            "requested_at": "2026-10-10T09:30:00Z",
            "estimated_cost": "₹194,250.00",
            "supplier": "Zenith Pharma Labs",
            "status": "pending_executive_approval",
            "is_simulation": True,
            "simulation_notice": "DEMONSTRATION QUEUE ONLY: No actual financial or supplier transactions occur.",
        },
        {
            "id": "APPR-DISB-002",
            "type": "payment_disbursement",
            "title": "Scheduled Vendor Payment: Sterling Biocare",
            "requester": "Finance Agent",
            "requested_at": "2026-10-10T10:00:00Z",
            "estimated_cost": "₹410,000.00",
            "supplier": "Sterling Biocare",
            "status": "pending_executive_approval",
            "is_simulation": True,
            "simulation_notice": "DEMONSTRATION QUEUE ONLY: No actual banking transactions occur.",
        },
    ]


@router.post("/approvals/{approval_id}/action")
async def action_simulated_approval(approval_id: str, action: str = Query("approve")):
    """Simulate approving or rejecting a pending request."""
    return {
        "approval_id": approval_id,
        "action_taken": action,
        "is_simulation": True,
        "message": f"Simulated {action} recorded for {approval_id}. Foundation phase maintains zero-write isolation.",
    }
