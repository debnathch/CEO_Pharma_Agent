# Observability, Tracing & Telemetry Architecture

## 1. Architectural Overview

Observability in the Bengal Remedies ecosystem is vendor-neutral, lightweight, and structured. It encompasses three core pillars:
1. **Structured JSON Logs** with unified correlation IDs.
2. **Distributed Tracing & Spans** compatible with OpenTelemetry concepts.
3. **Execution Telemetry & Aggregated Metrics**.

---

## 2. Event Taxonomy

The system emits standardized `ObservabilityEvent` records:

| Event Type | Emitted By | Description |
| :--- | :--- | :--- |
| `request_accepted` | API Boundary | Inbound HTTP request validated and assigned IDs |
| `workflow_started` | LangGraph Engine | Graph execution initialized |
| `agent_selected` | Orchestrator | Specialist agent discovered and queued |
| `agent_execution_started`| BaseAgent | Specialist capability starts execution |
| `tool_invoked` | Tool Registry | Business service method called |
| `provider_call_completed`| LLM Provider | Inference completed with latency & token metrics |
| `provider_call_failed` | LLM Provider | Inference failed or timed out (honest reporting) |
| `final_response_returned`| Orchestrator | Execution completed and response returned |
| `evaluation_completed` | EvaluationRunner | Test suite run finalized |

---

## 3. Structured Log Format

Logs are formatted as single-line JSON on stdout by `StructuredJsonFormatter`:

```json
{
  "timestamp": "2026-10-11T05:14:23.240102+00:00",
  "level": "INFO",
  "logger": "pharma.observability",
  "message": "Observability event: agent_selected (info)",
  "correlation_id": "b2c5ab81-2177-4f26-a1e4-06d9aa23a4c2",
  "request_id": "54088d82",
  "execution_id": "exec-92faf801",
  "agent_id": "ethical_sales",
  "event_type": "agent_selected",
  "duration_ms": null
}
```

---

## 4. Telemetry Metrics Collected

Available at `GET /api/v1/observability/metrics`:
- `total_requests`: Total executions run through the platform.
- `successful_executions`: Executions completed with full grounded evidence.
- `partial_executions`: Executions completed with partial results or unmapped entities.
- `failed_executions`: Executions encountering unhandled errors.
- `average_duration_ms`: Mean execution latency across all requests.
- `p95_duration_ms`: 95th percentile latency (pure Python calculation without heavy external libraries).
- `agent_invocation_counts`: Per-agent call frequency.
- `agent_success_rates`: Per-agent completion reliability percentage.
- `provider_mode`: Active provider identifier (`mock` or `ollama`).
- `provider_available`: Current live health of inference runtime.
