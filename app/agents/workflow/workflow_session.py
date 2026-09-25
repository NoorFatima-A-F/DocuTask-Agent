"""
Workflow Session.
Maintains stateful operational context, active tokens, and execution leases for a running workflow.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from app.agents.workflow.workflow_instance import WorkflowInstance


class WorkflowSession(BaseModel):
    """Session container managing active runtime context for a workflow instance."""
    session_id: UUID = Field(default_factory=uuid4)
    instance: WorkflowInstance
    active_node_id: Optional[str] = None
    staged_signals: List[Dict[str, Any]] = Field(default_factory=list)
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def stage_signal(self, signal: Dict[str, Any]) -> "WorkflowSession":
        return self.model_copy(update={"staged_signals": [*self.staged_signals, signal]})
