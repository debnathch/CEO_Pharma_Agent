# ADR-008: Observability Design with Correlation IDs, Structured Logs, and Tracing

## Status
Accepted

## Context
Debugging multi-agent systems requires tracking a user prompt as it routes through the orchestrator, agent discovery, specialist agent invocation, tool execution, and LLM synthesis. Traditional unstructured string logging makes it difficult to associate downstream errors with original requests or analyze latency bottlenecks.

## Decision
We implement a vendor-neutral observability architecture:
1. **Correlation IDs**: Propagated across the request lifecycle (`correlation_id`, `request_id`, `execution_id`).
2. **Structured JSON Logs**: Formatted with standard fields (`timestamp`, `correlation_id`, `agent_id`, `event_type`, `duration_ms`).
3. **OpenTelemetry-Compatible Trace Spans**: `TraceContext` and `trace_span` abstractions managing span hierarchies.
4. **Persistent Execution Records**: Complete telemetry saved to `ExecutionRecordModel` for historical audit.
5. **Real-time Telemetry Metrics**: `MetricsCollector` tracking execution counts, p95 latencies, and agent success rates.

## Alternatives Considered
1. **Third-Party SaaS Observability (DataDog, LangSmith, New Relic)**:
   - *Rejected for foundation*: Creates external network and commercial subscription dependencies.
2. **Standard Python `print()` statements**:
   - *Rejected*: Inadequate for enterprise auditing, correlation, and automated parsing.

## Consequences & Trade-offs
- **Positive**:
  - Full traceability across every agent execution without vendor lock-in.
  - Exposes dedicated `/api/v1/observability/metrics` and `/events` endpoints for the UI.
- **Negative / Trade-offs**:
  - In-memory event buffer is bounded (1000 events) in lightweight dev mode; persistent DB queries are used for historical trends.
