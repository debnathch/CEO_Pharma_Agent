"""Deterministic Sales Business Services (Ethical HQ and PCD)."""

from typing import Any

from pharma_platform.data.synthetic.fixtures import ETHICAL_SALES_HQ, PCD_SALES


class SalesService:
    """Provides deterministic sales calculations and aggregations."""

    @staticmethod
    def get_ethical_sales_summary() -> dict[str, Any]:
        """Calculate total target, achievement, and weighted achievement %."""
        total_target = sum(hq["target_mtd"] for hq in ETHICAL_SALES_HQ)
        total_achieved = sum(hq["achieved_mtd"] for hq in ETHICAL_SALES_HQ)
        achievement_pct = round((total_achieved / total_target * 100), 2) if total_target > 0 else 0.0

        hq_breakdown = []
        for hq in ETHICAL_SALES_HQ:
            pct = round((hq["achieved_mtd"] / hq["target_mtd"] * 100), 2) if hq["target_mtd"] > 0 else 0.0
            hq_breakdown.append({
                "hq_id": hq["hq_id"],
                "hq_name": hq["hq_name"],
                "target": hq["target_mtd"],
                "achieved": hq["achieved_mtd"],
                "achievement_pct": pct,
                "growth_yoy_pct": hq["growth_yoy_pct"],
                "top_rep": hq["top_performing_rep"],
            })

        # Sort by achievement percentage descending
        hq_breakdown.sort(key=lambda x: x["achievement_pct"], reverse=True)

        return {
            "total_target_mtd": total_target,
            "total_achieved_mtd": total_achieved,
            "overall_achievement_pct": achievement_pct,
            "hq_count": len(ETHICAL_SALES_HQ),
            "top_performing_hq": hq_breakdown[0]["hq_name"] if hq_breakdown else None,
            "lowest_performing_hq": hq_breakdown[-1]["hq_name"] if hq_breakdown else None,
            "hqs": hq_breakdown,
        }

    @staticmethod
    def get_hq_sales_by_id_or_name(query: str) -> dict[str, Any] | None:
        """Find a specific HQ by ID or partial name."""
        q = query.lower()
        for hq in ETHICAL_SALES_HQ:
            if q in hq["hq_id"].lower() or q in hq["hq_name"].lower():
                pct = round((hq["achieved_mtd"] / hq["target_mtd"] * 100), 2) if hq["target_mtd"] > 0 else 0.0
                return {
                    **hq,
                    "achievement_pct": pct,
                }
        return None

    @staticmethod
    def get_pcd_sales_summary() -> dict[str, Any]:
        """Calculate PCD network total revenue, pending orders, and active distributors."""
        total_revenue = sum(pcd["total_sales_val"] for pcd in PCD_SALES)
        total_pending = sum(pcd["pending_order_val"] for pcd in PCD_SALES)
        total_orders = sum(pcd["orders_count"] for pcd in PCD_SALES)

        return {
            "total_revenue": total_revenue,
            "total_pending_orders_val": total_pending,
            "total_orders_count": total_orders,
            "distributor_count": len(PCD_SALES),
            "distributors": PCD_SALES,
        }
