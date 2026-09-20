"""
Production Runtime Session Engine.
Maintains hierarchical session trees, parent-child correlations, and unified lifecycle tracking.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from app.agents.runtime.runtime_context import RuntimeContext


class RuntimeSession(BaseModel):
    """Root execution session unifying workflow, execution, recovery, and reflection sessions."""
    session_id: UUID = Field(default_factory=uuid4)
    parent_session_id: Optional[UUID] = None
    context: RuntimeContext = Field(default_factory=RuntimeContext)
    status: str = Field(default="ACTIVE")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    closed_at: Optional[datetime] = None
    workflow_session_id: Optional[UUID] = None
    execution_session_id: Optional[UUID] = None
    recovery_session_id: Optional[UUID] = None
    reflection_session_id: Optional[UUID] = None
    child_session_ids: List[UUID] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def spawn_child_session(
        self,
        agent_id: Optional[str] = None,
        workflow_id: Optional[str] = None,
        execution_id: Optional[str] = None,
    ) -> "RuntimeSession":
        """Spawns child session inheriting context and linking parent."""
        child_id = uuid4()
        child_ctx = self.context.spawn_child_context(
            new_span=True,
            agent_id=agent_id,
            workflow_id=workflow_id,
            execution_id=execution_id,
        )
        return RuntimeSession(
            session_id=child_id,
            parent_session_id=self.session_id,
            context=child_ctx,
            metadata=dict(self.metadata),
        )

    def bind_workflow_session(self, wf_session_id: UUID) -> "RuntimeSession":
        """Associates active workflow session."""
        updated_ctx = self.context.spawn_child_context(workflow_id=str(wf_session_id), new_span=False)
        return self.model_copy(
            update={
                "workflow_session_id": wf_session_id,
                "context": updated_ctx,
            }
        )

    def bind_execution_session(self, exec_session_id: UUID) -> "RuntimeSession":
        """Associates active execution session."""
        updated_ctx = self.context.spawn_child_context(execution_id=str(exec_session_id), new_span=False)
        return self.model_copy(
            update={
                "execution_session_id": exec_session_id,
                "context": updated_ctx,
            }
        )

    def bind_recovery_session(self, rec_session_id: UUID) -> "RuntimeSession":
        """Associates active recovery session."""
        return self.model_copy(update={"recovery_session_id": rec_session_id})

    def bind_reflection_session(self, refl_session_id: UUID) -> "RuntimeSession":
        """Associates active reflection session."""
        return self.model_copy(update={"reflection_session_id": refl_session_id})

    def close(self, status: str = "CLOSED") -> "RuntimeSession":
        """Closes session and timestamps completion."""
        return self.model_copy(
            update={
                "status": status,
                "closed_at": datetime.now(timezone.utc),
            }
        )

    model_config = {"frozen": True}
