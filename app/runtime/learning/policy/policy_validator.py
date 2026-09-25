"""
Policy Validator for Phase 13.5 (ARLP-KIP).
Validates that proposed policy parameters adhere to hard system safety boundaries.
"""

from typing import Dict, Any, List
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class PolicyValidationResult(BaseModel):
    is_valid: bool = True
    errors: List[str] = Field(default_factory=list)
    validation_timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class PolicyValidator:
    """
    Validates parameter safety bounds for candidate policies.
    """

    @classmethod
    def validate(cls, parameters: Dict[str, Any]) -> PolicyValidationResult:
        errors = []
        retries = parameters.get("max_retries", 3)
        if not (0 <= retries <= 10):
            errors.append(f"max_retries {retries} out of valid range [0, 10]")

        conf = parameters.get("confidence_threshold", 0.85)
        if not (0.50 <= conf <= 1.00):
            errors.append(f"confidence_threshold {conf} out of valid range [0.50, 1.00]")

        return PolicyValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
        )
