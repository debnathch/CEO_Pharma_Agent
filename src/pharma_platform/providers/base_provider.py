"""LLM Provider Abstraction Interface."""

from abc import ABC, abstractmethod
from typing import Any, Optional

from pydantic import BaseModel


class LLMResponse(BaseModel):
    text: str
    provider_name: str
    model_name: str
    duration_ms: float
    is_mock: bool = False
    tokens_prompt: Optional[int] = None
    tokens_completion: Optional[int] = None
    error: Optional[str] = None


class ProviderStatus(BaseModel):
    provider_name: str
    is_available: bool
    model_name: str
    details: str
    is_mock: bool


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return provider identifier (e.g. 'mock', 'ollama')."""
        pass

    @abstractmethod
    async def generate(
        self, prompt: str, system_prompt: Optional[str] = None, **kwargs: Any
    ) -> LLMResponse:
        """Generate text from the LLM."""
        pass

    @abstractmethod
    async def health_check(self) -> ProviderStatus:
        """Check provider reachability and model availability."""
        pass
