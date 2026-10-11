"""Unit tests for AgentRegistry and LLMProvider abstraction."""

import pytest

from pharma_platform.agents.billing import BillingAgent
from pharma_platform.agents.ethical_sales import EthicalSalesAgent
from pharma_platform.providers.hosted_provider import HostedLLMProvider
from pharma_platform.providers.mock_provider import MockLLMProvider
from pharma_platform.providers.ollama_provider import OllamaLLMProvider
from pharma_platform.registry.registry import AgentRegistry


def test_agent_registry_duplicate_rejection():
    registry = AgentRegistry()
    agent1 = EthicalSalesAgent()
    agent2 = EthicalSalesAgent()

    registry.register(agent1)
    with pytest.raises(ValueError, match="already registered"):
        registry.register(agent2)


def test_agent_registry_lookup_and_filtering():
    registry = AgentRegistry()
    registry.register(EthicalSalesAgent())
    registry.register(BillingAgent())

    assert len(registry.list_agents()) == 2
    assert registry.get("ethical_sales") is not None
    assert registry.get("billing") is not None

    with pytest.raises(KeyError, match="not registered"):
        registry.get("unknown_agent")

    # Find by domain
    sales_agents = registry.find_by_domain("Ethical Sales")
    assert len(sales_agents) == 1
    assert sales_agents[0].manifest.agent_id == "ethical_sales"


@pytest.mark.asyncio
async def test_mock_llm_provider():
    provider = MockLLMProvider()
    health = await provider.health_check()
    assert health.is_available is True
    assert health.is_mock is True

    res = await provider.generate("Give me an executive sales overview")
    assert res.is_mock is True
    assert "Sales" in res.text
    assert res.duration_ms >= 0.0


@pytest.mark.asyncio
async def test_ollama_provider_unavailable_handling():
    # Intentionally point to an unused port to simulate unavailable service
    provider = OllamaLLMProvider(base_url="http://localhost:59999", timeout_seconds=1.0)
    health = await provider.health_check()
    assert health.is_available is False
    assert "unreachable" in health.details.lower() or "connection" in health.details.lower()

    # Generation should report error truthfully and never silently fabricate success
    res = await provider.generate("Test prompt")
    assert res.error is not None
    assert "failed" in res.error.lower() or "error" in res.error.lower()


@pytest.mark.asyncio
async def test_hosted_llm_provider_disabled():
    provider = HostedLLMProvider()
    health = await provider.health_check()
    assert health.is_available is False
    assert "disabled" in health.details.lower()

    res = await provider.generate("Test prompt")
    assert res.error is not None
    assert "disabled" in res.error.lower()
