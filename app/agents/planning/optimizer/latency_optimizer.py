"""
Latency Optimizer for Autonomous Plan Optimization Engine.
Computes DAG topological concurrency waves, removes spurious sequential dependencies,
and optimizes wall-clock completion time.
"""

from __future__ import annotations

import copy
import logging
from collections import defaultdict
from typing import Dict, List, Tuple

from app.agents.planning.execution_plan import ExecutionPlan, PlannedTask

logger = logging.getLogger(__name__)

# Standard task duration estimates in milliseconds
DEFAULT_DURATIONS_MS: Dict[str, float] = {
    "ocr": 120.0,
    "extract": 180.0,
    "validate": 40.0,
    "classify": 60.0,
    "format": 25.0,
    "audit": 50.0,
}


class LatencyOptimizer:
    """Optimizes ExecutionPlan for minimum wall-clock completion time."""

    def __init__(self, action_durations: Dict[str, float] = None) -> None:
        self.action_durations = action_durations or DEFAULT_DURATIONS_MS

    def get_task_duration(self, task: PlannedTask) -> float:
        """Estimates task duration in milliseconds."""
        for action, dur in self.action_durations.items():
            if action in task.action.lower() or action in task.name.lower():
                return dur
        return 100.0

    def compute_concurrency_waves(self, plan: ExecutionPlan) -> List[List[PlannedTask]]:
        """Groups tasks into parallel execution waves using Kahn's topological ranking."""
        task_map = {t.task_id: t for t in plan.tasks}
        in_degree = {t.task_id: len(t.dependencies) for t in plan.tasks}
        children: Dict[str, List[str]] = defaultdict(list)
        for t in plan.tasks:
            for dep in t.dependencies:
                children[dep].append(t.task_id)

        waves: List[List[PlannedTask]] = []
        current_wave = [task_map[tid] for tid, deg in in_degree.items() if deg == 0]

        while current_wave:
            waves.append(current_wave)
            next_wave_ids: List[str] = []
            for task in current_wave:
                for child_id in children[task.task_id]:
                    in_degree[child_id] -= 1
                    if in_degree[child_id] == 0:
                        next_wave_ids.append(child_id)
            current_wave = [task_map[tid] for tid in next_wave_ids]

        return waves

    def estimate_total_latency(self, plan: ExecutionPlan) -> float:
        """Calculates expected critical path latency in milliseconds across waves."""
        waves = self.compute_concurrency_waves(plan)
        total_latency = 0.0
        for wave in waves:
            # Latency of a parallel wave is the max latency among tasks in that wave
            wave_max = max((self.get_task_duration(t) for t in wave), default=0.0)
            total_latency += wave_max
        return total_latency

    def optimize(self, plan: ExecutionPlan) -> Tuple[ExecutionPlan, float]:
        """
        Maximizes parallelism by removing artificial dependencies between independent tasks.
        Returns (optimized_plan, speedup_percentage).
        """
        optimized = copy.deepcopy(plan)
        initial_latency = self.estimate_total_latency(plan)

        # Identify independent extraction tasks and remove false chaining
        task_map = {t.task_id: t for t in optimized.tasks}
        for task in optimized.tasks:
            if "extract" in task.action.lower():
                # Extraction only truly depends on ingest/ocr tasks, not on sibling extractions
                pruned_deps = []
                for dep_id in task.dependencies:
                    dep_task = task_map.get(dep_id)
                    if dep_task and ("ocr" in dep_task.action.lower() or "ingest" in dep_task.action.lower()):
                        pruned_deps.append(dep_id)
                    elif dep_task and not ("extract" in dep_task.action.lower()):
                        pruned_deps.append(dep_id)
                task.dependencies = pruned_deps

        optimized_latency = self.estimate_total_latency(optimized)
        speedup = (initial_latency - optimized_latency) / initial_latency if initial_latency > 0 else 0.0
        return optimized, max(0.0, speedup)
