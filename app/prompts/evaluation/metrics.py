"""Prompt Evaluation Metrics & Multi-Dimensional Quality Scoring (Phase 8D)."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class PromptEvaluationMetrics(BaseModel):
    """Multi-dimensional evaluation quality score."""
    evaluation_id: str = Field(default_factory=lambda: f"eval_{uuid.uuid4().hex[:8]}")
    prompt_id: str
    version_id: str
    dataset_id: str
    total_cases: int = 0
    passed_cases: int = 0
    accuracy_score: float = 0.0  # 0.0 to 1.0
    faithfulness_score: float = 0.0  # 0.0 to 1.0
    format_compliance_score: float = 0.0  # 0.0 to 1.0
    safety_score: float = 1.0  # 0.0 to 1.0
    hallucination_rate: float = 0.0  # 0.0 to 1.0 (lower is better)
    composite_score: float = 0.0  # 0.0 to 1.0
    average_latency_ms: float = 0.0
    total_token_usage: int = 0
    estimated_cost_usd: float = 0.0
    evaluated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def compute_composite_score(self) -> float:
        """Compute weighted overall quality score."""
        acc = self.accuracy_score
        faith = self.faithfulness_score
        fmt = self.format_compliance_score
        safe = self.safety_score
        halluc_penalty = (1.0 - self.hallucination_rate)

        composite = (
            acc * 0.35
            + faith * 0.25
            + fmt * 0.15
            + safe * 0.15
            + halluc_penalty * 0.10
        )
        self.composite_score = round(composite, 4)
        return self.composite_score
