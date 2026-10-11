# Specialist Agent Development & Onboarding Guide

This guide demonstrates how to create, register, test, and evaluate a new specialist agent in the Bengal Remedies ecosystem without modifying existing agent code or rewriting conditional branches in the CEO Master Agent.

---

## 1. The 10-Step Onboarding Workflow

1. **Define the Agent Contract**: Inherit from `BaseAgent`.
2. **Declare Manifest & Capabilities**: Populate `AgentManifest`, version, capabilities, and required permissions.
3. **Connect to Business Services**: Implement deterministic domain calculations in `src/pharma_platform/business_services/`.
4. **Implement Truthful Capability Execution**:
   - For working capabilities: return `AgentStatus.SUCCESS` with structured data, summary, and evidence references.
   - For planned/unimplemented capabilities: return `self.create_not_implemented_result()`.
5. **Register in Bootstrap**: Add the instance to `src/pharma_platform/agents/bootstrap.py`.
6. **Add Synthetic Fixtures**: Provide realistic fixtures in `data/synthetic/fixtures.py`.
7. **Write Unit Tests**: Verify manifest compliance, capability routing, and calculation accuracy.
8. **Write Contract Tests**: Verify schema validation and rejection of undeclared capabilities.
9. **Add Evaluation Test Cases**: Add cases to `src/pharma_platform/evaluation/dataset.py`.
10. **Run Regression Suite**: Validate that `EvaluationRunner` passes with zero regressions.

---

## 2. Walkthrough Example: `RegulatoryComplianceAgent`

### Step 1: Create the Agent Class
Create `src/pharma_platform/agents/regulatory/agent.py`:

```python
import time
from pharma_platform.registry.base_agent import BaseAgent
from pharma_platform.contracts.agent import (
    AgentManifest, AgentCapability, AgentRequest, AgentResult,
    AgentStatus, EvidenceReference, ImplementationStatus
)

class RegulatoryComplianceAgent(BaseAgent):
    """Specialist agent auditing DCGI / CDSCO drug compliance and license expiries."""

    def __init__(self) -> None:
        self._manifest = AgentManifest(
            agent_id="regulatory_compliance",
            display_name="Regulatory & Compliance Agent",
            description="Audits manufacturing drug licenses, batch release certifications, and CDSCO compliance.",
            domain="Quality & Regulatory",
            version="0.1.0",
            implementation_status=ImplementationStatus.PARTIAL,
            capabilities=[
                AgentCapability(
                    name="audit_license_expiries",
                    description="Audit manufacturing plant licenses expiring within 90 days.",
                    input_schema_name="LicenseQuery",
                    output_schema_name="LicenseAuditResult",
                    is_implemented=True,
                ),
                AgentCapability(
                    name="file_cdsco_form",
                    description="Submit regulatory dossier to CDSCO portal (Restricted write operation).",
                    input_schema_name="DossierInput",
                    output_schema_name="DossierResult",
                    is_implemented=False,
                    requires_approval=True,
                ),
            ],
            required_permissions=["regulatory:read"],
            supported_tools=["regulatory_service"],
        )

    @property
    def manifest(self) -> AgentManifest:
        return self._manifest

    async def execute(self, request: AgentRequest) -> AgentResult:
        start_time = time.perf_counter()
        self.validate_request(request)

        if request.capability == "audit_license_expiries":
            data = {
                "active_licenses": 14,
                "expiring_soon_count": 1,
                "expiring_licenses": [
                    {
                        "license_no": "DL-WB-2021-9941",
                        "facility": "Bengal Remedies Mfg Plant 1",
                        "valid_till": "2026-12-15",
                        "days_remaining": 66,
                    }
                ],
            }
            duration_ms = (time.perf_counter() - start_time) * 1000.0
            return AgentResult(
                execution_id=request.execution_id,
                agent_id=self.manifest.agent_id,
                version=self.manifest.version,
                status=AgentStatus.SUCCESS,
                structured_data=data,
                summary="Regulatory audit: 1 manufacturing license expiring within 90 days (DL-WB-2021-9941).",
                evidence=[
                    EvidenceReference(
                        source_system="Regulatory License Master",
                        entity_type="DrugLicense",
                        entity_id="DL-WB-2021-9941",
                        authoritative=True,
                        details=data,
                    )
                ],
                warnings=["Renewal application must be filed 60 days before expiry."],
                duration_ms=round(duration_ms, 2),
                data_mode="synthetic",
            )

        elif request.capability == "file_cdsco_form":
            duration_ms = (time.perf_counter() - start_time) * 1000.0
            return self.create_not_implemented_result(request, "file_cdsco_form", duration_ms)

        raise ValueError(f"Unhandled capability '{request.capability}'")
```

### Step 2: Register in Bootstrap
In `src/pharma_platform/agents/bootstrap.py`:
```python
from pharma_platform.agents.regulatory.agent import RegulatoryComplianceAgent

def register_all_agents():
    # ...
    registry.register(RegulatoryComplianceAgent())
```

### Step 3: Add Evaluation Test Case
In `src/pharma_platform/evaluation/dataset.py`:
```python
EvaluationCase(
    case_id="EVAL-REG-01",
    name="Regulatory License Expiry Audit",
    category=EvaluationCategory.TASK_COMPLETION,
    target_agent="regulatory_compliance",
    user_query="Are any manufacturing drug licenses expiring soon?",
    expected_agents_routed=["regulatory_compliance"],
    expected_status="success",
    required_keywords=["DL-WB-2021-9941", "expiring"],
    tags=["regulatory", "compliance"],
)
```

### Step 4: Verification
Run the regression suite:
```bash
pytest tests/
```
The new agent is now active, discoverable, observable, and evaluated without modifying any existing agents.
