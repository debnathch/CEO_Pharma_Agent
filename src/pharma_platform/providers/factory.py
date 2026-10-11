"""Provider factory returning configured LLMProvider."""

from pharma_platform.configuration.settings import get_settings
from pharma_platform.providers.base_provider import LLMProvider
from pharma_platform.providers.hosted_provider import HostedLLMProvider
from pharma_platform.providers.mock_provider import MockLLMProvider
from pharma_platform.providers.ollama_provider import OllamaLLMProvider


def get_llm_provider() -> LLMProvider:
    """Return configured provider instance according to settings."""
    settings = get_settings()
    provider_type = settings.llm_provider.lower().strip()

    if provider_type == "ollama":
        return OllamaLLMProvider(
            base_url=settings.ollama_base_url,
            model_name=settings.ollama_model,
            timeout_seconds=settings.ollama_timeout_seconds,
        )
    elif provider_type == "hosted":
        return HostedLLMProvider()
    else:
        # Default: Mock provider for offline deterministic development
        return MockLLMProvider()
