"""
Evaluation Domain Models.
Defines structured evaluation metrics, dimensions, scoring envelopes, and comprehensive reports.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class EvaluationDimension(str, Enum):
    """Core evaluation dimensions for analyzing autonomous agent runs."""
    GOAL_ACHIEVEMENT = "GOAL_ACHIEVEMENT"
    QUALITY = "QUALITY"
    CONFIDENCE = "CONFIDENCE"
    CORRECTNESS = "CORRECTNESS"
    EFFICIENCY = "EFFICIENCY"
    COST = "COST"
    LATENCY = "LATENCY"
    TOKEN_UTILIZATION = "TOKEN_UTILIZATION"
    MEMORY_UTILIZATION = "MEMORY_UTILIZATION"
    RISK_AND_SAFETY = "RISK_AND_SAFETY"
    PLANNER_COGNITION = "PLANNER_COGNITION"
    EXECUTION_RUNTIME = "EXECUTION_RUNTIME"
    TOOL_RELIABILITY = "TOOL_RELIABILITY"


class EvaluationMetric(BaseModel):
    """An individual quantitative or qualitative evaluation metric."""
    name: str
    dimension: EvaluationDimension
    score: float = Field(ge=0.0, le=1.0)
    weight: float = Field(default=1.0, ge=0.0)
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    evidence: List[str] = Field(default_factory=list)
    details: Dict[str, Any] = Field(default_factory=dict)

    model_config = {"frozen": True}


class DimensionEvaluation(BaseModel):
    """Aggregated evaluation for a specific dimension."""
    dimension: EvaluationDimension
    score: float = Field(ge=0.0, le=1.0)
    status: str = Field(default="SATISFACTORY")  # EXCELLENT, SATISFACTORY, MARGINAL, POOR
    metrics: List[EvaluationMetric] = Field(default_factory=list)
    findings: List[str] = Field(default_factory=list)
    recommendation_hints: List[str] = Field(default_factory=list)

    model_config = {"frozen": True}


class EvaluationReport(BaseModel):
    """Comprehensive evaluation report summarizing all analytical and quantitative findings."""
    report_id: UUID = Field(default_factory=uuid4)
    execution_id: UUID
    overall_score: float = Field(ge=0.0, le=1.0)
    dimensions: Dict[str, DimensionEvaluation] = Field(default_factory=dict)
    summary: str = Field(default="")
    key_strengths: List[str] = Field(default_factory=list)
    key_weaknesses: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = {"frozen": True}
