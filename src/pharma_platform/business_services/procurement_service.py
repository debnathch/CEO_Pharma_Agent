"""Deterministic Procurement and Inventory Risk Business Services."""

from typing import Any

from pharma_platform.data.synthetic.fixtures import PRODUCTS


class ProcurementService:
    """Calculates inventory levels, reorder thresholds, and manufacturer lead times."""

    @staticmethod
    def get_inventory_status() -> dict[str, Any]:
        """Identify critical low stock products and compute reorder recommendations."""
        low_stock_items = []
        adequate_stock_items = []

        for p in PRODUCTS:
            stock = p["stock_units"]
            threshold = p["reorder_threshold"]
            safety = p["safety_stock"]

            is_low_stock = stock <= threshold
            suggested_order_qty = max(0, (threshold + safety) - stock) if is_low_stock else 0

            item_info = {
                "sku": p["sku"],
                "name": p["name"],
                "category": p["category"],
                "manufacturer": p["manufacturer"],
                "current_stock": stock,
                "reorder_threshold": threshold,
                "safety_stock": safety,
                "is_low_stock": is_low_stock,
                "suggested_reorder_units": suggested_order_qty,
                "lead_time_days": p["lead_time_days"],
                "unit_cost": p["cost_price"],
                "estimated_reorder_cost": round(suggested_order_qty * p["cost_price"], 2),
            }

            if is_low_stock:
                low_stock_items.append(item_info)
            else:
                adequate_stock_items.append(item_info)

        return {
            "total_skus": len(PRODUCTS),
            "low_stock_skus_count": len(low_stock_items),
            "low_stock_alerts": low_stock_items,
            "adequate_stock_items": adequate_stock_items,
        }
