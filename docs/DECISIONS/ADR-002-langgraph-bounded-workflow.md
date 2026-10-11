# ADR-002: LangGraph Bounded Workflow vs Autonomous ReAct Planning

## Status
Accepted

## Context
The CEO Master Agent needs to orchestrate specialist agents to fulfill executive inquiries. Autonomous LLM-driven multi-agent loops (e.g. unrestrained AutoGen or ReAct planners) frequently suffer from infinite loops, unpredictable token consumption, non-deterministic routing, hallucinated sub-tasks, and difficulty enforcing business policy boundaries.

## Decision
We select **LangGraph StateGraph** to implement an explicit, bounded state-machine workflow:
`classify_and_validate -> execute_specialists -> aggregate_and_ground -> synthesize_executive_response -> record_and_evaluate`.
The state machine is deterministic, bounded, and typed. Agent discovery occurs through the `AgentRegistry`, and specialists are invoked in parallel where read-only dependencies permit.

## Alternatives Considered
1. **Unbounded Autonomous ReAct Agent Loop**:
   - *Rejected*: In enterprise pharmaceutical contexts, unbounded LLM loops risk hallucinatory recursive tool invocation, high latency, and policy violations.
2. **Hardcoded procedural script without graph abstraction**:
   - *Rejected*: Lacks standardized state checkpointing, transition observability, and future capability to add conditional human-in-the-loop review nodes.

## Consequences & Trade-offs
- **Positive**:
  - Deterministic routing guarantees predictable execution times.
  - State is strictly typed via `TypedDict` and Pydantic schemas.
  - Transparent step-by-step observability and trace emission at each graph node.
- **Negative / Trade-offs**:
  - Routing requires maintaining domain keyword and capability mappings rather than relying purely on zero-shot model reasoning.
