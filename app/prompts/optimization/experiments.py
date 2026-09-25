"""Prompt A/B Testing & Experimentation Models (Phase 8D)."""

from __future__ import annotations

import enum
import time
from typing import List, Optional
from pydantic import BaseModel, Field


class ExperimentStatus(str, enum.Enum):
    """Lifecycle states of a prompt optimization experiment."""
    DRAFT = "DRAFT"
    RUNNING = "RUNNING"
    CONCLUDED = "CONCLUDED"
    CANCELLED = "CANCELLED"


class PromptVariant(BaseModel):
    """Single prompt candidate variant in an A/B experiment."""
    variant_id: str  # e.g. "variant_a", "variant_b"
    version_id: str
    traffic_weight: float = 0.5  # 0.0 to 1.0
    total_invocations: int = 0
    successful_invocations: int = 0
    total_latency_ms: float = 0.0
    positive_feedback_count: int = 0


class PromptExperiment(BaseModel):
    """A/B prompt optimization experiment container."""
    experiment_id: str
    prompt_id: str
    name: str
    organization_id: str
    status: ExperimentStatus = ExperimentStatus.DRAFT
    variants: List[PromptVariant] = Field(default_factory=list)
    winner_variant_id: Optional[str] = None
    created_at: float = Field(default_factory=time.time)
    concluded_at: Optional[float] = None
