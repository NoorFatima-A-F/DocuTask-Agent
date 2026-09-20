"""
Composite Quality Gate & Invariant Evaluation Engine
"""
from typing import List, Dict, Any
from app.platform_verification.domain.models import MetricResult, QualityGateRule, QualityGateResult

class QualityGateEngine:
    @staticmethod
    def evaluate_gates(
        metrics: List[MetricResult],
        rules: List[QualityGateRule]
    ) -> QualityGateResult:
        metric_map = {m.metric_name: m.value for m in metrics}
        evaluated_rules = []
        hard_violations = 0
        soft_warnings = 0

        for rule in rules:
            actual_val = metric_map.get(rule.metric_name)
            passed = False
            if actual_val is not None:
                if rule.operator == ">=":
                    passed = actual_val >= rule.threshold
                elif rule.operator == "<=":
                    passed = actual_val <= rule.threshold
                elif rule.operator == ">":
                    passed = actual_val > rule.threshold
                elif rule.operator == "<":
                    passed = actual_val < rule.threshold
                elif rule.operator == "==":
                    passed = abs(actual_val - rule.threshold) < 1e-6

            if not passed:
                if rule.is_hard_blocker:
                    hard_violations += 1
                else:
                    soft_warnings += 1

            evaluated_rules.append({
                "rule_id": rule.rule_id,
                "metric_name": rule.metric_name,
                "operator": rule.operator,
                "threshold": rule.threshold,
                "actual_value": actual_val,
                "is_hard_blocker": rule.is_hard_blocker,
                "passed": passed
            })

        gate_passed = (hard_violations == 0)
        return QualityGateResult(
            gate_passed=gate_passed,
            hard_violations_count=hard_violations,
            soft_warnings_count=soft_warnings,
            evaluated_rules=evaluated_rules
        )

quality_gate_engine = QualityGateEngine()
