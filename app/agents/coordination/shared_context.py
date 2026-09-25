"""
Shared Context Synchronization.
Synchronizes execution state, conversational state, and output references across collaborating agents
without violating subsystem ownership boundaries.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class SharedContextRecord(BaseModel):
    """Immutable data record in shared multi-agent context."""
    key: str
    value: Any
    producer_agent_id: UUID
    version: int = 1
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = {"frozen": True}


class SharedContext:
    """Thread-safe context repository accessible across multiple collaborating agents."""

    def __init__(self, context_id: Optional[UUID] = None):
        self.context_id = context_id or uuid4()
        self._entries: Dict[str, SharedContextRecord] = {}

    def get(self, key: str) -> Optional[Any]:
        """Retrieves value for key."""
        entry = self._entries.get(key)
        return entry.value if entry else None

    def put(self, key: str, value: Any, producer_id: UUID) -> None:
        """Publishes or updates a key in shared context with incremented version."""
        current_version = self._entries[key].version if key in self._entries else 0
        self._entries[key] = SharedContextRecord(
            key=key,
            value=value,
            producer_agent_id=producer_id,
            version=current_version + 1
        )

    def list_keys(self) -> List[str]:
        """Returns all keys in shared context."""
        return list(self._entries.keys())

    def snapshot(self) -> Dict[str, Any]:
        """Returns dictionary snapshot of all current values."""
        return {k: rec.value for k, rec in self._entries.items()}
