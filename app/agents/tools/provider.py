"""
Tool Provider Abstraction.
Defines ToolProvider, ProviderMetadata, ProviderHealth, ProviderStatus, ProviderCapabilities, and ProviderLimits.
Decouples planners from concrete providers (Vertex AI, Gemini, Document AI, Vision API, Tesseract, Azure, AWS).
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ProviderStatus(str, Enum):
    """Provider health lifecycle status."""
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNAVAILABLE = "UNAVAILABLE"
    MAINTENANCE = "MAINTENANCE"


class ProviderHealth(BaseModel):
    """Health metrics reported by a provider."""
    status: ProviderStatus = Field(default=ProviderStatus.HEALTHY)
    consecutive_failures: int = Field(default=0, ge=0)
    avg_response_latency_ms: float = Field(default=100.0, ge=0.0)
    error_message: Optional[str] = Field(default=None)
    model_config = {"frozen": True}


class ProviderMetadata(BaseModel):
    """Metadata specification for a tool provider."""
    provider_name: str
    display_name: str
    vendor: str = Field(default="Google Cloud")
    version: str = Field(default="v1.0")
    supported_regions: List[str] = Field(default_factory=lambda: ["us-central1", "global"])
    is_cloud_native: bool = Field(default=True)
    model_config = {"frozen": True}


class ToolProvider(ABC):
    """Abstract Base Class for Tool Providers."""

    def __init__(self, metadata: ProviderMetadata):
        self.metadata = metadata

    @property
    def provider_name(self) -> str:
        return self.metadata.provider_name

    @abstractmethod
    async def get_health(self) -> ProviderHealth:
        """Retrieves provider operational health metrics."""
        pass
