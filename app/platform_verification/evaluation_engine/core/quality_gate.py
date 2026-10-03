"""
Quality Gate Engine evaluating operational verification rules and release gating.
"""
from __future__ import annotations
from typing import Dict, List, Optional
from app.platform_verification.evaluation_engine.domain.models import (
    QualityGateRule,
    QualityGateDecision,
    QualityGateStatus,
    MetricResult,
    Severity,
)
from app.platform_verification.evaluation_engine.domain.interfaces import IQualityGateEngine


class QualityGateEngine(IQualityGateEngine):
    """Evaluates metrics against enterprise quality gates with deterministic multi-status outcomes."""

    def evaluate_gate(
        self, metric_results: List[MetricResult], rules: List[QualityGateRule]
    ) -> QualityGateDecision:
        metric_map: Dict[str, MetricResult] = {m.metric_id: m for m in metric_results}

        passed_rules: List[str] = []
        failed_rules: List[str] = []
        blocking_failures: List[str] = []
        warnings: List[str] = []
        recommendations: List[str] = []

        for rule in rules:
            if rule.metric_id not in metric_map:
                if rule.required:
                    msg = f"Required metric '{rule.metric_id}' was missing from evaluation."
                    failed_rules.append(rule.rule_id)
                    blocking_failures.append(msg)
                continue

            result = metric_map[rule.metric_id]
            val = result.raw_value
            target = rule.target_value
            passed = False

            if rule.condition == "gte":
                passed = val >= target
            elif rule.condition == "lte":
                passed = val <= target
            elif rule.condition == "gt":
                passed = val > target
            elif rule.condition == "lt":
                passed = val < target
            elif rule.condition == "eq":
                passed = val == target

            if passed:
                passed_rules.append(rule.rule_id)
            else:
                failed_rules.append(rule.rule_id)
                fail_msg = f"Rule '{rule.rule_id}' failed for {result.metric_name}: actual {val} {result.unit} did not satisfy {rule.condition} {target}."
                if rule.severity == Severity.CRITICAL and rule.required:
                    blocking_failures.append(fail_msg)
                    recommendations.append(f"Remediate critical violation: {rule.description or fail_msg}")
                else:
                    warnings.append(fail_msg)
                    recommendations.append(f"Investigate warning: {rule.description or fail_msg}")

        # Determine Overall Status
        if blocking_failures:
            status = QualityGateStatus.FAILED
        elif warnings:
            status = QualityGateStatus.CONDITIONAL
        else:
            status = QualityGateStatus.PASSED

        return QualityGateDecision(
            status=status,
            passed_rules=passed_rules,
            failed_rules=failed_rules,
            total_rules=len(rules),
            blocking_failures=blocking_failures,
            warnings=warnings,
            recommendations=recommendations,
        )
