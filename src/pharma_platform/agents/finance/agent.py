"""Finance & Accounts Specialist Agent."""

import time

from pharma_platform.business_services.finance_service import FinanceService
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


class FinanceAgent(BaseAgent):
    """Specialist agent for Debtors, Creditors, Aging Buckets, and Working Capital."""

    def __init__(self) -> None:
        self._manifest = AgentManifest(
            agent_id="finance",
            display_name="Finance & Accounts Agent",
            description="Analyzes customer debtor aging, critical overdue balances, and trade creditors.",
            domain="Finance & Accounts",
            version="0.1.0",
            implementation_status=ImplementationStatus.PARTIAL,
            capabilities=[
                AgentCapability(
                    name="get_debtors_aging",
                    description="Analyze debtor outstanding categorized into 0-30, 31-60, 61-90, and >90 day buckets.",
                    input_schema_name="DebtorAgingQuery",
                    output_schema_name="DebtorAgingResult",
                    is_implemented=True,
                ),
                AgentCapability(
                    name="get_creditors_summary",
                    description="Summarize pending supplier and manufacturer payables.",
                    input_schema_name="CreditorQuery",
                    output_schema_name="CreditorSummaryResult",
                    is_implemented=True,
                ),
                AgentCapability(
                    name="execute_payment_run",
                    description="Trigger banking disbursement (High-risk restricted write operation).",
                    input_schema_name="PaymentRunInput",
                    output_schema_name="PaymentRunResult",
                    is_implemented=False,
                    requires_approval=True,
                ),
            ],
            required_permissions=["finance:read"],
            supported_tools=["finance_service"],
            readiness_info={"unit_tested": True, "eval_dataset": "v1.0.0"},
        )

    @property
    def manifest(self) -> AgentManifest:
        return self._manifest

    async def execute(self, request: AgentRequest) -> AgentResult:
        start_time = time.perf_counter()
        self.validate_request(request)

        if request.capability == "get_debtors_aging":
            data = FinanceService.get_debtors_aging_summary()
            duration_ms = (time.perf_counter() - start_time) * 1000.0

            warnings = []
            if data["critical_risk_count"] > 0:
                warnings.append(
                    f"Action required: {data['critical_risk_count']} account(s) have balances overdue beyond 90 days "
                    f"or exceed authorized credit limits."
                )

            return AgentResult(
                execution_id=request.execution_id,
                agent_id=self.manifest.agent_id,
                version=self.manifest.version,
                status=AgentStatus.SUCCESS,
                structured_data=data,
                summary=(
                    f"Total outstanding debtors: ₹{data['total_debtors_outstanding']:,.2f}. "
                    f"Aging breakdown: 0-30d: ₹{data['aging_buckets']['days_0_to_30']:,.2f}, "
                    f"31-60d: ₹{data['aging_buckets']['days_31_to_60']:,.2f}, "
                    f"61-90d: ₹{data['aging_buckets']['days_61_to_90']:,.2f}, "
                    f">90d Overdue: ₹{data['aging_buckets']['days_over_90']:,.2f}."
                ),
                evidence=[
                    EvidenceReference(
                        source_system="Marg ERP (Accounts Receivable)",
                        entity_type="DebtorAgingLedger",
                        entity_id="AR-DEBTORS-AGING",
                        authoritative=True,
                        details={"debtor_count": data["debtor_count"]},
                    )
                ],
                warnings=warnings,
                duration_ms=round(duration_ms, 2),
                data_mode="synthetic",
                source_freshness="2026-10-10",
            )

        elif request.capability == "get_creditors_summary":
            data = FinanceService.get_creditors_summary()
            duration_ms = (time.perf_counter() - start_time) * 1000.0
            return AgentResult(
                execution_id=request.execution_id,
                agent_id=self.manifest.agent_id,
                version=self.manifest.version,
                status=AgentStatus.SUCCESS,
                structured_data=data,
                summary=(
                    f"Total trade creditors payable: ₹{data['total_creditors_payable']:,.2f} across "
                    f"{data['creditor_count']} vendor manufacturers."
                ),
                evidence=[
                    EvidenceReference(
                        source_system="Marg ERP (Accounts Payable)",
                        entity_type="CreditorLedger",
                        entity_id="AP-CREDITORS-ALL",
                        authoritative=True,
                        details=data,
                    )
                ],
                warnings=[],
                duration_ms=round(duration_ms, 2),
                data_mode="synthetic",
                source_freshness="2026-10-10",
            )

        elif request.capability == "execute_payment_run":
            duration_ms = (time.perf_counter() - start_time) * 1000.0
            return self.create_not_implemented_result(request, "execute_payment_run", duration_ms)

        raise ValueError(f"Unhandled capability '{request.capability}'")
