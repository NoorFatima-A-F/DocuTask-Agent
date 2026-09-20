"""Audit Context Propagation & Correlation Graph Tracking."""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
import uuid


class AuditContext(BaseModel):
    """Execution context carrying correlation identifiers across workflows, agents, tools, and models."""
    request_id: str = Field(default_factory=lambda: f"req_{uuid.uuid4().hex[:10]}")
    correlation_id: str = Field(default_factory=lambda: f"corr_{uuid.uuid4().hex[:10]}")
    parent_event_id: Optional[str] = None
    
    tenant_id: str
    organization_id: Optional[str] = None
    workspace_id: Optional[str] = None
    environment: str = "production"
    
    actor_id: str = "system"
    actor_type: str = "SYSTEM"
    
    workflow_id: Optional[str] = None
    agent_id: Optional[str] = None
    session_id: Optional[str] = None
    
    tags: Dict[str, str] = Field(default_factory=dict)

    def child_context(self, event_id: str) -> "AuditContext":
        """Creates a child context with the current event ID set as the parent_event_id."""
        return AuditContext(
            request_id=self.request_id,
            correlation_id=self.correlation_id,
            parent_event_id=event_id,
            tenant_id=self.tenant_id,
            organization_id=self.organization_id,
            workspace_id=self.workspace_id,
            environment=self.environment,
            actor_id=self.actor_id,
            actor_type=self.actor_type,
            workflow_id=self.workflow_id,
            agent_id=self.agent_id,
            session_id=self.session_id,
            tags=dict(self.tags),
        )
