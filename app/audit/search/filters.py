"""Audit Search Filter Models."""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class AuditSearchFilter(BaseModel):
    """Multi-facet query filters for searching audit logs."""
    tenant_id: str
    organization_id: Optional[str] = None
    workspace_id: Optional[str] = None
    actor_id: Optional[str] = None
    actor_type: Optional[str] = None
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None
    event_type: Optional[str] = None
    category: Optional[str] = None
    severity: Optional[str] = None
    outcome: Optional[str] = None
    min_risk_score: Optional[float] = None
    correlation_id: Optional[str] = None
    request_id: Optional[str] = None
    workflow_id: Optional[str] = None
    agent_id: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    query: Optional[str] = None  # Full-text token query
    limit: int = 100
    offset: int = 0
