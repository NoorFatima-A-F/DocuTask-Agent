"""Execution Simulator for DocuTask Autonomous Planning Platform.

Simulates candidate plan execution using Monte Carlo trials to compute failure probabilities,
critical path bottlenecks, token usage distributions, and execution resilience.
"""

from __future__ import annotations

import random
from typing import Any, Dict, List
from pydantic import BaseModel, Field

from app.runtime.planning.strategy_generator import CandidateStrategy


class SimulationResult(BaseModel):
    """Detailed output of Monte Carlo execution simulation."""
    strategy_id: str
    simulated_iterations: int = 1000
    simulated_success_rate: float
    mean_duration_ms: float
    p95_duration_ms: float
    simulated_token_usage: int
    simulated_total_cost_usd: float
    predicted_failure_points: List[Dict[str, Any]] = Field(default_factory=list)
    is_safe_to_execute: bool
    simulation_notes: str = ""


class ExecutionSimulator:
    """Performs dry-run simulation of candidate strategies before dispatching to worker pool."""

    def __init__(self, seed: int = 42) -> None:
        self.random = random.Random(seed)

    def simulate(
        self,
        strategy: CandidateStrategy,
        iterations: int = 500,
    ) -> SimulationResult:
        successes = 0
        durations: List[float] = []
        failure_hotspots: Dict[str, int] = {s.step_id: 0 for s in strategy.steps}

        for _ in range(iterations):
            run_success = True
            run_duration = 0.0

            for step in strategy.steps:
                # Stochastic execution sample
                base_lat = step.estimated_latency_ms
                jitter = self.random.gauss(0, base_lat * 0.1)
                step_lat = max(1.0, base_lat + jitter)
                run_duration += step_lat

                # Failure check
                if self.random.random() < step.failure_probability:
                    failure_hotspots[step.step_id] += 1
                    # If step has fallback, try fallback
                    if step.fallback_capability_id:
                        run_duration += 300.0  # fallback delay
                    else:
                        run_success = False
                        break

            if run_success:
                successes += 1
            durations.append(run_duration)

        durations.sort()
        mean_dur = sum(durations) / len(durations)
        p95_idx = int(len(durations) * 0.95)
        p95_dur = durations[min(p95_idx, len(durations) - 1)]
        success_rate = successes / iterations

        failure_points = [
            {"step_id": sid, "failure_count": count, "failure_rate": round(count / iterations, 4)}
            for sid, count in failure_hotspots.items()
            if count > 0
        ]

        is_safe = success_rate >= 0.92 and strategy.constraint_compliance.get("is_valid", True)

        return SimulationResult(
            strategy_id=strategy.strategy_id,
            simulated_iterations=iterations,
            simulated_success_rate=round(success_rate, 4),
            mean_duration_ms=round(mean_dur, 2),
            p95_duration_ms=round(p95_dur, 2),
            simulated_token_usage=strategy.token_estimate,
            simulated_total_cost_usd=round(strategy.estimated_total_cost_usd, 6),
            predicted_failure_points=failure_points,
            is_safe_to_execute=is_safe,
            simulation_notes=f"Simulated {iterations} Monte Carlo executions. Predicted success rate: {success_rate * 100:.1f}%.",
        )
