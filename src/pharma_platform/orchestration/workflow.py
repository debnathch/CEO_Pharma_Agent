"""CEO Bounded Orchestration Workflow Engine built with LangGraph."""

import asyncio
import re
import time
import uuid
from typing import Any, Optional, TypedDict

from langgraph.graph import END, StateGraph

from pharma_platform.contracts.agent import (
    AgentContext,
    AgentRequest,
    AgentResult,
    AgentStatus,
)
from pharma_platform.contracts.observability import EventType, ObservabilityEvent
from pharma_platform.observability.logger import emit_event
from pharma_platform.observability.metrics import get_metrics_collector
from pharma_platform.persistence.database import get_session
from pharma_platform.persistence.models import ExecutionRecordModel
from pharma_platform.providers.factory import get_llm_provider
from pharma_platform.registry.registry import get_agent_registry


class WorkflowState(TypedDict):
    """Execution state passed through the LangGraph bounded orchestration graph."""

    request_id: str
    execution_id: str
    correlation_id: str
    user_query: str
    context: dict[str, Any]
    intent: str
    selected_agent_invocations: list[dict[str, Any]]
    agent_results: list[dict[str, Any]]
    aggregated_data: dict[str, Any]
    all_evidence: list[dict[str, Any]]
    warnings: list[str]
    executive_summary: str
    provider_used: str
    model_used: str
    is_mock: bool
    status: str
    error: Optional[str]
    duration_ms: float


def classify_and_validate(state: WorkflowState) -> WorkflowState:
    """Classify user query and dynamically discover specialist agents via the registry."""
    q = state["user_query"].lower()
    selected: list[dict[str, Any]] = []
    intent = "general_query"

    emit_event(
        ObservabilityEvent(
            event_id=str(uuid.uuid4()),
            event_type=EventType.WORKFLOW_STARTED,
            request_id=state["request_id"],
            execution_id=state["execution_id"],
            correlation_id=state["correlation_id"],
            workflow_step="classify_and_validate",
        )
    )

    # 1. Daily Briefing / Comprehensive Overview
    if any(k in q for k in ["briefing", "daily", "overview", "executive summary", "status today", "dashboard"]):
        intent = "daily_briefing"
        selected = [
            {"agent_id": "ethical_sales", "capability": "get_hq_sales_summary", "params": {}},
            {"agent_id": "procurement", "capability": "get_inventory_alerts", "params": {}},
            {"agent_id": "finance", "capability": "get_debtors_aging", "params": {}},
            {"agent_id": "logistics", "capability": "get_shipments_status", "params": {}},
            {"agent_id": "hr", "capability": "get_milestones_and_payslips", "params": {}},
        ]

    # 2. PCD Franchise Sales (Check before HQ names so 'franchise' does not trigger 'ranchi')
    elif any(re.search(rf"\b{k}\b", q) for k in ["pcd", "franchise", "distributor"]):
        intent = "pcd_sales"
        selected.append({"agent_id": "pcd_sales", "capability": "get_pcd_sales_summary", "params": {}})

    # 3. Ethical Sales / HQ Performance
    elif any(re.search(rf"\b{k}\b", q) for k in ["ethical sales", "hq", "mr", "sales rep", "kolkata", "siliguri", "patna", "asansol", "ranchi"]):
        intent = "ethical_sales"
        # Check if specific HQ mentioned with word boundary
        for hq_name in ["kolkata", "siliguri", "patna", "asansol", "ranchi"]:
            if re.search(rf"\b{hq_name}\b", q):
                selected.append({
                    "agent_id": "ethical_sales",
                    "capability": "get_hq_detail",
                    "params": {"hq_name": hq_name},
                })
                break
        if not selected:
            selected.append({"agent_id": "ethical_sales", "capability": "get_hq_sales_summary", "params": {}})

    # 4. Inventory / Procurement / Stock
    elif any(k in q for k in ["procurement", "stock", "inventory", "reorder", "safety stock", "sku"]):
        intent = "procurement"
        selected.append({"agent_id": "procurement", "capability": "get_inventory_alerts", "params": {}})

    # 5. Billing / Gross Profit / Free Goods
    elif any(k in q for k in ["billing", "profit", "gross margin", "margin", "free goods", "sample", "invoice"]):
        intent = "billing"
        selected.append({"agent_id": "billing", "capability": "get_billing_summary", "params": {}})

    # 6. Finance / Debtors / Creditors
    elif any(k in q for k in ["debtor", "creditor", "finance", "overdue", "aging", "outstanding", "accounts"]):
        intent = "finance"
        selected.append({"agent_id": "finance", "capability": "get_debtors_aging", "params": {}})
        if "creditor" in q or "payable" in q:
            selected.append({"agent_id": "finance", "capability": "get_creditors_summary", "params": {}})

    # 7. Logistics / Shipments
    elif any(k in q for k in ["logistics", "shipment", "delivery", "dispatch", "delayed", "transporter", "lr"]):
        intent = "logistics"
        selected.append({"agent_id": "logistics", "capability": "get_shipments_status", "params": {}})

    # 8. Marketing
    elif any(k in q for k in ["marketing", "campaign", "social"]):
        intent = "marketing"
        selected.append({"agent_id": "marketing", "capability": "get_campaign_drafts", "params": {}})

    # 9. Product Launch / LBL
    elif any(k in q for k in ["launch", "lbl", "product card", "brochure", "pipeline"]):
        intent = "product_launch"
        selected.append({"agent_id": "product_launch", "capability": "get_launch_pipeline", "params": {}})

    # 10. HR
    elif any(k in q for k in ["hr", "employee", "birthday", "anniversary", "payslip", "recruitment"]):
        intent = "hr"
        selected.append({"agent_id": "hr", "capability": "get_milestones_and_payslips", "params": {}})

    else:
        # Default fallback to sales overview
        intent = "sales_fallback"
        selected.append({"agent_id": "ethical_sales", "capability": "get_hq_sales_summary", "params": {}})

    state["intent"] = intent
    state["selected_agent_invocations"] = selected
    return state


