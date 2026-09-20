from dataclasses import dataclass
from typing import Dict, List
from .metric_pipeline import ComputedMetric
from .definitions import VerificationSpecification

@dataclass(frozen=True)
class EvaluationCriterionResult:
    metric_name: str
    actual_value: float
    threshold: float
    operator: str
    passed: bool
    is_hard_blocker: bool

@dataclass(frozen=True)
class IndependentEvaluationResult:
    specification_id: str
    overall_passed: bool
    quality_score: float
    criteria_results: List[EvaluationCriterionResult]
    recommendations: List[str]

class IndependentEvaluationEngine:
    @staticmethod
    def evaluate(spec: VerificationSpecification, metrics: Dict[str, ComputedMetric]) -> IndependentEvaluationResult:
        criteria_results = []
        overall_passed = True
        total_rules = len(spec.quality_gate_rules)
        passed_rules = 0

        for rule in spec.quality_gate_rules:
            metric = metrics.get(rule.metric_name)
            actual = metric.value if metric else 0.0

            passed = False
            if rule.operator == ">=":
                passed = actual >= rule.threshold
            elif rule.operator == "<=":
                passed = actual <= rule.threshold
            elif rule.operator == "==":
                passed = actual == rule.threshold
            elif rule.operator == ">":
                passed = actual > rule.threshold
            elif rule.operator == "<":
                passed = actual < rule.threshold

            if passed:
                passed_rules += 1
            elif rule.is_hard_blocker:
                overall_passed = False

            criteria_results.append(EvaluationCriterionResult(
                metric_name=rule.metric_name,
                actual_value=actual,
                threshold=rule.threshold,
                operator=rule.operator,
                passed=passed,
                is_hard_blocker=rule.is_hard_blocker
            ))

        score = passed_rules / max(1, total_rules)
        recs = [] if overall_passed else ["Tune model extraction prompts to improve precision", "Optimize IO latency"]

        return IndependentEvaluationResult(
            specification_id=spec.specification_id,
            overall_passed=overall_passed,
            quality_score=score,
            criteria_results=criteria_results,
            recommendations=recs
        )
