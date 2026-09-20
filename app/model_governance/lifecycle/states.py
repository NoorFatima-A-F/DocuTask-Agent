"""Model Lifecycle States and Audit Events (Phase 8C)."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from app.model_governance.registry.models import ModelLifecycleState


class ModelLifecycleAuditEvent(BaseModel):
    """Audit log entry for model lifecycle transitions."""
    model_id: str
    organization_id: str
    from_state: ModelLifecycleState
    to_state: ModelLifecycleState
    actor_id: str
    reason: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
