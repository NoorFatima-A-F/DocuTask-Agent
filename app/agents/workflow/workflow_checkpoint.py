"""
Workflow Checkpoint.
Durable, point-in-time state capture enabling safe restart, recovery, and replay.
"""

from datetime import datetime, timezone
from typing import Any, Dict
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from app.agents.workflow.lifecycle import WorkflowLifecycleState
from app.agents.workflow.workflow_state import WorkflowState


class WorkflowCheckpoint(BaseModel):
    """Durable checkpoint capturing completed nodes, variables, and lifecycle state."""
    checkpoint_id: UUID = Field(default_factory=uuid4)
    instance_id: UUID
    state: WorkflowLifecycleState
    workflow_state: WorkflowState
    checkpoint_timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = {"frozen": True}
