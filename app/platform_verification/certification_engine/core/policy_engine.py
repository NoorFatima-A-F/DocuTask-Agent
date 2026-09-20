"""
Configurable Policy Evaluation Engine.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple
from app.platform_verification.certification_engine.domain.interfaces import IPolicyEngine
from app.platform_verification.certification_engine.domain.models import (
    GateComparisonOperator,
    PolicyDefinition,
    PolicyRule,
    QualityGateCondition,
    Severity,
)


class ConfigurablePolicyEngine(IPolicyEngine):
    """Evaluates rule-based policies against verification metrics."""

    def __init__(self):
        self._policies: Dict[str, PolicyDefinition] = {}
        self._initialize_default_policies()

    def register_policy(self, policy: PolicyDefinition) -> None:
        self._policies[policy.id] = policy

    def evaluate_policy(self, policy_id: str, metrics: Dict[str, Any]) -> Tuple[bool, List[str]]:
        policy = self._policies.get(policy_id)
        if not policy:
            return False, [f"Policy '{policy_id}' not found in registry."]

        rule_results: List[Tuple[bool, str]] = []
        for rule in policy.rules:
            cond = QualityGateCondition(
                metric_name=rule.metric_name,
                operator=rule.operator,
                threshold=rule.threshold,
            )
            val = metrics.get(rule.metric_name)
            passed = cond.evaluate(val)
            msg = (
                f"Rule '{rule.name}' PASSED"
                if passed
                else f"Rule '{rule.name}' FAILED: {rule.metric_name} is {val}, expected {rule.operator.value} {rule.threshold}"
            )
            rule_results.append((passed, msg))

        if policy.logical_operator.upper() == "OR":
            overall_passed = any(passed for passed, _ in rule_results)
        else:  # Default AND
            overall_passed = all(passed for passed, _ in rule_results)

        failure_reasons = [msg for passed, msg in rule_results if not passed]
        return overall_passed, failure_reasons

    def _initialize_default_policies(self) -> None:
        # Production Release Policy
        self.register_policy(
            PolicyDefinition(
                id="PRODUCTION_RELEASE_POLICY",
                name="Production Release Policy",
                logical_operator="AND",
                description="Strict requirements for production readiness",
                rules=[
                    PolicyRule(
                        name="Zero Critical Vulnerabilities",
                        metric_name="critical_vulnerabilities",
                        operator=GateComparisonOperator.EQUALS,
                        threshold=0,
                        severity=Severity.CRITICAL,
                    ),
                    PolicyRule(
                        name="High Reliability Rate",
                        metric_name="availability_rate",
                        operator=GateComparisonOperator.GREATER_THAN_OR_EQUAL,
                        threshold=0.99,
                        severity=Severity.HIGH,
                    ),
                    PolicyRule(
                        name="Low Hallucination Rate",
                        metric_name="hallucination_rate",
                        operator=GateComparisonOperator.LESS_THAN_OR_EQUAL,
                        threshold=0.03,
                        severity=Severity.HIGH,
                    ),
                ],
            )
        )
