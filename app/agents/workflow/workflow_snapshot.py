"""
Workflow Snapshot.
Serialized, immutable snapshot of full workflow definition, state machine, and instance history.
"""

from datetime import datetime, timezone
from typing import Any, Dict
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from app.agents.workflow.workflow_instance import WorkflowInstance


class WorkflowSnapshot(BaseModel):
    """Complete serialized point-in-time snapshot for cold storage or Cloud Storage backup."""
    snapshot_id: UUID = Field(default_factory=uuid4)
    instance_id: UUID
    instance_data: Dict[str, Any]
    definition_id: UUID
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = {"frozen": True}

    @classmethod
    def create(cls, instance: WorkflowInstance) -> "WorkflowSnapshot":
        return cls(
            instance_id=instance.instance_id,
            instance_data=instance.model_dump(mode="json"),
            definition_id=instance.definition_id
        )
