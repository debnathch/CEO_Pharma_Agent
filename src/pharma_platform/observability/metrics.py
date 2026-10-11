"""Observability Metrics Collection and Aggregation (Pure Python)."""

import math
from collections import defaultdict

from pharma_platform.contracts.observability import MetricSummary
from pharma_platform.persistence.database import get_session
from pharma_platform.persistence.models import ExecutionRecordModel


def _percentile(data: list[float], percentile: float) -> float:
    """Calculate percentile without external dependencies."""
    if not data:
        return 0.0
    s_data = sorted(data)
    k = (len(s_data) - 1) * (percentile / 100.0)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return float(s_data[int(k)])
    d0 = s_data[int(f)] * (c - k)
    d1 = s_data[int(c)] * (k - f)
    return float(d0 + d1)


class MetricsCollector:
    """Collects and reports real execution telemetry and metrics."""

    def __init__(self) -> None:
        self._latencies: list[float] = []
        self._invocations: dict[str, int] = defaultdict(int)
        self._agent_successes: dict[str, int] = defaultdict(int)

    def record_execution(
        self,
        agents_invoked: list[str],
        status: str,
        duration_ms: float,
        is_success: bool = True,
    ) -> None:
        self._latencies.append(duration_ms)
        if len(self._latencies) > 2000:
            self._latencies.pop(0)

        for agent in agents_invoked:
            self._invocations[agent] += 1
            if is_success:
                self._agent_successes[agent] += 1

    def get_summary(self, provider_mode: str = "mock", provider_available: bool = True) -> MetricSummary:
        """Compute aggregated metrics using both in-memory and persisted records."""
        try:
            session = get_session()
            records = session.query(ExecutionRecordModel).all()
            session.close()
        except Exception:
            records = []

        total_requests = len(records)
        successful = sum(1 for r in records if r.workflow_status == "success")
        partial = sum(1 for r in records if r.workflow_status == "partial")
        failed = sum(1 for r in records if r.workflow_status == "failed")

        latencies = [float(r.duration_ms) for r in records if r.duration_ms and r.duration_ms > 0]
        if not latencies and self._latencies:
            latencies = self._latencies

        avg_lat = round(sum(latencies) / len(latencies), 2) if latencies else 0.0
        p95_lat = round(_percentile(latencies, 95.0), 2) if latencies else 0.0

        invocations = defaultdict(int)
        successes = defaultdict(int)
        for r in records:
            agents = r.agents_invoked or []
            for a in agents:
                invocations[a] += 1
                if r.workflow_status == "success":
                    successes[a] += 1

        success_rates = {}
        for a, count in invocations.items():
            success_rates[a] = round((successes[a] / count * 100.0), 1) if count > 0 else 0.0

        return MetricSummary(
            total_requests=total_requests,
            successful_executions=successful,
            partial_executions=partial,
            failed_executions=failed,
            agent_invocation_counts=dict(invocations),
            agent_success_rates=success_rates,
            average_duration_ms=avg_lat,
            p95_duration_ms=p95_lat,
            provider_mode=provider_mode,
            provider_available=provider_available,
        )


_global_metrics = MetricsCollector()


def get_metrics_collector() -> MetricsCollector:
    return _global_metrics