async def execute_specialists(state: WorkflowState) -> WorkflowState:
    """Invoke discovered specialist agents in parallel using the AgentRegistry."""
    from pharma_platform.agents.bootstrap import register_all_agents

    registry = get_agent_registry()
    if not registry.list_agents():
        register_all_agents()

    tasks = []

    for item in state["selected_agent_invocations"]:
        agent_id = item["agent_id"]
        capability = item["capability"]
        params = item.get("params", {})

        agent = registry.get_optional(agent_id)
        if not agent:
            continue

        emit_event(
            ObservabilityEvent(
                event_id=str(uuid.uuid4()),
                event_type=EventType.AGENT_SELECTED,
                request_id=state["request_id"],
                execution_id=state["execution_id"],
                correlation_id=state["correlation_id"],
                agent_id=agent_id,
                workflow_step=f"execute_{agent_id}:{capability}",
            )
        )

        agent_req = AgentRequest(
            request_id=state["request_id"],
            execution_id=f"{state['execution_id']}-{agent_id}",
            correlation_id=state["correlation_id"],
            capability=capability,
            parameters=params,
            context=AgentContext(**state["context"]),
        )
        tasks.append(agent.execute(agent_req))

    if tasks:
        results: list[AgentResult] = await asyncio.gather(*tasks, return_exceptions=True)
        converted_results = []
        for r in results:
            if isinstance(r, AgentResult):
                converted_results.append(r.model_dump())
            elif isinstance(r, Exception):
                converted_results.append({
                    "execution_id": state["execution_id"],
                    "agent_id": "unknown",
                    "version": "0.1.0",
                    "status": AgentStatus.FAILED.value,
                    "structured_data": {},
                    "summary": f"Agent execution raised error: {r}",
                    "evidence": [],
                    "warnings": [str(r)],
                    "error_details": {"error": str(r)},
                    "duration_ms": 0.0,
                    "data_mode": "synthetic",
                })
        state["agent_results"] = converted_results
    else:
        state["agent_results"] = []

    return state


def aggregate_and_ground(state: WorkflowState) -> WorkflowState:
    """Aggregate structured payloads, merge evidence chains, and collect warnings."""
    aggregated: dict[str, Any] = {}
    evidence: list[dict[str, Any]] = []
    warnings: list[str] = []
    has_partial = False
    has_failed = False

    for res in state["agent_results"]:
        agent_id = res.get("agent_id", "specialist")
        aggregated[agent_id] = res.get("structured_data", {})
        evidence.extend(res.get("evidence", []))
        warnings.extend(res.get("warnings", []))

        st = res.get("status")
        if st == AgentStatus.PARTIAL.value:
            has_partial = True
        elif st == AgentStatus.FAILED.value:
            has_failed = True

    state["aggregated_data"] = aggregated
    state["all_evidence"] = evidence
    state["warnings"] = list(dict.fromkeys(warnings))  # Deduplicate

    if has_failed:
        state["status"] = "partial" if has_partial or aggregated else "failed"
    elif has_partial:
        state["status"] = "partial"
    else:
        state["status"] = "success"

    return state


