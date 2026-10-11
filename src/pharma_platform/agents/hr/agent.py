"""Human Resources & Talent Specialist Agent."""

import time

from pharma_platform.business_services.hr_service import HRService
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


class HRAgent(BaseAgent):
    """Specialist agent for Employee Milestones, Recruitment Intake, and Payslip Workflow Staging."""

    def __init__(self) -> None:
        self._manifest = AgentManifest(
            agent_id="hr",
            display_name="Human Resources Agent",
            description="Manages staff milestones, announcements, recruitment pipeline, and payslip disbursement workflows.",
            domain="Human Resources",
            version="0.1.0",
            implementation_status=ImplementationStatus.PARTIAL,
            capabilities=[
                AgentCapability(
                    name="get_milestones_and_payslips",
                    description="Retrieve employee birthdays, work anniversaries, and payslip batch staging status.",
                    input_schema_name="HRMilestoneQuery",
                    output_schema_name="HRMilestoneResult",
                    is_implemented=True,
                ),
                AgentCapability(
                    name="transmit_employee_payslips",
                    description="Bulk email/WhatsApp encrypted employee payslips (Restricted write operation).",
                    input_schema_name="TransmitPayslipRequest",
                    output_schema_name="TransmitPayslipResult",
                    is_implemented=False,
                    requires_approval=True,
                ),
            ],
            required_permissions=["hr:read"],
            supported_tools=["hr_service"],
            readiness_info={"unit_tested": True, "eval_dataset": "v1.0.0"},
        )

    @property
    def manifest(self) -> AgentManifest:
        return self._manifest

    async def execute(self, request: AgentRequest) -> AgentResult:
        start_time = time.perf_counter()
        self.validate_request(request)

        if request.capability == "get_milestones_and_payslips":
            data = HRService.get_milestones_and_batches()
            duration_ms = (time.perf_counter() - start_time) * 1000.0

            bday_names = [e["name"] for e in data["birthdays_today"]]
            anni_names = [e["name"] for e in data["anniversaries_today"]]

            summary_parts = []
            if bday_names:
                summary_parts.append(f"Birthdays today: {', '.join(bday_names)}")
            if anni_names:
                summary_parts.append(f"Work anniversaries today: {', '.join(anni_names)}")
            if not summary_parts:
                summary_parts.append("No employee milestones registered for today.")

            return AgentResult(
                execution_id=request.execution_id,
                agent_id=self.manifest.agent_id,
                version=self.manifest.version,
                status=AgentStatus.SUCCESS,
                structured_data=data,
                summary=f"HR Milestones: {'; '.join(summary_parts)}. Total employees on roster: {data['total_employees']}.",
                evidence=[
                    EvidenceReference(
                        source_system="Synthetic HR Records",
                        entity_type="EmployeeRoster",
                        entity_id="HR-ROSTER-2026",
                        authoritative=True,
                        details={"employee_count": data["total_employees"]},
                    )
                ],
                warnings=["Transmission of real employee documents and actual payslip release is disabled."],
                duration_ms=round(duration_ms, 2),
                data_mode="synthetic",
                source_freshness="2026-10-10",
            )

        elif request.capability == "transmit_employee_payslips":
            duration_ms = (time.perf_counter() - start_time) * 1000.0
            return self.create_not_implemented_result(request, "transmit_employee_payslips", duration_ms)

        raise ValueError(f"Unhandled capability '{request.capability}'")
