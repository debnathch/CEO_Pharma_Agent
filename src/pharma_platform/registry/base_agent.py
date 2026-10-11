"""Abstract Base Agent specification."""

from abc import ABC, abstractmethod

from pharma_platform.contracts.agent import (
    AgentManifest,
    AgentRequest,
    AgentResult,
    AgentStatus,
)


class BaseAgent(ABC):
    """Abstract base class for all pharmaceutical agents."""

    @property
    @abstractmethod
    def manifest(self) -> AgentManifest:
        """Return the manifest describing this agent's capabilities and metadata."""
        pass

    def validate_request(self, request: AgentRequest) -> None:
        """Validate request against declared capabilities and requirements."""
        declared_caps = {cap.name for cap in self.manifest.capabilities}
        if request.capability not in declared_caps:
            raise ValueError(
                f"Capability '{request.capability}' not declared by agent '{self.manifest.agent_id}'. "
                f"Available: {sorted(declared_caps)}"
            )

    @abstractmethod
    async def execute(self, request: AgentRequest) -> AgentResult:
        """Execute the agent capability asynchronously."""
        pass

    def create_not_implemented_result(
        self, request: AgentRequest, capability_name: str, duration_ms: float = 0.0
    ) -> AgentResult:
        """Create a truthful not_implemented result for unimplemented capabilities."""
        return AgentResult(
            execution_id=request.execution_id,
            agent_id=self.manifest.agent_id,
            version=self.manifest.version,
            status=AgentStatus.NOT_IMPLEMENTED,
            structured_data={"capability": capability_name, "is_implemented": False},
            summary=(
                f"Agent '{self.manifest.display_name}' ({self.manifest.agent_id}) does not currently implement "
                f"capability '{capability_name}'. This specialist capability is planned for a subsequent phase."
            ),
            evidence=[],
            warnings=[f"Capability '{capability_name}' is declared as a skeleton and is not yet implemented."],
            duration_ms=duration_ms,
            data_mode="synthetic",
        )
