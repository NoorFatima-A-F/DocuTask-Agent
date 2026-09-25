from dataclasses import dataclass
from enum import Enum
from typing import List
from .evaluator import IndependentEvaluationResult

class QualityGateDecision(str, Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    CONDITIONAL = "CONDITIONAL"
    MANUAL_REVIEW_REQUIRED = "MANUAL_REVIEW_REQUIRED"

@dataclass(frozen=True)
class GateEvaluationSummary:
    decision: QualityGateDecision
    blockers_triggered: List[str]
    soft_warnings: List[str]

class QualityGateDecisionEngine:
    @staticmethod
    def evaluate_gates(evaluation: IndependentEvaluationResult) -> GateEvaluationSummary:
        blockers = []
        warnings = []

        for crit in evaluation.criteria_results:
            if not crit.passed:
                if crit.is_hard_blocker:
                    blockers.append(f"Hard blocker failed: '{crit.metric_name}' value {crit.actual_value} does not satisfy {crit.operator} {crit.threshold}")
                else:
                    warnings.append(f"Soft warning: '{crit.metric_name}' value {crit.actual_value} below threshold {crit.threshold}")

        if blockers:
            decision = QualityGateDecision.FAILED
        elif warnings:
            decision = QualityGateDecision.CONDITIONAL
        else:
            decision = QualityGateDecision.PASSED

        return GateEvaluationSummary(
            decision=decision,
            blockers_triggered=blockers,
            soft_warnings=warnings
        )
