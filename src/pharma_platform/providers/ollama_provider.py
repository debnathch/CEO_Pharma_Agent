"""Ollama Local LLM Provider for self-hosted model inference."""

import logging
import time
from typing import Any, Optional

import httpx

from pharma_platform.providers.base_provider import LLMProvider, LLMResponse, ProviderStatus

logger = logging.getLogger(__name__)


class OllamaLLMProvider(LLMProvider):
    """Integrates with a local Ollama daemon (e.g. qwen3:4b, llama3.2:3b)."""

    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model_name: str = "qwen3:4b",
        timeout_seconds: float = 30.0,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._model_name = model_name
        self._timeout_seconds = timeout_seconds

    @property
    def provider_name(self) -> str:
        return "ollama"

    async def generate(
        self, prompt: str, system_prompt: Optional[str] = None, **kwargs: Any
    ) -> LLMResponse:
        start_time = time.perf_counter()
        url = f"{self._base_url}/api/generate"
        payload = {
            "model": self._model_name,
            "prompt": prompt,
            "system": system_prompt or "You are an executive AI assistant for a pharmaceutical enterprise.",
            "stream": False,
        }

        try:
            async with httpx.AsyncClient(timeout=self._timeout_seconds) as client:
                res = await client.post(url, json=payload)
                res.raise_for_status()
                data = res.json()

            duration_ms = (time.perf_counter() - start_time) * 1000.0
            return LLMResponse(
                text=data.get("response", ""),
                provider_name=self.provider_name,
                model_name=self._model_name,
                duration_ms=round(duration_ms, 2),
                is_mock=False,
                tokens_prompt=data.get("prompt_eval_count"),
                tokens_completion=data.get("eval_count"),
            )
        except httpx.ConnectError as exc:
            duration_ms = (time.perf_counter() - start_time) * 1000.0
            err_msg = (
                f"Ollama server connection failed at {self._base_url}. "
                f"Ensure Ollama daemon is running ('ollama serve'). Error: {exc}"
            )
            logger.error(err_msg)
            return LLMResponse(
                text="",
                provider_name=self.provider_name,
                model_name=self._model_name,
                duration_ms=round(duration_ms, 2),
                is_mock=False,
                error=err_msg,
            )
        except Exception as exc:
            duration_ms = (time.perf_counter() - start_time) * 1000.0
            err_msg = f"Ollama generation error: {exc}"
            logger.error(err_msg)
            return LLMResponse(
                text="",
                provider_name=self.provider_name,
                model_name=self._model_name,
                duration_ms=round(duration_ms, 2),
                is_mock=False,
                error=err_msg,
            )

    async def health_check(self) -> ProviderStatus:
        url = f"{self._base_url}/api/tags"
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                res = await client.get(url)
                if res.status_code == 200:
                    data = res.json()
                    models = [m.get("name") for m in data.get("models", [])]
                    model_found = any(self._model_name in m for m in models)
                    if model_found:
                        return ProviderStatus(
                            provider_name=self.provider_name,
                            is_available=True,
                            model_name=self._model_name,
                            details=f"Ollama server online. Model '{self._model_name}' available.",
                            is_mock=False,
                        )
                    return ProviderStatus(
                        provider_name=self.provider_name,
                        is_available=False,
                        model_name=self._model_name,
                        details=(
                            f"Ollama server online, but model '{self._model_name}' is not downloaded. "
                            f"Installed models: {models}. Run 'ollama pull {self._model_name}'."
                        ),
                        is_mock=False,
                    )
        except Exception as exc:
            return ProviderStatus(
                provider_name=self.provider_name,
                is_available=False,
                model_name=self._model_name,
                details=f"Ollama service unreachable at {self._base_url} ({exc})",
                is_mock=False,
            )

        return ProviderStatus(
            provider_name=self.provider_name,
            is_available=False,
            model_name=self._model_name,
            details="Ollama health check returned unknown status",
            is_mock=False,
        )
