"""Canary Progressive Rollout Strategy with Multi-Step Metric Evaluation."""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


@dataclass
class CanaryStep:
    """A progressive traffic milestone."""
    percentage: float  # 1.0, 5.0, 25.0, 50.0, 100.0
    evaluation_duration_seconds: float = 1.0


class CanaryDeploymentStrategy:
    """Executes canary traffic shift (1% -> 5% -> 25% -> 50% -> 100%) with error rate gates."""

    DEFAULT_STEPS = [
        CanaryStep(1.0),
        CanaryStep(5.0),
        CanaryStep(25.0),
        CanaryStep(50.0),
        CanaryStep(100.0),
    ]

    def __init__(self, steps: Optional[List[CanaryStep]] = None, max_error_rate: float = 0.01) -> None:
        self.steps = steps or self.DEFAULT_STEPS
        self.max_error_rate = max_error_rate

    def execute(
        self,
        set_weight_fn: Callable[[float], None],
        evaluate_metrics_fn: Callable[[float], Dict[str, float]],  # returns {"error_rate": ..., "p95_latency_ms": ...}
    ) -> bool:
        """Progress through canary steps evaluating error rates at each increment."""
        for step in self.steps:
            # 1. Shift traffic weight
            set_weight_fn(step.percentage)

            # 2. Evaluate canary telemetry
            metrics = evaluate_metrics_fn(step.percentage)
            err_rate = metrics.get("error_rate", 0.0)

            if err_rate > self.max_error_rate:
                # Halt and trigger rollback
                return False

        return True
