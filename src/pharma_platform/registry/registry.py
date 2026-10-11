"""Centralized Agent Registry."""

import logging
from typing import Optional

from pharma_platform.contracts.agent import AgentManifest
from pharma_platform.registry.base_agent import BaseAgent

logger = logging.getLogger(__name__)


class AgentRegistry:
    """Registry maintaining all active agents and their declared manifests."""

    def __init__(self) -> None:
        self._agents: dict[str, BaseAgent] = {}

    def register(self, agent: BaseAgent) -> None:
        """Register an agent instance. Rejects duplicate agent IDs."""
        agent_id = agent.manifest.agent_id
        if not agent_id:
            raise ValueError("Agent manifest must provide a non-empty agent_id")

        if agent_id in self._agents:
            raise ValueError(
                f"Agent with ID '{agent_id}' is already registered. Duplicate registration rejected."
            )

        self._agents[agent_id] = agent
        logger.info(
            "Registered agent '%s' (v%s) with %d capabilities",
            agent_id,
            agent.manifest.version,
            len(agent.manifest.capabilities),
        )

    def get(self, agent_id: str) -> BaseAgent:
        """Retrieve an agent by its ID, or raise KeyError."""
        if agent_id not in self._agents:
            raise KeyError(
                f"Agent with ID '{agent_id}' is not registered. Registered: {list(self._agents.keys())}"
            )
        return self._agents[agent_id]

    def get_optional(self, agent_id: str) -> Optional[BaseAgent]:
        """Retrieve an agent by its ID or None if not registered."""
        return self._agents.get(agent_id)

    def list_agents(self) -> list[AgentManifest]:
        """Return manifests for all registered agents."""
        return [agent.manifest for agent in self._agents.values()]

    def find_by_capability(self, capability: str) -> list[BaseAgent]:
        """Return agents declaring the specified capability."""
        matches = []
        for agent in self._agents.values():
            for cap in agent.manifest.capabilities:
                if cap.name == capability:
                    matches.append(agent)
                    break
        return matches

    def find_by_domain(self, domain: str) -> list[BaseAgent]:
        """Return agents matching a department domain."""
        return [agent for agent in self._agents.values() if agent.manifest.domain.lower() == domain.lower()]

    def clear(self) -> None:
        """Clear all registered agents (useful for test isolation)."""
        self._agents.clear()


# Global default registry instance
_default_registry = AgentRegistry()


def get_agent_registry() -> AgentRegistry:
    """Return the global AgentRegistry instance."""
    return _default_registry
