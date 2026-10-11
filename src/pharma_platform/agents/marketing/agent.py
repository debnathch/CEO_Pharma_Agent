"""Digital Marketing Specialist Agent."""

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
from pharma_platform.registry.base_agent import BaseAgent


class MarketingAgent(BaseAgent):
    """Specialist agent for Digital Marketing Campaigns, Healthcare Professional Content, and Simulated Engagement."""

    def __init__(self) -> None:
        self._manifest = AgentManifest(
            agent_id="marketing",
            display_name="Digital Marketing Agent",
            description="Assists in drafting medical promotional campaigns, physician digital engagement, and educational briefs.",
            domain="Marketing & Brand",
            version="0.1.0",
            implementation_status=ImplementationStatus.PARTIAL,
            capabilities=[
                AgentCapability(
                    name="get_campaign_drafts",
                    description="Retrieve active and proposed digital marketing campaigns.",
                    input_schema_name="CampaignQuery",
                    output_schema_name="CampaignDraftsResult",
                    is_implemented=True,
                ),
                AgentCapability(
                    name="publish_campaign_externally",
                    description="Publish marketing post to live social media channels (Restricted write operation).",
                    input_schema_name="PublishRequest",
                    output_schema_name="PublishResult",
                    is_implemented=False,
                    requires_approval=True,
                ),
            ],
            required_permissions=["marketing:read"],
            supported_tools=["marketing_service"],
            readiness_info={"unit_tested": True, "eval_dataset": "v1.0.0"},
        )

    @property
    def manifest(self) -> AgentManifest:
        return self._manifest

    async def execute(self, request: AgentRequest) -> AgentResult:
        start_time = time.perf_counter()
        self.validate_request(request)

        if request.capability == "get_campaign_drafts":
            # Synthetic draft campaigns
            campaigns = [
                {
                    "campaign_id": "CMP-2026-CARDIO",
                    "title": "World Heart Day Physician Education Series",
                    "focus_molecule": "Telmisartan 40mg",
                    "target_audience": "Consultant Cardiologists & Physicians",
                    "status": "draft_in_review",
                    "simulated_reach": 4500,
                    "external_publishing_enabled": False,
                },
                {
                    "campaign_id": "CMP-2026-RESP",
                    "title": "Monsoon Respiratory Alert & Anti-Allergy Guide",
                    "focus_molecule": "Montelukast 10mg + Levocetirizine 5mg",
                    "target_audience": "Pediatricians & Chest Physicians",
                    "status": "approved_internal",
                    "simulated_reach": 3200,
                    "external_publishing_enabled": False,
                },
            ]
            duration_ms = (time.perf_counter() - start_time) * 1000.0

            return AgentResult(
                execution_id=request.execution_id,
                agent_id=self.manifest.agent_id,
                version=self.manifest.version,
                status=AgentStatus.SUCCESS,
                structured_data={"campaigns": campaigns, "total_campaigns": len(campaigns)},
                summary=(
                    f"Identified {len(campaigns)} marketing campaigns staged in draft. "
                    f"Notice: All external publishing is disabled in the foundation environment."
                ),
                evidence=[
                    EvidenceReference(
                        source_system="Simulated Campaign Staging",
                        entity_type="CampaignStore",
                        entity_id="MKTG-STAGING-01",
                        authoritative=False,
                        details={"campaign_count": len(campaigns)},
                    )
                ],
                warnings=["External social media publishing is restricted and operates in sandbox mode."],
                duration_ms=round(duration_ms, 2),
                data_mode="synthetic",
                source_freshness="2026-10-10",
            )

        elif request.capability == "publish_campaign_externally":
            duration_ms = (time.perf_counter() - start_time) * 1000.0
            return self.create_not_implemented_result(request, "publish_campaign_externally", duration_ms)

        raise ValueError(f"Unhandled capability '{request.capability}'")
