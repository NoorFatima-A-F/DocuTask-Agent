"""Model Usage Analytics Engine (Phase 8C).

Tracks request volumes, prompt & completion tokens, user and tenant attribution,
and model-level workload distribution.
"""

from __future__ import annotations

import time
from typing import List, Optional
from pydantic import BaseModel, Field


class UsageEvent(BaseModel):
    """Single model invocation usage record."""
    event_id: str
    organization_id: str
    model_id: str
    user_id: Optional[str] = None
    workflow_id: Optional[str] = None
    agent_id: Optional[str] = None
    prompt_tokens: int = 0
    completion_tokens: int = 0
    timestamp: float = Field(default_factory=time.time)

    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens


class ModelUsageSummary(BaseModel):
    """Aggregated usage metrics for a model."""
    model_id: str
    organization_id: str
    total_requests: int = 0
    total_prompt_tokens: int = 0
    total_completion_tokens: int = 0
    total_tokens: int = 0


class ModelUsageTracker:
    """In-memory & persistent usage tracking service for model governance."""

    def __init__(self):
        self._events: List[UsageEvent] = []

    def record_usage(self, event: UsageEvent) -> None:
        """Record an execution usage event."""
        self._events.append(event)

    def get_summary(
        self,
        organization_id: str,
        model_id: Optional[str] = None,
    ) -> ModelUsageSummary:
        """Compute aggregated usage for an organization and optional model filter."""
        filtered = [
            e for e in self._events
            if e.organization_id == organization_id and (model_id is None or e.model_id == model_id)
        ]

        total_reqs = len(filtered)
        p_tokens = sum(e.prompt_tokens for e in filtered)
        c_tokens = sum(e.completion_tokens for e in filtered)

        return ModelUsageSummary(
            model_id=model_id or "ALL",
            organization_id=organization_id,
            total_requests=total_reqs,
            total_prompt_tokens=p_tokens,
            total_completion_tokens=c_tokens,
            total_tokens=p_tokens + c_tokens,
        )
