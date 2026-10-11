"""Failure Analyzer diagnosing recurring error patterns from executions and feedback."""

from collections import defaultdict
from typing import Any

from pharma_platform.contracts.improvement import FailureCategory
from pharma_platform.persistence.database import get_session
from pharma_platform.persistence.models import ExecutionRecordModel, FeedbackRecordModel


class FailureAnalyzer:
    """Analyzes execution logs and reviewer feedback to isolate root failure modes."""

    @staticmethod
    def analyze_recent_failures(limit: int = 100) -> dict[str, Any]:
        """Aggregate failures across agents, error categories, and user feedback."""
        try:
            session = get_session()
            exec_rows = (
                session.query(ExecutionRecordModel)
                .filter(ExecutionRecordModel.workflow_status.in_(["partial", "failed"]))
                .order_by(ExecutionRecordModel.id.desc())
                .limit(limit)
                .all()
            )
            feedback_rows = (
                session.query(FeedbackRecordModel)
                .filter(FeedbackRecordModel.rating.in_(["incorrect", "incomplete", "unsupported"]))
                .limit(limit)
                .all()
            )
            session.close()
        except Exception:
            exec_rows = []
            feedback_rows = []

        category_counts: dict[str, int] = defaultdict(int)
        agent_failure_counts: dict[str, int] = defaultdict(int)
        diagnosed_issues: list[dict[str, Any]] = []

        for r in exec_rows:
            agents = r.agents_invoked or ["unrouted"]
            for a in agents:
                agent_failure_counts[a] += 1

            # Infer category
            warn_str = " ".join(r.warnings or []).lower()

            if "not implemented" in warn_str or "unsupported" in warn_str:
                cat = FailureCategory.UNSUPPORTED_CAPABILITY
            elif "unmapped" in warn_str or "missing" in warn_str:
                cat = FailureCategory.ROUTING_MISCLASSIFICATION
            elif "timeout" in warn_str or "connection" in warn_str:
                cat = FailureCategory.TIMEOUT_OR_UNAVAILABLE
            else:
                cat = FailureCategory.DATA_INCONSISTENCY

            category_counts[cat.value] += 1
            diagnosed_issues.append({
                "execution_id": r.execution_id,
                "query": r.user_query,
                "agents": agents,
                "category": cat.value,
                "summary": r.summary[:120] if r.summary else "",
            })

        for fb in feedback_rows:
            if fb.rating == "unsupported":
                category_counts[FailureCategory.UNSUPPORTED_CAPABILITY.value] += 1
            elif fb.rating == "incorrect":
                category_counts[FailureCategory.DATA_INCONSISTENCY.value] += 1
            elif fb.rating == "incomplete":
                category_counts[FailureCategory.MISSING_EVIDENCE.value] += 1

        return {
            "total_failures_analyzed": len(exec_rows),
            "negative_feedback_count": len(feedback_rows),
            "category_breakdown": dict(category_counts),
            "agent_breakdown": dict(agent_failure_counts),
            "diagnosed_issues": diagnosed_issues[:10],
        }
