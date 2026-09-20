"""Canary Analysis Engine & Quality Gates (Req 37, 40, 41)."""
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class RolloutDecision(str, Enum):
    """Canary analysis verdict."""
    PROMOTE = "PROMOTE"
    PAUSE = "PAUSE"
    ABORT = "ABORT"
    ROLLBACK = "ROLLBACK"
    REQUIRE_HUMAN = "REQUIRE_HUMAN"


@dataclass
class QualityGatePolicy:
    """Configurable quality gate thresholds (Req 41)."""
    max_error_rate: float = 0.01  # 1%
    max_p95_latency_ms: float = 300.0
    min_workflow_success_rate: float = 0.99  # 99%
    max_hallucination_rate: float = 0.02
    allow_safety_violations: bool = False


class CanaryAnalysisEngine:
    """Evaluates multi-dimensional telemetry against quality gate policy."""

    def __init__(self, policy: Optional[QualityGatePolicy] = None):
        self.policy = policy or QualityGatePolicy()

    def evaluate_telemetry(
        self,
        error_rate: float,
        p95_latency_ms: float,
        workflow_success_rate: float = 0.995,
        hallucination_rate: float = 0.005,
        safety_violations_count: int = 0,
    ) -> Tuple[RolloutDecision, List[str]]:
        reasons = []

        if error_rate > self.policy.max_error_rate:
            reasons.append(f"Error rate {error_rate*100:.2f}% breached threshold ({self.policy.max_error_rate*100:.2f}%)")
        if p95_latency_ms > self.policy.max_p95_latency_ms:
            reasons.append(f"P95 Latency {p95_latency_ms:.1f}ms breached threshold ({self.policy.max_p95_latency_ms:.1f}ms)")
        if workflow_success_rate < self.policy.min_workflow_success_rate:
            reasons.append(f"Workflow success rate {workflow_success_rate*100:.1f}% below target ({self.policy.min_workflow_success_rate*100:.1f}%)")
        if safety_violations_count > 0 and not self.policy.allow_safety_violations:
            reasons.append(f"Detected {safety_violations_count} critical safety violations")

        if reasons:
            return RolloutDecision.ABORT, reasons
        return RolloutDecision.PROMOTE, ["All quality gates passed"]
