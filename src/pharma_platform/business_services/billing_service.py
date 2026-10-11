"""Deterministic Billing and Gross Profit Business Services."""

from typing import Any

from pharma_platform.data.synthetic.fixtures import INVOICES


class BillingService:
    """Calculates billing, gross profit, margin %, and sample/free goods impact."""

    @staticmethod
    def calculate_invoice_profit(invoice: dict[str, Any]) -> dict[str, Any]:
        """Compute exact deterministic gross profit and margin percentage."""
        net = float(invoice["net_amount"])
        cogs = float(invoice["cost_of_goods_sold"])
        free_goods_cost = float(invoice.get("sample_scheme_goods_cost", 0.0))

        gross_profit = net - (cogs + free_goods_cost)
        margin_pct = (gross_profit / net * 100.0) if net > 0 else 0.0

        return {
            "invoice_no": invoice["invoice_no"],
            "net_amount": round(net, 2),
            "cost_of_goods_sold": round(cogs, 2),
            "free_goods_scheme_cost": round(free_goods_cost, 2),
            "gross_profit": round(gross_profit, 2),
            "gross_margin_pct": round(margin_pct, 2),
            "low_margin_warning": margin_pct < 15.0,
        }

    @classmethod
    def get_billing_summary(cls) -> dict[str, Any]:
        """Aggregate all billing records with total gross margin."""
        total_net = sum(inv["net_amount"] for inv in INVOICES)
        total_cogs = sum(inv["cost_of_goods_sold"] for inv in INVOICES)
        total_free_goods = sum(inv.get("sample_scheme_goods_cost", 0.0) for inv in INVOICES)
        total_gross_profit = total_net - (total_cogs + total_free_goods)
        overall_margin_pct = (total_gross_profit / total_net * 100.0) if total_net > 0 else 0.0

        analyzed_invoices = [cls.calculate_invoice_profit(inv) for inv in INVOICES]
        low_margin_invoices = [inv for inv in analyzed_invoices if inv["low_margin_warning"]]

        return {
            "total_invoiced_net": round(total_net, 2),
            "total_cogs": round(total_cogs, 2),
            "total_free_goods_cost": round(total_free_goods, 2),
            "total_gross_profit": round(total_gross_profit, 2),
            "overall_gross_margin_pct": round(overall_margin_pct, 2),
            "invoice_count": len(INVOICES),
            "low_margin_invoices_count": len(low_margin_invoices),
            "low_margin_alerts": low_margin_invoices,
            "invoices": analyzed_invoices,
        }
