"""Deterministic HR Business Services (Birthdays, Anniversaries, Payslips)."""

from typing import Any

from pharma_platform.data.synthetic.fixtures import EMPLOYEES, PAYSLIP_BATCHES


class HRService:
    """Manages employee milestones, recruitment records, and payslip batches."""

    @staticmethod
    def get_milestones_and_batches() -> dict[str, Any]:
        """Identify employee milestones as of 2026-10-10."""
        # Synthetic date reference: 10-10
        birthdays_today = [e for e in EMPLOYEES if e["dob"].endswith("-10-10")]
        anniversaries_today = [e for e in EMPLOYEES if e["join_date"].endswith("-10-10")]

        return {
            "total_employees": len(EMPLOYEES),
            "birthdays_today": birthdays_today,
            "anniversaries_today": anniversaries_today,
            "payslip_batches": PAYSLIP_BATCHES,
        }
