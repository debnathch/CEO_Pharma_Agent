"""Improvement Proposal Engine and Controlled Release Workflow."""

import uuid
from datetime import datetime, timezone
from typing import Any, Optional

from pharma_platform.contracts.improvement import (
    FailureCategory,
    ImprovementProposal,
    ProposalStatus,
    ProposalType,
)
from pharma_platform.persistence.database import get_session
from pharma_platform.persistence.models import ImprovementProposalModel


class ProposalEngine:
    """Manages improvement proposals and controlled release gates."""

    @staticmethod
    def create_proposal(
        title: str,
        description: str,
        target_agent_id: str,
        proposal_type: ProposalType,
        failure_category: FailureCategory,
        rationale: str,
        proposed_changes: dict[str, Any],
    ) -> ImprovementProposal:
        proposal = ImprovementProposal(
            proposal_id=f"prop-{str(uuid.uuid4())[:8]}",
            title=title,
            description=description,
            target_agent_id=target_agent_id,
            proposal_type=proposal_type,
            failure_category=failure_category,
            rationale=rationale,
            proposed_changes=proposed_changes,
            status=ProposalStatus.DRAFT,
            created_at=datetime.now(timezone.utc),
        )

        try:
            session = get_session()
            model = ImprovementProposalModel(
                proposal_id=proposal.proposal_id,
                title=proposal.title,
                description=proposal.description,
                target_agent_id=proposal.target_agent_id,
                proposal_type=proposal.proposal_type.value,
                failure_category=proposal.failure_category.value,
                rationale=proposal.rationale,
                proposed_changes=proposal.proposed_changes,
                status=proposal.status.value,
            )
            session.add(model)
            session.commit()
            session.close()
        except Exception:
            pass

        return proposal

    @staticmethod
    def list_proposals() -> list[ImprovementProposal]:
        """List all proposals in the registry."""
        try:
            session = get_session()
            rows = session.query(ImprovementProposalModel).order_by(ImprovementProposalModel.id.desc()).all()
            session.close()
            if rows:
                return [
                    ImprovementProposal(
                        proposal_id=r.proposal_id,
                        title=r.title,
                        description=r.description,
                        target_agent_id=r.target_agent_id,
                        proposal_type=ProposalType(r.proposal_type),
                        failure_category=FailureCategory(r.failure_category),
                        rationale=r.rationale,
                        proposed_changes=r.proposed_changes or {},
                        status=ProposalStatus(r.status),
                        reviewed_by=r.reviewed_by,
                        review_comments=r.review_comments,
                        regression_suite_passed=r.regression_suite_passed,
                        created_at=r.created_at,
                    )
                    for r in rows
                ]
        except Exception:
            pass

        # Return default seed proposals if DB empty
        return [
            ImprovementProposal(
                proposal_id="prop-seed-01",
                title="Refine Prompt Grounding for Low-Margin Invoices",
                description="Include explicit formula definition for gross profit margin in Billing Agent system prompt.",
                target_agent_id="billing",
                proposal_type=ProposalType.PROMPT_REFINEMENT,
                failure_category=FailureCategory.DATA_INCONSISTENCY,
                rationale="Reviewer noted potential ambiguity in differentiating trade discount from scheme free-goods cost.",
                proposed_changes={
                    "prompt_clause": "Always state: Net Sales - (COGS + Scheme Cost) = Gross Profit.",
                    "version": "v1.1-candidate",
                },
                status=ProposalStatus.APPROVED,
                reviewed_by="Principal Architect",
                review_comments="Approved pending regression suite execution.",
                regression_suite_passed=True,
            ),
            ImprovementProposal(
                proposal_id="prop-seed-02",
                title="Expand Routing Keywords for PCD Sales Queries",
                description="Add 'franchisee', 'c&f', and 'stockist' to CEO classifier triggers for pcd_sales.",
                target_agent_id="pcd_sales",
                proposal_type=ProposalType.ROUTING_KEYWORD_UPDATE,
                failure_category=FailureCategory.ROUTING_MISCLASSIFICATION,
                rationale="User queries regarding 'Bengal stockist performance' previously defaulted to ethical sales.",
                proposed_changes={
                    "new_keywords": ["franchisee", "c&f", "stockist"],
                },
                status=ProposalStatus.UNDER_REVIEW,
                reviewed_by=None,
            ),
        ]

    @staticmethod
    def review_proposal(
        proposal_id: str,
        decision: str,  # "approved" or "rejected"
        reviewer_id: str,
        comments: str,
    ) -> Optional[ImprovementProposal]:
        """Update review status of a proposal."""
        new_status = ProposalStatus.APPROVED if decision == "approved" else ProposalStatus.REJECTED
        try:
            session = get_session()
            row = session.query(ImprovementProposalModel).filter_by(proposal_id=proposal_id).first()
            if row:
                row.status = new_status.value
                row.reviewed_by = reviewer_id
                row.review_comments = comments
                session.commit()
                res = ImprovementProposal(
                    proposal_id=row.proposal_id,
                    title=row.title,
                    description=row.description,
                    target_agent_id=row.target_agent_id,
                    proposal_type=ProposalType(row.proposal_type),
                    failure_category=FailureCategory(row.failure_category),
                    rationale=row.rationale,
                    proposed_changes=row.proposed_changes or {},
                    status=new_status,
                    reviewed_by=reviewer_id,
                    review_comments=comments,
                    regression_suite_passed=row.regression_suite_passed,
                    created_at=row.created_at,
                )
                session.close()
                return res
            session.close()
        except Exception:
            pass
        return None
