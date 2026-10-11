"""Deterministic Finance Business Services (Debtors and Creditors)."""

from typing import Any

from pharma_platform.data.synthetic.fixtures import CREDITORS, DEBTORS


class FinanceService:
    """Calculates debtor aging, overdue risk, and creditor obligations."""

    @staticmethod
    def get_debtors_aging_summary() -> dict[str, Any]:
        """Aggregate debtor balances across standardized aging buckets."""
        total_outstanding = sum(d["total_outstanding"] for d in DEBTORS)
        bucket_0_30 = sum(d["bucket_0_30"] for d in DEBTORS)
        bucket_31_60 = sum(d["bucket_31_60"] for d in DEBTORS)
        bucket_61_90 = sum(d["bucket_61_90"] for d in DEBTORS)
        bucket_over_90 = sum(d["bucket_over_90"] for d in DEBTORS)

        critical_debtors = [
            d for d in DEBTORS if d["bucket_over_90"] > 0 or d["total_outstanding"] > d["credit_limit"]
        ]

        return {
            "total_debtors_outstanding": round(total_outstanding, 2),
            "aging_buckets": {
                "days_0_to_30": round(bucket_0_30, 2),
                "days_31_to_60": round(bucket_31_60, 2),
                "days_61_to_90": round(bucket_61_90, 2),
                "days_over_90": round(bucket_over_90, 2),
            },
            "debtor_count": len(DEBTORS),
            "critical_risk_count": len(critical_debtors),
            "critical_risk_debtors": critical_debtors,
            "all_debtors": DEBTORS,
        }

    @staticmethod
    def get_creditors_summary() -> dict[str, Any]:
        """Aggregate trade creditors payable."""
        total_payable = sum(c["total_payable"] for c in CREDITORS)
        return {
            "total_creditors_payable": round(total_payable, 2),
            "creditor_count": len(CREDITORS),
            "creditors": CREDITORS,
        }