async def synthesize_executive_response(state: WorkflowState) -> WorkflowState:
    """Use the configured LLM provider to synthesize a grounded natural language executive response."""
    provider = get_llm_provider()

    # Formulate bounded grounded prompt containing strictly the verified synthetic data
    data_summary_snippets = []
    for res in state["agent_results"]:
        data_summary_snippets.append(f"[{res.get('agent_id')}]: {res.get('summary')}")

    prompt = (
        f"You are the CEO Master Intelligence Agent for a pharmaceutical enterprise.\n"
        f"User Query: {state['user_query']}\n"
        f"Verified Business Evidence:\n" + "\n".join(data_summary_snippets) + "\n\n"
        "Provide a concise, professional executive response based strictly on the evidence above."
    )

    llm_res = await provider.generate(prompt=prompt)

    state["provider_used"] = llm_res.provider_name
    state["model_used"] = llm_res.model_name
    state["is_mock"] = llm_res.is_mock

    # Deterministic fallback if provider failed or timed out
    if llm_res.error or not llm_res.text:
        fallback_parts = [res.get("summary") for res in state["agent_results"] if res.get("summary")]
        state["executive_summary"] = (
            "Executive Grounded Summary (Deterministic Fallback):\n"
            + "\n".join(f"• {part}" for part in fallback_parts)
        )
        if llm_res.error:
            state["warnings"].append(f"Provider '{llm_res.provider_name}' notice: {llm_res.error}")
    else:
        state["executive_summary"] = llm_res.text

    return state


def record_and_evaluate(state: WorkflowState) -> WorkflowState:
    """Persist execution record, emit metrics, and record trace completion."""
    invoked_agents = [r.get("agent_id") for r in state["agent_results"] if r.get("agent_id")]

    # Persist in DB
    try:
        session = get_session()
        record = ExecutionRecordModel(
            request_id=state["request_id"],
            execution_id=state["execution_id"],
            correlation_id=state["correlation_id"],
            user_query=state["user_query"],
            workflow_status=state["status"],
            agents_invoked=invoked_agents,
            duration_ms=state["duration_ms"],
            provider_mode=state["provider_used"],
            model_identifier=state["model_used"],
            structured_data=state["aggregated_data"],
            summary=state["executive_summary"],
            evidence_count=len(state["all_evidence"]),
            warnings=state["warnings"],
            error_category=state.get("error"),
            data_mode="synthetic",
        )
        session.add(record)
        session.commit()
        session.close()
    except Exception:
        pass

    # Update metrics
    collector = get_metrics_collector()
    collector.record_execution(
        agents_invoked=invoked_agents,
        status=state["status"],
        duration_ms=state["duration_ms"],
        is_success=state["status"] == "success",
    )

    emit_event(
        ObservabilityEvent(
            event_id=str(uuid.uuid4()),
            event_type=EventType.FINAL_RESPONSE_RETURNED,
            request_id=state["request_id"],
            execution_id=state["execution_id"],
            correlation_id=state["correlation_id"],
            status=state["status"],
            duration_ms=state["duration_ms"],
            provider=state["provider_used"],
            model=state["model_used"],
            workflow_step="completed",
        )
    )

    return state


def build_ceo_graph():
    """Build and compile the LangGraph StateGraph workflow."""
    workflow = StateGraph(WorkflowState)

    workflow.add_node("classify", classify_and_validate)
    workflow.add_node("execute_agents", execute_specialists)
    workflow.add_node("aggregate", aggregate_and_ground)
    workflow.add_node("synthesize", synthesize_executive_response)
    workflow.add_node("record", record_and_evaluate)

    workflow.set_entry_point("classify")
    workflow.add_edge("classify", "execute_agents")
    workflow.add_edge("execute_agents", "aggregate")
    workflow.add_edge("aggregate", "synthesize")
    workflow.add_edge("synthesize", "record")
    workflow.add_edge("record", END)

    return workflow.compile()


# Compiled singleton graph
_ceo_graph = build_ceo_graph()


async def run_ceo_workflow(
    user_query: str,
    context: Optional[dict[str, Any]] = None,
    correlation_id: Optional[str] = None,
) -> WorkflowState:
    """Execute the CEO orchestration graph end to end."""
    start_time = time.perf_counter()
    req_id = str(uuid.uuid4())[:8]
    exec_id = f"exec-{str(uuid.uuid4())[:8]}"
    corr_id = correlation_id or str(uuid.uuid4())

    initial_state: WorkflowState = {
        "request_id": req_id,
        "execution_id": exec_id,
        "correlation_id": corr_id,
        "user_query": user_query,
        "context": context or {"user_role": "CEO", "user_id": "exec-01"},
        "intent": "",
        "selected_agent_invocations": [],
        "agent_results": [],
        "aggregated_data": {},
        "all_evidence": [],
        "warnings": [],
        "executive_summary": "",
        "provider_used": "mock",
        "model_used": "none",
        "is_mock": True,
        "status": "pending",
        "error": None,
        "duration_ms": 0.0,
    }

    final_state = await _ceo_graph.ainvoke(initial_state)
    final_state["duration_ms"] = round((time.perf_counter() - start_time) * 1000.0, 2)
    # Run final record step with accurate duration
    record_and_evaluate(final_state)
    return final_state
