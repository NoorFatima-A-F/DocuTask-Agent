"""
Learning Validator for Phase 13.5 (ARLP-KIP).
Validates that mined lessons adhere to empirical significance criteria and statistical confidence floors.
"""

from typing import Dict, Any, List
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class LearningValidationResult(BaseModel):
    is_valid: bool = True
    errors: List[str] = Field(default_factory=list)
    validation_timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class LearningValidator:
    """
    Validates institutional lessons and policy recommendations.
    """

    @classmethod
    def validate_lesson(
        cls,
        lesson_id: str,
        rules: List[Any],
        confidence: float,
    ) -> LearningValidationResult:
        errors = []
        if confidence < 0.50:
            errors.append(f"Confidence score {confidence} is below minimum admissible floor (0.50)")
        if not rules:
            errors.append("Lesson must contain at least one extracted actionable rule")

        return LearningValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
        )
