"""Argo-Rollouts aligned Stepwise Canary Strategy (Req 36)."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Callable, List, Optional, Tuple


@dataclass
class CanaryStepEvaluation:
    step_index: int
    traffic_percentage: int
    error_rate: float
    p95_latency_ms: float
    passed: bool
    details: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class CanaryStrategy:
    """Orchestrates traffic shifting across configurable step increments (1%, 5%, 10%, 25%, 50%, 100%)."""

    DEFAULT_STEPS = [1, 5, 10, 25, 50, 100]

    def __init__(
        self,
        steps: Optional[List[int]] = None,
        max_error_rate: float = 0.01,
        max_p95_latency_ms: float = 250.0,
    ):
        self.steps = steps or self.DEFAULT_STEPS
        self.max_error_rate = max_error_rate
        self.max_p95_latency_ms = max_p95_latency_ms
        self.history: List[CanaryStepEvaluation] = []

    def evaluate_step(
        self,
        step_index: int,
        traffic_pct: int,
        observed_error_rate: float,
        observed_p95_ms: float,
    ) -> CanaryStepEvaluation:
        passed = (observed_error_rate <= self.max_error_rate) and (observed_p95_ms <= self.max_p95_latency_ms)
        details = (
            "SLO verified"
            if passed
            else f"SLO breached: error_rate={observed_error_rate*100:.2f}%, p95={observed_p95_ms:.1f}ms"
        )
        step = CanaryStepEvaluation(
            step_index=step_index,
            traffic_percentage=traffic_pct,
            error_rate=observed_error_rate,
            p95_latency_ms=observed_p95_ms,
            passed=passed,
            details=details,
        )
        self.history.append(step)
        return step
