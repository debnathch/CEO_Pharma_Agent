"""Ethical Sales Specialist Agent."""

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


class EthicalSalesAgent(BaseAgent):
    """Specialist agent for Ethical Pharmaceutical Sales organized by HQ."""

    def __init__(self) -> None:
        self._manifest = AgentManifest(
            agent_id="ethical_sales",
            display_name="Ethical Pharmaceutical Sales Agent",
            description="Analyzes HQ-wise sales, medical representative performance, and doctor coverage.",
            domain="Ethical Sales",
            version="0.1.0",
            implementation_status=ImplementationStatus.PARTIAL,
            capabilities=[
                AgentCapability(
                    name="get_hq_sales_summary",
                    description="Retrieve MTD sales targets, achievements, and performance across all HQs.",
                    input_schema_name="HQSalesQuery",
                    output_schema_name="HQSalesSummary",
                    is_implemented=True,
                ),
                AgentCapability(
                    name="get_hq_detail",
                    description="Retrieve detailed sales metrics for a specific HQ by name or code.",
                    input_schema_name="HQDetailQuery",
                    output_schema_name="HQDetailResult",
                    is_implemented=True,
                ),
                AgentCapability(
                    name="ingest_field_reports",
                    description="Ingest doctor call reports and daily activity from MRs.",
                    input_schema_name="FieldReportInput",
                    output_schema_name="FieldReportResult",
                    is_implemented=False,  # Planned for next phase
                ),
            ],
            required_permissions=["sales:read"],
            supported_tools=["sales_service"],
            readiness_info={"unit_tested": True, "eval_dataset": "v1.0.0"},
        )

    @property
    def manifest(self) -> AgentManifest:
        return self._manifest

    async def execute(self, request: AgentRequest) -> AgentResult:
        start_time = time.perf_counter()
        self.validate_request(request)

        if request.capability == "get_hq_sales_summary":
            data = SalesService.get_ethical_sales_summary()
            duration_ms = (time.perf_counter() - start_time) * 1000.0
            return AgentResult(
                execution_id=request.execution_id,
                agent_id=self.manifest.agent_id,
                version=self.manifest.version,
                status=AgentStatus.SUCCESS,
                structured_data=data,
                summary=(
                    f"Ethical Sales MTD Achievement is {data['overall_achievement_pct']}% "
                    f"(₹{data['total_achieved_mtd']:,.2f} achieved vs ₹{data['total_target_mtd']:,.2f} target). "
                    f"Top HQ: {data['top_performing_hq']}. Lowest HQ: {data['lowest_performing_hq']}."
                ),
                evidence=[
                    EvidenceReference(
                        source_system="Marg ERP (Sales Ledger)",
                        entity_type="HQSalesLedger",
                        entity_id="ETHICAL-HQ-ALL",
                        authoritative=True,
                        details={"hq_count": data["hq_count"]},
                    )
                ],
                warnings=[],
                duration_ms=round(duration_ms, 2),
                data_mode="synthetic",
                source_freshness="2026-10-10",
            )

        elif request.capability == "get_hq_detail":
            hq_query = request.parameters.get("hq_name", "")
            data = SalesService.get_hq_sales_by_id_or_name(hq_query)
            duration_ms = (time.perf_counter() - start_time) * 1000.0
            if not data:
                return AgentResult(
                    execution_id=request.execution_id,
                    agent_id=self.manifest.agent_id,
                    version=self.manifest.version,
                    status=AgentStatus.PARTIAL,
                    structured_data={"query": hq_query},
                    summary=f"No ethical sales HQ matching '{hq_query}' was found in synthetic records.",
                    evidence=[],
                    warnings=[f"Unmapped HQ query '{hq_query}'."],
                    duration_ms=round(duration_ms, 2),
                    data_mode="synthetic",
                )

            return AgentResult(
                execution_id=request.execution_id,
                agent_id=self.manifest.agent_id,
                version=self.manifest.version,
                status=AgentStatus.SUCCESS,
                structured_data=data,
                summary=(
                    f"HQ {data['hq_name']} achieved {data['achievement_pct']}% of MTD target "
                    f"(₹{data['achieved_mtd']:,.2f} vs target ₹{data['target_mtd']:,.2f}). "
                    f"Top performing MR: {data['top_performing_rep']}."
                ),
                evidence=[
                    EvidenceReference(
                        source_system="Marg ERP (Sales Ledger)",
                        entity_type="HQRecord",
                        entity_id=data["hq_id"],
                        authoritative=True,
                        details=data,
                    )
                ],
                warnings=[],
                duration_ms=round(duration_ms, 2),
                data_mode="synthetic",
                source_freshness="2026-10-10",
            )

        elif request.capability == "ingest_field_reports":
            duration_ms = (time.perf_counter() - start_time) * 1000.0
            return self.create_not_implemented_result(request, "ingest_field_reports", duration_ms)

        raise ValueError(f"Unhandled capability '{request.capability}'")
