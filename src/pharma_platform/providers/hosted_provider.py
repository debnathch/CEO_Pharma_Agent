"""Hosted LLM Provider (Optional extension point - disabled by default)."""

from typing import Any, Optional

from pharma_platform.providers.base_provider import LLMProvider, LLMResponse, ProviderStatus


class HostedLLMProvider(LLMProvider):
    """Extension point for external hosted LLM providers (e.g. cloud APIs).

    Not enabled in foundation phase to guarantee zero API fees.
    """

    @property
    def provider_name(self) -> str:
        return "hosted"

    async def generate(
        self, prompt: str, system_prompt: Optional[str] = None, **kwargs: Any
    ) -> LLMResponse:
        return LLMResponse(
            text="",
            provider_name=self.provider_name,
            model_name="none",
            duration_ms=0.0,
            is_mock=False,
            error="Hosted LLM provider is disabled in this phase. Free local LLM / Mock provider is active.",
        )

    async def health_check(self) -> ProviderStatus:
        return ProviderStatus(
            provider_name=self.provider_name,
            is_available=False,
            model_name="unconfigured",
            details="Hosted LLM provider is not configured (disabled by design).",
            is_mock=False,
        )
