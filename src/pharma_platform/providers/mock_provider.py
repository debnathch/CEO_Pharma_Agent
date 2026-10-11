"""Mock LLM Provider for fully offline and deterministic execution."""

import time
from typing import Any, Optional

from pharma_platform.providers.base_provider import LLMProvider, LLMResponse, ProviderStatus


class MockLLMProvider(LLMProvider):
    """Deterministic LLM provider that runs without any network or local daemon."""

    def __init__(self, model_name: str = "mock-deterministic-v1") -> None:
        self._model_name = model_name

    @property
    def provider_name(self) -> str:
        return "mock"

    async def generate(
        self, prompt: str, system_prompt: Optional[str] = None, **kwargs: Any
    ) -> LLMResponse:
        start_time = time.perf_counter()

        # Provide a structured executive summary based on prompt cues
        p_lower = prompt.lower()
        if "sales" in p_lower:
            text = (
                "Executive Sales Synthesis (Mock Provider):\n"
                "Kolkata Central HQ achieved 107.4% MTD target (₹13.43L achieved vs ₹12.50L target), "
                "leading ethical sales. North Bengal HQ achieved 91.0%, impacted by logistics delays. "
                "PCD franchise network generated ₹46.60L total revenue across 4 distributors."
            )
        elif "profit" in p_lower or "billing" in p_lower or "margin" in p_lower:
            text = (
                "Billing & Margin Intelligence (Mock Provider):\n"
                "Total invoiced net sales stand at ₹440,900 with an overall gross margin of 28.81%. "
                "Notice: Invoice INV-2026-4409 shows a compromised margin of only 9.09% due to heavy "
                "promotional free-goods scheme allocation (₹9,900 bonus units)."
            )
        elif "debtor" in p_lower or "creditor" in p_lower or "finance" in p_lower:
            text = (
                "Financial Risk Advisory (Mock Provider):\n"
                "Total outstanding debtors are ₹622,000. Critical attention required for City Life Hospital "
                "(₹245,000 overdue >90 days, exceeding credit limit). Total trade payables to manufacturers "
                "are ₹1,050,000, scheduled across Net 30 terms."
            )
        elif "procurement" in p_lower or "inventory" in p_lower or "stock" in p_lower:
            text = (
                "Procurement & Inventory Advisory (Mock Provider):\n"
                "Critical stock deficit identified in Amoxicillin & Potassium Clavulanate 625mg (BR-AMX-625) "
                "with only 450 units remaining versus the 1,500 unit threshold. Suggested reorder of 1,850 units "
                "from Zenith Pharma Labs (21-day lead time)."
            )
        elif "briefing" in p_lower or "daily" in p_lower or "overview" in p_lower:
            text = (
                "CEO Daily Executive Briefing (Mock Provider):\n"
                "1. Sales: Kolkata Central leading at 107.4% target achievement.\n"
                "2. Operations: Delayed shipment SHP-2026-8821 held at Siliguri bypass.\n"
                "3. Finance: Overdue debtor City Life Hospital requires credit hold.\n"
                "4. HR: Birthday congratulations to MD Dr. Roy and 5-yr anniversary for TM Debanjan Mukherjee."
            )
        else:
            text = (
                "Executive Assessment (Mock Provider):\n"
                "Processed query against synthetic pharmaceutical business records. "
                "All operations are validated against deterministic business calculations."
            )

        duration_ms = (time.perf_counter() - start_time) * 1000.0

        return LLMResponse(
            text=text,
            provider_name=self.provider_name,
            model_name=self._model_name,
            duration_ms=round(duration_ms, 2),
            is_mock=True,
            tokens_prompt=len(prompt.split()),
            tokens_completion=len(text.split()),
        )

    async def health_check(self) -> ProviderStatus:
        return ProviderStatus(
            provider_name=self.provider_name,
            is_available=True,
            model_name=self._model_name,
            details="Mock provider operational. Zero API fees, deterministic offline execution.",
            is_mock=True,
        )
