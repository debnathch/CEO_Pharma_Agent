# CEO Bounded Orchestration Architecture

## 1. Architectural Philosophy

The CEO Master Agent acts as the central executive conductor for Bengal Remedies. Rather than delegating queries to an unbounded, unpredictable autonomous planning loop, the orchestration engine executes an explicit, bounded **LangGraph StateGraph**.

Key tenets:
1. **Bounded State Machine**: Fixed, auditable transitions prevent infinite agent loops and unbounded token expenditure.
2. **Dynamic Registry Discovery**: Agents are discovered by capability from `AgentRegistry`, eliminating monolithic `if/elif` trees.
3. **Parallel Specialist Invocation**: Independent read-only domain queries (e.g. Sales, Logistics, Finance) execute concurrently via `asyncio.gather`.
4. **Evidence & Citation Grounding**: All numerical and factual claims are strictly grounded in structured outputs returned by verified business services.
5. **Deterministic Fallback**: If local LLM inference times out or fails, the orchestrator falls back to a deterministic synthesis of verified evidence without failing the request.

---

## 2. State Machine Specification

The state is typed via `WorkflowState`:

```python
class WorkflowState(TypedDict):
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
```

### Graph Nodes:
- **`classify`** (`classify_and_validate`): Parses user intent using word-boundary pattern matching and extracts required agent capabilities from the registry. Emits `WORKFLOW_STARTED`.
- **`execute_agents`** (`execute_specialists`): Emits `AGENT_SELECTED` events and concurrently invokes all selected agents asynchronously. Handles exceptions defensively.
- **`aggregate`** (`aggregate_and_ground`): Merges structured payloads, collects authoritative evidence references, and aggregates domain warnings.
- **`synthesize`** (`synthesize_executive_response`): Builds a constrained prompt strictly containing verified data and calls the configured `LLMProvider`. Triggers deterministic bulleted fallback if the provider fails.
- **`record`** (`record_and_evaluate`): Persists `ExecutionRecordModel` in the database, updates telemetry metrics in `MetricsCollector`, and emits `FINAL_RESPONSE_RETURNED`.

---

## 3. Parallel Execution Example: Daily Morning Briefing

When the user queries `"Give me the CEO daily morning briefing"`, the classifier targets five independent domains concurrently:
1. `ethical_sales.get_hq_sales_summary`
2. `procurement.get_inventory_alerts`
3. `finance.get_debtors_aging`
4. `logistics.get_shipments_status`
5. `hr.get_milestones_and_payslips`

These 5 queries execute in parallel in under 15ms total, aggregate evidence from Marg ERP, Transporter Manifests, and HR Records, and synthesize a unified morning briefing.
