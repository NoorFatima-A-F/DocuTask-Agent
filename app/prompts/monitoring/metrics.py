"""Prompt Runtime Execution Telemetry Models (Phase 8D)."""

from __future__ import annotations

import time
from typing import Optional
from pydantic import BaseModel, Field


class PromptExecutionEvent(BaseModel):
    """Telemetry record for a single prompt runtime invocation."""
    event_id: str
    prompt_id: str
    version_id: str
    organization_id: str
    model_id: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    latency_ms: float = 0.0
    cost_usd: float = 0.0
    is_success: bool = True
    error_type: Optional[str] = None
    user_feedback_score: Optional[float] = None  # 1 to 5 or -1 to 1
    timestamp: float = Field(default_factory=time.time)

    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens
