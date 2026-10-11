"""Deterministic Logistics and Dispatch Tracking Business Services."""

from typing import Any

from pharma_platform.data.synthetic.fixtures import SHIPMENTS


class LogisticsService:
    """Tracks shipment delivery statuses, carriers, and transport delays."""

    @staticmethod
    def get_shipments_summary() -> dict[str, Any]:
        """Aggregate shipments by delivery status and flag active transit delays."""
        delayed = [s for s in SHIPMENTS if s.get("is_delayed", False)]
        in_transit = [s for s in SHIPMENTS if "in_transit" in s.get("status", "")]
        delivered = [s for s in SHIPMENTS if s.get("status") == "delivered"]

        return {
            "total_shipments": len(SHIPMENTS),
            "in_transit_count": len(in_transit),
            "delivered_count": len(delivered),
            "delayed_shipments_count": len(delayed),
            "delayed_shipments": delayed,
            "all_shipments": SHIPMENTS,
        }
