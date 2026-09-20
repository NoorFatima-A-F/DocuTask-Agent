"""
Reflection Validation Report.
Aggregates validation outcomes across trace inputs, models, and generated artifacts.
"""

from typing import List
from pydantic import BaseModel, Field
from app.agents.reflection.context import ReflectionRequest
from app.agents.reflection.validators import ReflectionValidator


class ReflectionValidationReport(BaseModel):
    """Validation report summarizing integrity checks on a reflection request."""
    is_valid: bool = True
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)

    model_config = {"frozen": True}


class ReflectionRequestValidator:
    """Validates full reflection requests prior to pipeline execution."""

    @staticmethod
    def validate(request: ReflectionRequest) -> ReflectionValidationReport:
        """Runs pre-flight validation on reflection request."""
        errors: List[str] = []
        warnings: List[str] = []

        try:
            ReflectionValidator.validate_execution_trace(request.trace)
        except Exception as e:
            errors.append(str(e))

        if len(request.trace.tasks) == 0:
            warnings.append("Execution trace contains no tasks.")

        if request.context.max_evaluation_timeout_sec <= 0:
            errors.append("max_evaluation_timeout_sec must be greater than zero.")

        return ReflectionValidationReport(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
