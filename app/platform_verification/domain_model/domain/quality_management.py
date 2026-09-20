"""
Quality Management Domain: Quality Gates, Blocker Policies, and Decision Aggregation.
"""
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
import uuid


class GateSeverity(str, Enum):
    HARD_BLOCKER = "HARD_BLOCKER"
    SOFT_BLOCKER = "SOFT_BLOCKER"
    WARNING_ONLY = "WARNING_ONLY"


class QualityDecisionOutcome(str, Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    CONDITIONALLY_PASSED = "CONDITIONALLY_PASSED"
    WAIVED = "WAIVED"


class QualityGate(BaseModel):
    gate_id: str = Field(default_factory=lambda: f"qgate_{uuid.uuid4().hex[:8]}")
    name: str
    criteria: Dict[str, Any]
    severity: GateSeverity = GateSeverity.HARD_BLOCKER
    is_required: bool = True
    weight: float = 1.0


class QualityDecision(BaseModel):
    decision_id: str = Field(default_factory=lambda: f"qdec_{uuid.uuid4().hex[:8]}")
    execution_id: str
    gate_id: str
    gate_name: str
    outcome: QualityDecisionOutcome = QualityDecisionOutcome.PASSED
    composite_score: float = 1.0
    passed_requirements_count: int
    failed_requirements_count: int
    reason: str = "All acceptance criteria successfully satisfied."
    evaluated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
