"""
Tool Descriptor Domain Models.
Provides ToolIdentity, ToolVersion, ToolStatistics, ToolMetadata, and ToolDescriptor.
Descriptors contain only metadata and metadata attributes; never execution logic.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.agents.tools.metadata import CostProfile, LatencyProfile, ToolResourceRequirements, ToolSecurityProfile


class ToolIdentity(BaseModel):
    """Immutable Tool Identity."""
    tool_id: str
    name: str
    provider_name: str
    category: str
    model_config = {"frozen": True}


class ToolVersion(BaseModel):
    """Tool Versioning Specification."""
    version: str = Field(default="1.0.0")
    is_deprecated: bool = Field(default=False)
    model_config = {"frozen": True}


class ToolStatistics(BaseModel):
    """Tool operational statistics."""
    execution_count: int = Field(default=0, ge=0)
    success_count: int = Field(default=0, ge=0)
    failure_count: int = Field(default=0, ge=0)
    avg_latency_ms: float = Field(default=0.0, ge=0.0)
    avg_cost_usd: float = Field(default=0.0, ge=0.0)
    confidence_score: float = Field(default=0.95, ge=0.0, le=1.0)
    model_config = {"frozen": True}


class ToolMetadata(BaseModel):
    """Comprehensive Tool Metadata Description."""
    description: str
    supported_capabilities: List[str] = Field(default_factory=list)
    supported_document_types: List[str] = Field(default_factory=list)
    supported_mime_types: List[str] = Field(default_factory=list)
    cost_profile: CostProfile = Field(default_factory=CostProfile)
    latency_profile: LatencyProfile = Field(default_factory=LatencyProfile)
    security_profile: ToolSecurityProfile = Field(default_factory=ToolSecurityProfile)
    resource_requirements: ToolResourceRequirements = Field(default_factory=ToolResourceRequirements)
    supports_batch: bool = Field(default=False)
    supports_streaming: bool = Field(default=False)
    limitations: List[str] = Field(default_factory=list)
    extra_metadata: Dict[str, Any] = Field(default_factory=dict)
    model_config = {"frozen": True}


class ToolDescriptor(BaseModel):
    """Complete Immutable Tool Descriptor."""
    identity: ToolIdentity
    version: ToolVersion = Field(default_factory=ToolVersion)
    metadata: ToolMetadata
    statistics: ToolStatistics = Field(default_factory=ToolStatistics)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    model_config = {"frozen": True}
