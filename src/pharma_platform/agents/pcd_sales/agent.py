"""PCD (Propaganda Cum Distribution) Sales Specialist Agent."""

import time

from pharma_platform.business_services.sales_service import SalesService
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


class PCDSalesAgent(BaseAgent):
    """Specialist agent for PCD / Franchise Pharmaceutical Network."""

    def __init__(self) -> None:
        self._manifest = AgentManifest(
            agent_id="pcd_sales",
            display_name="PCD Franchise Sales Agent",
            description="Manages PCD franchise distribution, distributor performance, and pending franchise orders.",
            domain="PCD Distribution",
            version="0.1.0",
            implementation_status=ImplementationStatus.PARTIAL,
            capabilities=[
                AgentCapability(
                    name="get_pcd_sales_summary",
                    description="Retrieve consolidated PCD revenue, order count, and distributor standings.",
                    input_schema_name="PCDSummaryQuery",
                    output_schema_name="PCDSummaryResult",
                    is_implemented=True,
                ),
                AgentCapability(
                    name="analyze_distributor_trends",
                    description="Perform deep trend analysis for franchise territories.",
                    input_schema_name="PCDTrendQuery",
                    output_schema_name="PCDTrendResult",
                    is_implemented=False,
                ),
            ],
            required_permissions=["pcd:read"],
            supported_tools=["sales_service"],
            readiness_info={"unit_tested": True, "eval_dataset": "v1.0.0"},
        )

    @property
    def manifest(self) -> AgentManifest:
        return self._manifest

    async def execute(self, request: AgentRequest) -> AgentResult:
        start_time = time.perf_counter()
        self.validate_request(request)

        if request.capability == "get_pcd_sales_summary":
            data = SalesService.get_pcd_sales_summary()
            duration_ms = (time.perf_counter() - start_time) * 1000.0
            return AgentResult(
                execution_id=request.execution_id,
                agent_id=self.manifest.agent_id,
                version=self.manifest.version,
                status=AgentStatus.SUCCESS,
                structured_data=data,
                summary=(
                    f"Consolidated PCD franchise network generated ₹{data['total_revenue']:,.2f} across "
                    f"{data['distributor_count']} distributors with {data['total_orders_count']} total orders. "
                    f"Pending order pipeline: ₹{data['total_pending_orders_val']:,.2f}."
                ),
                evidence=[
                    EvidenceReference(
                        source_system="Ordering Portal (http://bengalremedies.com:9000)",
                        entity_type="FranchiseOrderStream",
                        entity_id="PCD-ALL",
                        authoritative=True,
                        details={"distributor_count": data["distributor_count"]},
                    )
                ],
                warnings=[],
                duration_ms=round(duration_ms, 2),
                data_mode="synthetic",
                source_freshness="2026-10-10",
            )

        elif request.capability == "analyze_distributor_trends":
            duration_ms = (time.perf_counter() - start_time) * 1000.0
            return self.create_not_implemented_result(request, "analyze_distributor_trends", duration_ms)

        raise ValueError(f"Unhandled capability '{request.capability}'")
