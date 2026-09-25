"""
AOIS-HROP Phase 13.7 - Root Cause Engine
Infers root causes using Replay snapshots, Learning graph priors, Optimization reports, and Telemetry event traces.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List
import uuid
from app.runtime.operations.diagnostics.dependency_analyzer import DependencyAnalyzer
from app.runtime.operations.diagnostics.causal_reasoner import CausalReasoner, CausalDiagnosticExplanation
from app.runtime.operations.diagnostics.diagnosis_confidence import DiagnosisConfidenceCalculator
from app.runtime.operations.events.operation_events import HealingActionType


@dataclass
class RootCauseDiagnosis:
    diagnosis_id: str
    incident_id: str
    primary_culprit_subsystem: str
    error_pattern: str
    confidence: float
    explanation: CausalDiagnosticExplanation
    recommended_healing_action: HealingActionType
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class RootCauseEngine:
    """
    Executes automated root-cause inference for active incidents.
    """

    def __init__(self):
        self.dep_analyzer = DependencyAnalyzer()
        self.causal_reasoner = CausalReasoner()
        self.confidence_calc = DiagnosisConfidenceCalculator()

    def infer_root_cause(
        self,
        incident_id: str,
        anomalous_subsystems: List[str],
        error_type: str = "GENERIC_DEGRADATION",
    ) -> RootCauseDiagnosis:
        culprit = self.dep_analyzer.trace_root_culprit(anomalous_subsystems)
        confidence = self.confidence_calc.calculate_confidence()
        explanation = self.causal_reasoner.construct_explanation(
            culprit_subsystem=culprit,
            error_type=error_type,
            affected_subsystems=anomalous_subsystems,
            confidence=confidence,
        )

        # Select recommended healing action based on error and culprit
        if error_type in ("HUNG_WORKER", "WORKER_CRASH", "RETRY_STORM"):
            action = HealingActionType.WORKER_RESTART
        elif error_type in ("FROZEN_PLANNER", "DEADLOCK"):
            action = HealingActionType.PLANNER_REPLAN
        elif error_type in ("MEMORY_LEAK", "CACHE_CORRUPTION"):
            action = HealingActionType.MEMORY_REPAIR
        elif error_type in ("MODEL_RATE_LIMIT", "OCR_FAILURE"):
            action = HealingActionType.FALLBACK_MODEL_ENGAGE
        else:
            action = HealingActionType.RESOURCE_REALLOCATE

        return RootCauseDiagnosis(
            diagnosis_id=f"diag-{uuid.uuid4().hex[:8]}",
            incident_id=incident_id,
            primary_culprit_subsystem=culprit,
            error_pattern=error_type,
            confidence=confidence,
            explanation=explanation,
            recommended_healing_action=action,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
