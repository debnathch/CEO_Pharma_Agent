"""Centralized platform configuration."""

import os
from functools import lru_cache

from pydantic import BaseModel, Field


class Settings(BaseModel):
    app_name: str = "Enterprise Pharmaceutical Agentic AI Ecosystem"
    version: str = "0.1.0"
    environment: str = Field(default_factory=lambda: os.getenv("ENVIRONMENT", "development"))
    data_mode: str = "synthetic"  # All data is synthetic; strictly labeled
    api_prefix: str = "/api/v1"

    # Database
    database_url: str = Field(
        default_factory=lambda: os.getenv("DATABASE_URL", "sqlite:///./data/pharma.db")
    )

    # LLM Settings
    llm_provider: str = Field(default_factory=lambda: os.getenv("LLM_PROVIDER", "mock").lower())
    ollama_base_url: str = Field(
        default_factory=lambda: os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    )
    ollama_model: str = Field(default_factory=lambda: os.getenv("OLLAMA_MODEL", "qwen3:4b"))
    ollama_timeout_seconds: float = Field(
        default_factory=lambda: float(os.getenv("OLLAMA_TIMEOUT_SECONDS", "30.0"))
    )

    # External systems mock URLs (Do NOT connect to live systems)
    marg_erp_url: str = "mock://marg.erp.internal"
    ordering_portal_url: str = "mock://bengalremedies.com:9000"

    # Security & Governance
    enable_simulated_approvals: bool = True
    cors_origins: list[str] = ["*"]
    log_level: str = Field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))


@lru_cache()
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()
