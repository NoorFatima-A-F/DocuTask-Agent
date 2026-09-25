"""
Shared Memory Bridge.
Enables agents to exchange immutable pointers to Memory Foundation entries without duplicating state.
"""

from typing import Dict, List, Optional
from uuid import UUID
from pydantic import BaseModel, Field


class MemoryReference(BaseModel):
    """Pointer to a shared memory record in the Memory subsystem."""
    reference_id: str
    tier: str  # EPISODIC, SEMANTIC, PROCEDURAL, REFLECTION
    owner_agent_id: UUID
    summary: str
    tags: List[str] = Field(default_factory=list)

    model_config = {"frozen": True}


class SharedMemoryBridge:
    """Registry maintaining accessible memory pointers between collaborating agents."""

    def __init__(self):
        self._references: Dict[str, MemoryReference] = {}

    def share_reference(self, ref: MemoryReference) -> None:
        """Shares a memory pointer with peer agents."""
        self._references[ref.reference_id] = ref

    def get_reference(self, ref_id: str) -> Optional[MemoryReference]:
        """Retrieves a shared memory pointer."""
        return self._references.get(ref_id)

    def list_references(self) -> List[MemoryReference]:
        """Lists all active shared memory references."""
        return list(self._references.values())
