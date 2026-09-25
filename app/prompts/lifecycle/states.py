"""Prompt Lifecycle States and Audit Records (Phase 8D)."""

from __future__ import annotations

from datetime import datetime, timezone
from pydantic import BaseModel, Field
from app.prompts.registry.models import PromptLifecycleState


class PromptLifecycleAuditEvent(BaseModel):
    """Audit log record for prompt state transitions."""
    prompt_id: str
    organization_id: str
    from_state: PromptLifecycleState
    to_state: PromptLifecycleState
    actor: str
    reason: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
