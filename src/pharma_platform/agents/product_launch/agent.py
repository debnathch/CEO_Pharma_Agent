"""Product Launch & LBL (Leave Behind Literature) Specialist Agent."""

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


class ProductLaunchAgent(BaseAgent):
    """Specialist agent for New Product Introduction, Product Cards, and LBL Drafts."""

    def __init__(self) -> None:
        self._manifest = AgentManifest(
            agent_id="product_launch",
            display_name="Product Launch & LBL Agent",
            description="Assists in drafting product cards and Leave Behind Literature (LBL) with strict regulatory disclaimers.",
            domain="Medical Affairs & Product Management",
            version="0.1.0",
            implementation_status=ImplementationStatus.PARTIAL,
            capabilities=[
                AgentCapability(
                    name="get_launch_pipeline",
                    description="Retrieve upcoming molecule launches and drafting status of marketing literature.",
                    input_schema_name="LaunchQuery",
                    output_schema_name="LaunchPipelineResult",
                    is_implemented=True,
                ),
                AgentCapability(
                    name="generate_lbl_draft",
                    description="Draft an LBL brochure for doctors (Unapproved draft requiring medical committee sign-off).",
                    input_schema_name="LBLDraftQuery",
                    output_schema_name="LBLDraftResult",
                    is_implemented=True,
                ),
            ],
            required_permissions=["product:read"],
            supported_tools=["product_service"],
            readiness_info={"unit_tested": True, "eval_dataset": "v1.0.0"},
        )

    @property
    def manifest(self) -> AgentManifest:
        return self._manifest

    async def execute(self, request: AgentRequest) -> AgentResult:
        start_time = time.perf_counter()
        self.validate_request(request)

        regulatory_warning = (
            "IMPORTANT REGULATORY DISCLAIMER: This content is an internal draft and is NOT medically, "
            "legally, or regulatorily approved by DCGI or any regulatory health authority. "
            "Mandatory medical-legal review required prior to physician dissemination."
        )

        if request.capability == "get_launch_pipeline":
            launches = [
                {
                    "project_id": "LNCH-2026-TEL-CHLOR",
                    "molecule": "Telmisartan 40mg + Chlorthalidone 12.5mg Tablets",
                    "indication": "Stage II Essential Hypertension",
                    "target_launch_quarter": "Q1 2027",
                    "product_card_status": "draft_in_review",
                    "lbl_brochure_status": "drafting",
                    "regulatory_approval_status": "pending_cdsco_clearance",
                }
            ]
            duration_ms = (time.perf_counter() - start_time) * 1000.0
            return AgentResult(
                execution_id=request.execution_id,
                agent_id=self.manifest.agent_id,
                version=self.manifest.version,
                status=AgentStatus.SUCCESS,
                structured_data={"launches": launches, "count": len(launches)},
                summary=f"Product pipeline has {len(launches)} active launch project staged in draft.",
                evidence=[
                    EvidenceReference(
                        source_system="Product Launch Registry",
                        entity_type="PipelineRecord",
                        entity_id="LNCH-2026-TEL-CHLOR",
                        authoritative=False,
                        details={"launches": launches},
                    )
                ],
                warnings=[regulatory_warning],
                duration_ms=round(duration_ms, 2),
                data_mode="synthetic",
                source_freshness="2026-10-10",
            )

        elif request.capability == "generate_lbl_draft":
            draft = {
                "headline": "Target Beyond Pressure: Dual Synergy for 24-Hour BP Control",
                "brand_tentative_name": "BEN-TELCHLOR 40/12.5",
                "key_highlights": [
                    "Sustained 24-hour arterial control with smooth night-time dip restoration",
                    "Chlorthalidone offers proven cardiovascular mortality reduction over hydrochlorothiazide",
                    "Once-daily compliance-friendly blister packaging",
                ],
                "dosage_form": "Bilayered tablet",
                "medical_disclaimer": regulatory_warning,
            }
            duration_ms = (time.perf_counter() - start_time) * 1000.0
            return AgentResult(
                execution_id=request.execution_id,
                agent_id=self.manifest.agent_id,
                version=self.manifest.version,
                status=AgentStatus.SUCCESS,
                structured_data=draft,
                summary="Generated preliminary LBL draft for Telmisartan + Chlorthalidone.",
                evidence=[],
                warnings=[regulatory_warning],
                duration_ms=round(duration_ms, 2),
                data_mode="synthetic",
            )

        raise ValueError(f"Unhandled capability '{request.capability}'")
