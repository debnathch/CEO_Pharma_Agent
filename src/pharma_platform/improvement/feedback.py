"""Feedback collection and storage for continuous improvement."""

import uuid
from datetime import datetime, timezone

from pharma_platform.contracts.improvement import FeedbackRating, FeedbackRecord
from pharma_platform.persistence.database import get_session
from pharma_platform.persistence.models import FeedbackRecordModel


class FeedbackService:
    """Manages human reviewer and user feedback records."""

    @staticmethod
    def submit_feedback(
        execution_id: str,
        rating: FeedbackRating,
        comment: str = "",
        reviewer_id: str = "reviewer-01",
    ) -> FeedbackRecord:
        record = FeedbackRecord(
            feedback_id=f"fb-{str(uuid.uuid4())[:8]}",
            execution_id=execution_id,
            rating=rating,
            comment=comment,
            reviewer_id=reviewer_id,
            timestamp=datetime.now(timezone.utc),
        )

        try:
            session = get_session()
            db_model = FeedbackRecordModel(
                feedback_id=record.feedback_id,
                execution_id=record.execution_id,
                rating=record.rating.value,
                comment=record.comment,
                reviewer_id=record.reviewer_id,
            )
            session.add(db_model)
            session.commit()
            session.close()
        except Exception:
            pass

        return record

    @staticmethod
    def list_feedback(limit: int = 50) -> list[FeedbackRecord]:
        """Retrieve recent feedback records."""
        try:
            session = get_session()
            rows = (
                session.query(FeedbackRecordModel)
                .order_by(FeedbackRecordModel.id.desc())
                .limit(limit)
                .all()
            )
            session.close()
            return [
                FeedbackRecord(
                    feedback_id=r.feedback_id,
                    execution_id=r.execution_id,
                    rating=FeedbackRating(r.rating),
                    comment=r.comment,
                    reviewer_id=r.reviewer_id,
                    timestamp=r.created_at,
                )
                for r in rows
            ]
        except Exception:
            return []
