"""
Monte Carlo Planner Simulator.

Performs stochastic pre-execution simulations over ExecutionDAG topologies to predict
completion times, tail latencies ($P_{90}, P_{99}$), expected cost, and failure probabilities.
"""

from __future__ import annotations

import random
from typing import List
from pydantic import BaseModel
from app.runtime.planning.graph.dag import ExecutionDAG


class SimulationResult(BaseModel):
    mission_id: str
    trials_count: int
    mean_completion_ms: float
    p50_completion_ms: float
    p90_completion_ms: float
    p99_completion_ms: float
    expected_total_cost_usd: float
    expected_total_tokens: int
    expected_retry_probability: float
    bottleneck_node_ids: List[str]


class PlannerSimulator:
    """Simulates execution variations using Monte Carlo sampling."""

    @classmethod
    def simulate_dag(
        cls, dag: ExecutionDAG, num_trials: int = 100
    ) -> SimulationResult:
        """Simulates stochastic node execution runtimes and failure rates."""
        crit_nodes, base_dur = dag.compute_critical_path()
        durations: List[float] = []
        retry_counts = 0
        total_costs: List[float] = []

        base_cost = sum(n.estimated_cost_usd for n in dag.nodes.values())
        base_tokens = sum(n.estimated_tokens for n in dag.nodes.values())

        for _ in range(num_trials):
            # Stochastic variance: +/- 20% lognormal jitter
            trial_crit_dur = 0.0
            for nid in crit_nodes:
                node = dag.nodes[nid]
                jitter = random.uniform(0.85, 1.25)
                runtime = node.estimated_runtime_ms * jitter
                # Random retry check
                if random.random() < node.risk_score:
                    runtime += node.estimated_runtime_ms * 1.5
                    retry_counts += 1
                trial_crit_dur += runtime

            durations.append(trial_crit_dur)
            total_costs.append(base_cost * random.uniform(0.95, 1.10))

        durations.sort()
        p50 = durations[int(num_trials * 0.50)]
        p90 = durations[int(num_trials * 0.90)]
        p99 = durations[min(num_trials - 1, int(num_trials * 0.99))]
        mean_dur = sum(durations) / len(durations)

        return SimulationResult(
            mission_id=dag.mission_id,
            trials_count=num_trials,
            mean_completion_ms=round(mean_dur, 2),
            p50_completion_ms=round(p50, 2),
            p90_completion_ms=round(p90, 2),
            p99_completion_ms=round(p99, 2),
            expected_total_cost_usd=round(sum(total_costs) / len(total_costs), 5),
            expected_total_tokens=base_tokens,
            expected_retry_probability=round(retry_counts / (num_trials * max(1, len(dag.nodes))), 3),
            bottleneck_node_ids=crit_nodes[:3],
        )
