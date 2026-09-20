"""Canary Progressive Traffic Shifting Strategy."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Callable, Dict, List, Optional, Tuple
from ..core.exceptions import StrategyExecutionException


@dataclass
class CanaryStep:
    """Evaluation result for a single traffic canary step."""
    step_index: int
    traffic_percentage: int
    observed_error_rate: float
    observed_p99_latency_ms: float
    passed: bool
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    details: str = ""


class CanaryStrategy:
    """Orchestrates canary rollout with progressive traffic increments and automated SLO gates."""

    DEFAULT_STEPS = [5, 25, 50, 100]

    def __init__(
        self,
        steps: Optional[List[int]] = None,
        max_error_rate: float = 0.01,
        max_p99_latency_ms: float = 250.0,
    ):
        self.steps = steps or self.DEFAULT_STEPS
        self.max_error_rate = max_error_rate
        self.max_p99_latency_ms = max_p99_latency_ms
        self.current_step_index: int = 0
        self.aborted: bool = False
        self.history: List[CanaryStep] = []

    def evaluate_step(
        self,
        step_index: int,
        traffic_pct: int,
        error_rate: float,
        p99_ms: float,
    ) -> CanaryStep:
        """Evaluates health criteria for a specific traffic split."""
        passed = (error_rate <= self.max_error_rate) and (p99_ms <= self.max_p99_latency_ms)
        details = "Passed SLO thresholds" if passed else (
            f"Breached SLO: error_rate={error_rate*100:.2f}% (max {self.max_error_rate*100:.2f}%), "
            f"p99={p99_ms:.1f}ms (max {self.max_p99_latency_ms:.1f}ms)"
        )
        step = CanaryStep(
            step_index=step_index,
            traffic_percentage=traffic_pct,
            observed_error_rate=error_rate,
            observed_p99_latency_ms=p99_ms,
            passed=passed,
            details=details,
        )
        self.history.append(step)
        if not passed:
            self.aborted = True
        return step

    def execute(
        self,
        metrics_provider: Callable[[int, int], Tuple[float, float]],
    ) -> List[CanaryStep]:
        """Executes full multi-step canary progression."""
        results: List[CanaryStep] = []
        for idx, pct in enumerate(self.steps, start=1):
            self.current_step_index = idx
            err_rate, p99 = metrics_provider(idx, pct)
            step_eval = self.evaluate_step(
                step_index=idx,
                traffic_pct=pct,
                error_rate=err_rate,
                p99_ms=p99,
            )
            results.append(step_eval)
            if not step_eval.passed:
                raise StrategyExecutionException(
                    f"Canary rollout automatically aborted at step {idx} ({pct}% traffic): {step_eval.details}"
                )
        return results
