"""
Collaboration Context.
Shared, thread-safe context holding intermediate artifacts, variables, and conversation references.
"""

from typing import Any, Dict, List
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class CollaborationContext(BaseModel):
    """Execution context shared across collaborating agents in a session."""
    context_id: UUID = Field(default_factory=uuid4)
    session_id: UUID
    shared_data: Dict[str, Any] = Field(default_factory=dict)
    active_artifacts: List[str] = Field(default_factory=list)
    version: int = Field(default=1, ge=1)

    def update_data(self, key: str, value: Any) -> "CollaborationContext":
        """Returns a new immutable context version with updated key-value."""
        new_data = dict(self.shared_data)
        new_data[key] = value
        return self.model_copy(update={
            "shared_data": new_data,
            "version": self.version + 1
        })
