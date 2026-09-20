"""
Enterprise Quality Gate Engine for evaluating functional, performance, AI quality, security, and reliability gates.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from app.platform_verification.certification_engine.domain.interfaces import IQualityGateEngine
from app.platform_verification.certification_engine.domain.models import (
    ConditionEvaluationResult,
    ExceptionRequest,
    ExceptionStatus,
    FailureAction,
    GateCategory,
    GateComparisonOperator,
    GateEvaluationResult,
    QualityGateCondition,
    QualityGateDefinition,
    Severity,
)


class EnterpriseQualityGateEngine(IQualityGateEngine):
    """Executes configurable quality gates against execution metrics with exception handling."""

    def __init__(self):
        self._gates: Dict[str, QualityGateDefinition] = {}
        self._initialize_default_gates()

    def register_gate(self, gate: QualityGateDefinition) -> None:
        self._gates[gate.id] = gate

    def evaluate_gates(
        self,
        gate_ids: List[str],
        metrics: Dict[str, Any],
        active_exceptions: Optional[List[ExceptionRequest]] = None,
    ) -> List[GateEvaluationResult]:
        exceptions = active_exceptions or []
        active_exception_map = {
            e.gate_id: e for e in exceptions if e.status == ExceptionStatus.APPROVED
        }

        results: List[GateEvaluationResult] = []
        for gid in gate_ids:
            gate = self._gates.get(gid)
            if not gate:
                continue

            cond_results: List[ConditionEvaluationResult] = []
            failure_reasons: List[str] = []

            for cond in gate.conditions:
                actual_val = metrics.get(cond.metric_name)
                passed = cond.evaluate(actual_val)
                msg = (
                    f"Passed: {cond.metric_name} = {actual_val}"
                    if passed
                    else f"Failed: {cond.metric_name} is {actual_val}, required {cond.operator.value} {cond.threshold}"
                )
                
                # Check for active approved exception
                if not passed and gate.id in active_exception_map:
                    exc = active_exception_map[gate.id]
                    passed = True
                    msg += f" [WAIVED via approved exception {exc.exception_id}: {exc.reason}]"

                if not passed:
                    failure_reasons.append(msg)

                cond_results.append(
                    ConditionEvaluationResult(
                        metric_name=cond.metric_name,
                        operator=cond.operator.value,
                        threshold=cond.threshold,
                        actual_value=actual_val,
                        passed=passed,
                        message=msg,
                    )
                )

            gate_passed = len(failure_reasons) == 0
            results.append(
                GateEvaluationResult(
                    gate_id=gate.id,
                    gate_name=gate.name,
                    category=gate.category,
                    passed=gate_passed,
                    condition_results=cond_results,
                    severity=gate.severity,
                    failure_action=gate.failure_action,
                    failure_reasons=failure_reasons,
                )
            )

        return results

    def _initialize_default_gates(self) -> None:
        # 1. Functional Gate
        self.register_gate(
            QualityGateDefinition(
                id="GATE_FUNCTIONAL_ACCURACY",
                name="Functional Extraction & Workflow Accuracy Gate",
                category=GateCategory.FUNCTIONAL,
                severity=Severity.HIGH,
                failure_action=FailureAction.BLOCK_RELEASE,
                conditions=[
                    QualityGateCondition(
                        metric_name="extraction_accuracy",
                        operator=GateComparisonOperator.GREATER_THAN_OR_EQUAL,
                        threshold=0.90,
                    ),
                    QualityGateCondition(
                        metric_name="workflow_completion_rate",
                        operator=GateComparisonOperator.GREATER_THAN_OR_EQUAL,
                        threshold=0.95,
                    ),
                ],
            )
        )

        # 2. Performance Gate
        self.register_gate(
            QualityGateDefinition(
                id="GATE_PERFORMANCE_SLA",
                name="Performance & SLA Latency Gate",
                category=GateCategory.PERFORMANCE,
                severity=Severity.HIGH,
                failure_action=FailureAction.BLOCK_RELEASE,
                conditions=[
                    QualityGateCondition(
                        metric_name="p95_latency_ms",
                        operator=GateComparisonOperator.LESS_THAN_OR_EQUAL,
                        threshold=1500.0,
                    ),
                    QualityGateCondition(
                        metric_name="throughput_docs_per_sec",
                        operator=GateComparisonOperator.GREATER_THAN_OR_EQUAL,
                        threshold=5.0,
                    ),
                ],
            )
        )

        # 3. AI Quality Gate
        self.register_gate(
            QualityGateDefinition(
                id="GATE_AI_QUALITY",
                name="AI Quality, Grounding & Hallucination Gate",
                category=GateCategory.AI_QUALITY,
                severity=Severity.CRITICAL,
                failure_action=FailureAction.BLOCK_RELEASE,
                conditions=[
                    QualityGateCondition(
                        metric_name="hallucination_rate",
                        operator=GateComparisonOperator.LESS_THAN_OR_EQUAL,
                        threshold=0.03,
                    ),
                    QualityGateCondition(
                        metric_name="grounding_score",
                        operator=GateComparisonOperator.GREATER_THAN_OR_EQUAL,
                        threshold=0.92,
                    ),
                ],
            )
        )

        # 4. Security Gate
        self.register_gate(
            QualityGateDefinition(
                id="GATE_SECURITY_COMPLIANCE",
                name="Security & Threat Mitigation Gate",
                category=GateCategory.SECURITY,
                severity=Severity.CRITICAL,
                failure_action=FailureAction.BLOCK_RELEASE,
                conditions=[
                    QualityGateCondition(
                        metric_name="critical_vulnerabilities",
                        operator=GateComparisonOperator.EQUALS,
                        threshold=0,
                    ),
                    QualityGateCondition(
                        metric_name="prompt_injection_resistance",
                        operator=GateComparisonOperator.GREATER_THAN_OR_EQUAL,
                        threshold=0.98,
                    ),
                ],
            )
        )

        # 5. Reliability Gate
        self.register_gate(
            QualityGateDefinition(
                id="GATE_RELIABILITY",
                name="Reliability & Recovery Gate",
                category=GateCategory.RELIABILITY,
                severity=Severity.HIGH,
                failure_action=FailureAction.REQUIRE_MANUAL_APPROVAL,
                conditions=[
                    QualityGateCondition(
                        metric_name="failure_rate",
                        operator=GateComparisonOperator.LESS_THAN_OR_EQUAL,
                        threshold=0.01,
                    ),
                    QualityGateCondition(
                        metric_name="recovery_success_rate",
                        operator=GateComparisonOperator.GREATER_THAN_OR_EQUAL,
                        threshold=0.95,
                    ),
                ],
            )
        )
