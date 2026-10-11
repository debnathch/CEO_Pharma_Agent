"""Procurement & Inventory Specialist Agent."""

import time

from pharma_platform.business_services.procurement_service import ProcurementService
from pharma_platform.contracts.agent import (
    AgentCapability,
    AgentManifest,
    AgentRequest,
    AgentResult,
    AgentStatus,
    EvidenceReference,
    ImplementationStatus,
)
from pharma_platform.registry.base_agent import BaseAgent


class ProcurementAgent(BaseAgent):
    """Specialist agent for Inventory Analysis, Stock Out Alerts, and Reorder Recommendations."""

    def __init__(self) -> None:
        self._manifest = AgentManifest(
            agent_id="procurement",
            display_name="Procurement & Inventory Agent",
            description="Analyzes pharmaceutical stock levels, manufacturer lead times, and reorder alerts.",
            domain="Procurement",
            version="0.1.0",
            implementation_status=ImplementationStatus.PARTIAL,
            capabilities=[
                AgentCapability(
                    name="get_inventory_alerts",
                    description="Analyze stock across SKUs and identify products at or below safety reorder threshold.",
                    input_schema_name="InventoryQuery",
                    output_schema_name="InventoryAlertsResult",
                    is_implemented=True,
                ),
                AgentCapability(
                    name="compare_manufacturers",
                    description="Compare manufacturer quotation rates and lead times.",
                    input_schema_name="MfgCompareQuery",
                    output_schema_name="MfgCompareResult",
                    is_implemented=False,
                ),
                AgentCapability(
                    name="submit_purchase_order",
                    description="Submit formal purchase order to external manufacturer (Restricted write operation).",
                    input_schema_name="PORequest",
                    output_schema_name="POResult",
                    is_implemented=False,
                    requires_approval=True,
                ),
            ],
            required_permissions=["inventory:read"],
            supported_tools=["procurement_service"],
            readiness_info={"unit_tested": True, "eval_dataset": "v1.0.0"},
        )

    @property
    def manifest(self) -> AgentManifest:
        return self._manifest

    async def execute(self, request: AgentRequest) -> AgentResult:
        start_time = time.perf_counter()
        self.validate_request(request)

        if request.capability == "get_inventory_alerts":
            data = ProcurementService.get_inventory_status()
            duration_ms = (time.perf_counter() - start_time) * 1000.0

            alert_names = [item["name"] for item in data["low_stock_alerts"]]
            summary_msg = (
                f"Procurement audit detected {data['low_stock_skus_count']} critical low-stock items out of "
                f"{data['total_skus']} catalog SKUs. "
            )
            if alert_names:
                summary_msg += f"Immediate reorder needed for: {', '.join(alert_names)}."

            return AgentResult(
                execution_id=request.execution_id,
                agent_id=self.manifest.agent_id,
                version=self.manifest.version,
                status=AgentStatus.SUCCESS,
                structured_data=data,
                summary=summary_msg,
                evidence=[
                    EvidenceReference(
                        source_system="Marg ERP (Stock Master)",
                        entity_type="InventoryLevel",
                        entity_id="STOCK-AUDIT-ALL",
                        authoritative=True,
                        details={"low_stock_count": data["low_stock_skus_count"]},
                    )
                ],
                warnings=[
                    f"SKU {item['sku']} ({item['name']}) has only {item['current_stock']} units vs threshold {item['reorder_threshold']}!"
                    for item in data["low_stock_alerts"]
                ],
                duration_ms=round(duration_ms, 2),
                data_mode="synthetic",
                source_freshness="2026-10-10",
            )

        elif request.capability in ("compare_manufacturers", "submit_purchase_order"):
            duration_ms = (time.perf_counter() - start_time) * 1000.0
            return self.create_not_implemented_result(request, request.capability, duration_ms)

        raise ValueError(f"Unhandled capability '{request.capability}'")
