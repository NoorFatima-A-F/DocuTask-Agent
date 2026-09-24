"""
Distributed State Store.
Provides thread-safe state management with optimistic concurrency control across distributed agents.
"""

from typing import Any, Dict, Optional
from uuid import UUID
from pydantic import BaseModel
from app.agents.coordination.exceptions import InconsistentSharedStateError


class StateEntry(BaseModel):
    """Versioned state item with optimistic lock check."""
    key: str
    value: Any
    version: int = 1
    updated_by: Optional[UUID] = None

    model_config = {"frozen": True}


class DistributedStateStore:
    """In-memory distributed state store enforcing optimistic concurrency control."""

    def __init__(self):
        self._store: Dict[str, StateEntry] = {}

    def get(self, key: str) -> Optional[StateEntry]:
        """Retrieves state entry."""
        return self._store.get(key)

    def set_with_optimistic_lock(
        self,
        key: str,
        value: Any,
        expected_version: int,
        agent_id: UUID
    ) -> StateEntry:
        """Sets value ensuring expected version matches current version."""
        current = self._store.get(key)
        curr_ver = current.version if current else 0

        if curr_ver != expected_version:
            raise InconsistentSharedStateError(
                f"Optimistic lock conflict on key '{key}'. Expected version {expected_version}, found {curr_ver}."
            )

        new_entry = StateEntry(
            key=key,
            value=value,
            version=curr_ver + 1,
            updated_by=agent_id
        )
        self._store[key] = new_entry
        return new_entry
