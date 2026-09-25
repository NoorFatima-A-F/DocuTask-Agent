"""
Abstract base class and contracts for Persistent Runtime Context Stores.
Provides persistent state snapshotting, versioned checkpointing, and cross-worker recovery.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from app.agents.runtime.runtime_context import RuntimeContext


class CheckpointRecord(BaseModel):
    """Metadata and state representation for a single context checkpoint."""
    runtime_id: str
    version: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    state_snapshot: Dict[str, Any] = Field(default_factory=dict)
    context_metadata: Dict[str, Any] = Field(default_factory=dict)


class ContextStore(ABC):
    """Abstract interface defining operations for persistent runtime context."""

    @abstractmethod
    async def save_context(self, context: RuntimeContext, ttl_seconds: Optional[int] = None) -> None:
        """Persists the runtime context."""
        pass

    @abstractmethod
    async def load_context(self, runtime_id: str) -> Optional[RuntimeContext]:
        """Loads a persisted runtime context by its runtime_id."""
        pass

    @abstractmethod
    async def checkpoint_context(
        self,
        runtime_id: str,
        state_snapshot: Dict[str, Any],
        expected_version: Optional[int] = None,
    ) -> int:
        """
        Creates an immutable versioned checkpoint of worker state under runtime_id.
        Returns the new checkpoint version number.
        """
        pass

    @abstractmethod
    async def restore_context(
        self,
        runtime_id: str,
        version: Optional[int] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Restores state snapshot from a checkpoint.
        If version is None, restores the latest checkpoint.
        """
        pass

    @abstractmethod
    async def list_checkpoints(self, runtime_id: str) -> List[int]:
        """Returns sorted list of checkpoint version numbers for runtime_id."""
        pass

    @abstractmethod
    async def delete_context(self, runtime_id: str) -> bool:
        """Deletes runtime context and all its checkpoints."""
        pass
