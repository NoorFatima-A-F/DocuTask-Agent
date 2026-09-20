"""
MemoryItem Domain Aggregate & MemoryRepository Pattern.
Defines strongly typed MemoryItem aggregate model and abstract repository contract.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.agents.memory.embeddings import VectorEmbedding
from app.agents.memory.lifecycle import MemoryLifecycleState
from app.agents.memory.metadata import MemoryIdentity, MemoryMetadata, MemoryStatistics


class MemoryItem(BaseModel):
    """
    Strongly Typed Memory Item Aggregate.
    Represents an atomic memory record stored across memory tiers.
    """

    identity: MemoryIdentity = Field(default_factory=MemoryIdentity)
    key: str
    value: Any
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: Optional[datetime] = Field(default=None)
    
    lifecycle_state: MemoryLifecycleState = Field(default=MemoryLifecycleState.ACTIVE)
    metadata: MemoryMetadata = Field(default_factory=MemoryMetadata)
    statistics: MemoryStatistics = Field(default_factory=MemoryStatistics)
    embedding: Optional[VectorEmbedding] = Field(default=None)

    model_config = {"frozen": True}

    def is_expired(self) -> bool:
        """Returns True if record has passed its expiration deadline."""
        if not self.expires_at:
            return False
        return datetime.now(timezone.utc) > self.expires_at
