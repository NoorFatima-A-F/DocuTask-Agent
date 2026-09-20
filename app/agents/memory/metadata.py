"""
Memory Metadata & Statistics Models.
Provides immutable Pydantic v2 metadata models for memory items.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class MemoryIdentity(BaseModel):
    """Immutable Memory Identity."""
    memory_id: UUID = Field(default_factory=uuid4)
    session_id: Optional[str] = Field(default=None)
    execution_id: Optional[str] = Field(default=None)
    workflow_id: Optional[str] = Field(default=None)
    goal_id: Optional[str] = Field(default=None)
    task_id: Optional[str] = Field(default=None)
    correlation_id: str = Field(default_factory=lambda: str(uuid4()))
    tenant_id: str = Field(default="default")
    owner: str = Field(default="system")
    model_config = {"frozen": True}


class MemoryStatistics(BaseModel):
    """Operational statistics for a memory record."""
    access_count: int = Field(default=0, ge=0)
    last_accessed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    retrieval_count: int = Field(default=0, ge=0)
    importance_score: float = Field(default=0.5, ge=0.0, le=1.0)
    confidence_score: float = Field(default=0.95, ge=0.0, le=1.0)
    model_config = {"frozen": True}


class MemoryMetadata(BaseModel):
    """Metadata parameters for a memory record."""
    source_component: str = Field(default="DocumentAgent")
    memory_type: str = Field(default="WORKING")
    security_classification: str = Field(default="INTERNAL")
    version: str = Field(default="v1.0")
    tags: List[str] = Field(default_factory=list)
    labels: Dict[str, str] = Field(default_factory=dict)
    checksum: str = Field(default="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
    extra: Dict[str, Any] = Field(default_factory=dict)
    model_config = {"frozen": True}
