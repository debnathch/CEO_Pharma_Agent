"""Abstract Integration Adapter and Health Status."""

from abc import ABC, abstractmethod
from datetime import datetime, timezone

from pydantic import BaseModel, Field


class IntegrationHealth(BaseModel):
    system_id: str
    display_name: str
    is_connected: bool
    is_mock: bool = True
    authority_scope: str
    last_sync_timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status_message: str = "Operating normally (Mock synthetic mode)"


class BaseIntegrationAdapter(ABC):
    """Abstract interface for external systems integration."""

    @abstractmethod
    def get_system_id(self) -> str:
        """Return unique system identifier."""
        pass

    @abstractmethod
    def get_health(self) -> IntegrationHealth:
        """Return health status and mock indicator."""
        pass
