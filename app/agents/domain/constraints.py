"""
Reusable Domain Constraint Models.
Models Time, Budget, Token, Security, Document, Resource, Latency, Compliance, Quality, and Confidence constraints.
"""

from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from app.agents.domain.enums import ConstraintType


class DomainConstraint(BaseModel):
    """Base domain constraint specification."""
    constraint_type: ConstraintType
    name: str
    target_value: Any
    is_hard_constraint: bool = Field(default=True)
    model_config = {"frozen": True}


class TimeConstraint(DomainConstraint):
    """Deadline time constraint."""
    constraint_type: ConstraintType = ConstraintType.TIME
    max_duration_seconds: float = Field(default=300.0, gt=0.0)


class BudgetConstraint(DomainConstraint):
    """Monetary cost constraint."""
    constraint_type: ConstraintType = ConstraintType.BUDGET
    max_cost_usd: float = Field(default=1.0, ge=0.0)


class TokenConstraint(DomainConstraint):
    """LLM token limit constraint."""
    constraint_type: ConstraintType = ConstraintType.TOKEN
    max_total_tokens: int = Field(default=8000, ge=0)


class ConfidenceConstraint(DomainConstraint):
    """Minimum output confidence constraint."""
    constraint_type: ConstraintType = ConstraintType.CONFIDENCE
    min_confidence_score: float = Field(default=0.85, ge=0.0, le=1.0)
