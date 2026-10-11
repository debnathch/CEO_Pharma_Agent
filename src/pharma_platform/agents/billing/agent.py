"""Billing & Gross Profit Specialist Agent."""

import time

from pharma_platform.business_services.billing_service import BillingService
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


class BillingAgent(BaseAgent):
    """Specialist agent for Billing, Invoices, Gross Profit, and Free Goods Analysis."""

    def __init__(self) -> None:
        self._manifest = AgentManifest(
            agent_id="billing",
            display_name="Billing & Gross Profit Agent",
            description="Performs deterministic billing calculations, gross profit audit, and sample/bonus goods analysis.",
            domain="Billing & Commercial",
            version="0.1.0",
            implementation_status=ImplementationStatus.PARTIAL,
            capabilities=[
                AgentCapability(
                    name="get_billing_summary",
                    description="Calculate total billed revenue, COGS, free goods costs, and overall gross margin.",
                    input_schema_name="BillingQuery",
                    output_schema_name="BillingSummaryResult",
                    is_implemented=True,
                ),
                AgentCapability(
                    name="analyze_free_goods_leakage",
                    description="Detect margin erosion caused by unapproved physician samples or excessive bonus goods.",
                    input_schema_name="LeakageQuery",
                    output_schema_name="LeakageResult",
                    is_implemented=False,
                ),
            ],
            required_permissions=["billing:read"],
            supported_tools=["billing_service"],
            readiness_info={"unit_tested": True, "eval_dataset": "v1.0.0"},
        )

    @property
    def manifest(self) -> AgentManifest:
        return self._manifest

    async def execute(self, request: AgentRequest) -> AgentResult:
        start_time = time.perf_counter()
        self.validate_request(request)

        if request.capability == "get_billing_summary":
            data = BillingService.get_billing_summary()
            duration_ms = (time.perf_counter() - start_time) * 1000.0

            warnings = []
            if data["low_margin_invoices_count"] > 0:
                warnings.append(
                    f"Identified {data['low_margin_invoices_count']} invoice(s) with gross margin below 15% threshold."
                )

            return AgentResult(
                execution_id=request.execution_id,
                agent_id=self.manifest.agent_id,
                version=self.manifest.version,
                status=AgentStatus.SUCCESS,
                structured_data=data,
                summary=(
                    f"Total billed net value: ₹{data['total_invoiced_net']:,.2f} with total gross profit of "
                    f"₹{data['total_gross_profit']:,.2f} (Overall Gross Margin: {data['overall_gross_margin_pct']}%). "
                    f"Total promotional/scheme free-goods cost absorbed: ₹{data['total_free_goods_cost']:,.2f}."
                ),
                evidence=[
                    EvidenceReference(
                        source_system="Marg ERP (Billing Module)",
                        entity_type="InvoiceRegister",
                        entity_id="INV-REGISTER-OCT2026",
                        authoritative=True,
                        details={"invoice_count": data["invoice_count"]},
                    )
                ],
                warnings=warnings,
                duration_ms=round(duration_ms, 2),
                data_mode="synthetic",
                source_freshness="2026-10-10",
            )

        elif request.capability == "analyze_free_goods_leakage":
            duration_ms = (time.perf_counter() - start_time) * 1000.0
            return self.create_not_implemented_result(request, "analyze_free_goods_leakage", duration_ms)

        raise ValueError(f"Unhandled capability '{request.capability}'")
