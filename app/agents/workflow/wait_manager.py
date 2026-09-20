"""
Workflow Wait Condition Manager.
Coordinates asynchronous barrier conditions and multi-signal synchronizations.
"""

from typing import Dict, List, Optional, Set
from uuid import UUID
from pydantic import BaseModel, Field


class WaitCondition(BaseModel):
    """Represents a discrete synchronization barrier condition."""
    condition_id: str
    description: str = ""
    is_satisfied: bool = False


class WaitManager:

    """Tracks workflows blocked waiting for one or more conditions."""

    def __init__(self):
        self._waiting_instances: Dict[UUID, Set[str]] = {}

    def register_wait(self, instance_id: UUID, conditions: List[str]) -> None:
        self._waiting_instances[instance_id] = set(conditions)

    def satisfy_condition(self, instance_id: UUID, condition: str) -> bool:
        """Removes condition. Returns True if all conditions are satisfied."""
        if instance_id not in self._waiting_instances:
            return False
        conds = self._waiting_instances[instance_id]
        conds.discard(condition)
        if not conds:
            del self._waiting_instances[instance_id]
            return True
        return False
