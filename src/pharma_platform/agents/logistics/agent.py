"""Logistics & Supply Chain Specialist Agent."""

import time

from pharma_platform.business_services.logistics_service import LogisticsService
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


class LogisticsAgent(BaseAgent):
    """Specialist agent for Dispatches, Shipments, Transporters, and Delivery Tracking."""

    def __init__(self) -> None:
        self._manifest = AgentManifest(
            agent_id="logistics",
            display_name="Logistics & Delivery Tracking Agent",
            description="Monitors dispatches from warehouse, tracking consignments, and detecting shipment delays.",
            domain="Logistics & Supply Chain",
            version="0.1.0",
            implementation_status=ImplementationStatus.PARTIAL,
            capabilities=[
                AgentCapability(
                    name="get_shipments_status",
                    description="Audit active dispatches, delivered orders, and flag transit delays with carrier reasons.",
                    input_schema_name="LogisticsQuery",
                    output_schema_name="LogisticsSummaryResult",
                    is_implemented=True,
                ),
                AgentCapability(
                    name="reroute_delayed_shipment",
                    description="Dispatch emergency stock via alternate airline or surface courier.",
                    input_schema_name="RerouteRequest",
                    output_schema_name="RerouteResult",
                    is_implemented=False,
                    requires_approval=True,
                ),
            ],
            required_permissions=["logistics:read"],
            supported_tools=["logistics_service"],
            readiness_info={"unit_tested": True, "eval_dataset": "v1.0.0"},
        )

    @property
    def manifest(self) -> AgentManifest:
        return self._manifest

    async def execute(self, request: AgentRequest) -> AgentResult:
        start_time = time.perf_counter()
        self.validate_request(request)

        if request.capability == "get_shipments_status":
            data = LogisticsService.get_shipments_summary()
            duration_ms = (time.perf_counter() - start_time) * 1000.0

            warnings = []
            if data["delayed_shipments_count"] > 0:
                for s in data["delayed_shipments"]:
                    warnings.append(
                        f"Shipment {s['shipment_id']} (LR: {s['lr_number']}) to {s['destination_hq']} is DELAYED: {s.get('delay_reason', 'Transit hold')}."
                    )

            return AgentResult(
                execution_id=request.execution_id,
                agent_id=self.manifest.agent_id,
                version=self.manifest.version,
                status=AgentStatus.SUCCESS,
                structured_data=data,
                summary=(
                    f"Logistics status: {data['total_shipments']} active shipments monitored "
                    f"({data['delivered_count']} delivered, {data['in_transit_count']} in transit, "
                    f"{data['delayed_shipments_count']} delayed)."
                ),
                evidence=[
                    EvidenceReference(
                        source_system="Transporter Dispatch Manifest",
                        entity_type="ConsignmentRegister",
                        entity_id="DISPATCH-2026-OCT",
                        authoritative=True,
                        details={"shipment_count": data["total_shipments"]},
                    )
                ],
                warnings=warnings,
                duration_ms=round(duration_ms, 2),
                data_mode="synthetic",
                source_freshness="2026-10-10",
            )

        elif request.capability == "reroute_delayed_shipment":
            duration_ms = (time.perf_counter() - start_time) * 1000.0
            return self.create_not_implemented_result(request, "reroute_delayed_shipment", duration_ms)

        raise ValueError(f"Unhandled capability '{request.capability}'")
