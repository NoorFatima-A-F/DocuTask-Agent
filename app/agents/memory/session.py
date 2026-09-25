"""
Memory Session Domain Model.
Tracks memory execution session scope and session-bound memory identifiers.
"""

from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class MemorySession(BaseModel):
    """Memory Execution Session boundary object."""

    session_id: UUID = Field(default_factory=uuid4)
    user_id: Optional[UUID] = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = Field(default=True)
    memory_keys: List[str] = Field(default_factory=list)

    model_config = {"frozen": True}
