"""Contract tests verifying all 10 specialist agents conform to AgentManifest and AgentResult contracts."""

import pytest

from pharma_platform.agents.bootstrap import register_all_agents
from pharma_platform.contracts.agent import (
    AgentManifest,
    AgentRequest,
    AgentResult,
    AgentStatus,
)
from pharma_platform.registry.registry import get_agent_registry


@pytest.fixture(autouse=True)
def setup_agents():
    register_all_agents()


REQUIRED_AGENT_IDS = [
    "ceo_master",
    "ethical_sales",
    "pcd_sales",
    "procurement",
    "billing",
    "finance",
    "logistics",
    "marketing",
    "product_launch",
    "hr",
]


def test_all_ten_agents_registered():
    registry = get_agent_registry()
    manifests = registry.list_agents()
    registered_ids = {m.agent_id for m in manifests}

    for req_id in REQUIRED_AGENT_IDS:
        assert req_id in registered_ids, f"Agent '{req_id}' missing from registry!"


def test_all_manifests_conform_to_contract():
    registry = get_agent_registry()
    for agent_id in REQUIRED_AGENT_IDS:
        agent = registry.get(agent_id)
        manifest = agent.manifest
        assert isinstance(manifest, AgentManifest)
        assert manifest.agent_id == agent_id
        assert manifest.display_name
        assert manifest.domain
        assert manifest.version == "0.1.0"
        assert len(manifest.capabilities) > 0

        # Verify capabilities
        for cap in manifest.capabilities:
            assert cap.name
            assert cap.description
            assert cap.input_schema_name
            assert cap.output_schema_name


@pytest.mark.asyncio
async def test_specialist_implemented_and_unimplemented_contracts():
    registry = get_agent_registry()

    for agent_id in REQUIRED_AGENT_IDS:
        if agent_id == "ceo_master":
            continue

        agent = registry.get(agent_id)
        for cap in agent.manifest.capabilities:
            req = AgentRequest(
                request_id="test-req-01",
                execution_id=f"test-exec-{agent_id}",
                correlation_id="test-corr-01",
                capability=cap.name,
                parameters={},
            )

            result = await agent.execute(req)
            assert isinstance(result, AgentResult)
            assert result.agent_id == agent_id
            assert result.version == "0.1.0"
            assert result.data_mode == "synthetic"

            if cap.is_implemented:
                assert result.status in (AgentStatus.SUCCESS, AgentStatus.PARTIAL)
                assert result.summary
            else:
                # Truthful reporting of unimplemented capabilities!
                assert result.status == AgentStatus.NOT_IMPLEMENTED
                assert "not currently implement" in result.summary


def test_undeclared_capability_rejected():
    registry = get_agent_registry()
    agent = registry.get("ethical_sales")
    req = AgentRequest(
        request_id="test-req-01",
        execution_id="test-exec-undeclared",
        correlation_id="test-corr-01",
        capability="arbitrary_undeclared_capability",
        parameters={},
    )
    with pytest.raises(ValueError, match="not declared"):
        agent.validate_request(req)
