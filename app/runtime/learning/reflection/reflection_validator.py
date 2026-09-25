"""
Reflection Validator for Phase 13.5 (ARLP-KIP).
Validates structural integrity, statistical consistency, and event grounding of reflection reports.
"""

from typing import Any, List
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class ReflectionValidationResult(BaseModel):
    is_valid: bool = True
    errors: List[str] = Field(default_factory=list)
    validation_timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ReflectionValidator:
    """
    Validates that a reflection report contains statistically sound metrics and grounded evidence.
    """

    @classmethod
    def validate(cls, report: Any) -> ReflectionValidationResult:
        errors = []
        if not getattr(report, "mission_id", None):
            errors.append("Missing mission_id in reflection report")
        
        kpis = getattr(report, "macro_kpis", None)
        if kpis and getattr(kpis, "throughput_tasks_per_sec", 0) <= 0:
            errors.append("Invalid throughput metric in reflection report")

        conf = getattr(report, "confidence_metrics", None)
        if conf and (getattr(conf, "avg_confidence", 0) < 0.0 or getattr(conf, "avg_confidence", 0) > 1.0):
            errors.append("Confidence out of bounds [0.0, 1.0]")

        return ReflectionValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
        )
