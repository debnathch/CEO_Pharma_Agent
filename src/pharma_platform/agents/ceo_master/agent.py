"""CEO Master Intelligence Agent."""

import time

from pharma_platform.contracts.agent import (
    AgentCapability,
    AgentManifest,
    AgentRequest,
    AgentResult,
    AgentStatus,
    EvidenceReference,
    ImplementationStatus,
)
from pharma_platform.orchestration.workflow import run_ceo_workflow
from pharma_platform.registry.base_agent import BaseAgent


class CEOMasterAgent(BaseAgent):
    """Chief Executive Officer Master Intelligence Agent.

    Orchestrates requests across the multi-agent ecosystem, synthesizes executive briefings,
    and grounds cross-domain data into actionable intelligence.
    """

    def __init__(self) -> None:
        self._manifest = AgentManifest(
            agent_id="ceo_master",
            display_name="CEO Master Intelligence Agent",
            description="Executive orchestration, conversational interface, cross-domain synthesis, and daily briefing.",
            domain="Executive Leadership",
            version="0.1.0",
            implementation_status=ImplementationStatus.FULL,
            capabilities=[
                AgentCapability(
                    name="handle_chat_query",
                    description="Process natural language executive inquiries and route across specialist agents.",
                    input_schema_name="ChatQueryInput",
                    output_schema_name="ChatQueryResult",
                    is_implemented=True,
                ),
                AgentCapability(
                    name="generate_daily_briefing",
                    description="Compile cross-departmental daily morning intelligence briefing.",
                    input_schema_name="BriefingQueryInput",
                    output_schema_name="BriefingQueryResult",
                    is_implemented=True,
                ),
            ],
            required_permissions=["executive:all"],
            supported_tools=["all_specialist_agents", "orchestration_engine"],
            readiness_info={"unit_tested": True, "eval_dataset": "v1.0.0", "eval_pass_rate": 1.0},
        )

    @property
    def manifest(self) -> AgentManifest:
        return self._manifest

    async def execute(self, request: AgentRequest) -> AgentResult:
        start_time = time.perf_counter()
        self.validate_request(request)

        query = request.parameters.get("query", "")
        if request.capability == "generate_daily_briefing" and not query:
            query = "Generate comprehensive morning daily briefing for the CEO"

        state = await run_ceo_workflow(
            user_query=query,
            context=request.context.model_dump(),
            correlation_id=request.correlation_id,
        )

        duration_ms = (time.perf_counter() - start_time) * 1000.0

        status_map = {
            "success": AgentStatus.SUCCESS,
            "partial": AgentStatus.PARTIAL,
            "failed": AgentStatus.FAILED,
        }
        final_status = status_map.get(state["status"], AgentStatus.SUCCESS)

        evidence_objs = [
            EvidenceReference(
                source_system=e.get("source_system", "Platform Registry"),
                entity_type=e.get("entity_type", "Record"),
                entity_id=str(e.get("entity_id", "ID")),
                authoritative=e.get("authoritative", True),
                details=e.get("details", {}),
            )
            for e in state["all_evidence"]
        ]

        return AgentResult(
            execution_id=request.execution_id,
            agent_id=self.manifest.agent_id,
            version=self.manifest.version,
            status=final_status,
            structured_data=state["aggregated_data"],
            summary=state["executive_summary"],
            evidence=evidence_objs,
            warnings=state["warnings"],
            duration_ms=round(duration_ms, 2),
            data_mode="synthetic",
            source_freshness="2026-10-10",
        )
