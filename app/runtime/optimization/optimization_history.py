"""
Multi-Objective Optimization Engine - Optimization History
Maintains provenance records of optimizer runs, candidate inputs, and selected optimal plans.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
from dataclasses import dataclass, asdict


@dataclass
class OptimizationRunRecord:
    run_id: str
    timestamp_utc: str
    context_id: str
    weights: Dict[str, float]
    selected_plan_id: str
    selected_plan_utility: float
    candidate_count: int
    pareto_frontier_count: int
    raw_candidates: List[Dict[str, Any]]
    pareto_frontier: List[Dict[str, Any]]


class OptimizationHistoryTracker:
    """Maintains an in-memory & queryable log of all runtime optimization decisions."""

    def __init__(self, max_history: int = 500):
        self.max_history = max_history
        self._history: List[OptimizationRunRecord] = []

    def record_run(self, record: OptimizationRunRecord) -> None:
        self._history.append(record)
        if len(self._history) > self.max_history:
            self._history.pop(0)

    def get_runs(self, limit: int = 50) -> List[Dict[str, Any]]:
        return [asdict(r) for r in reversed(self._history[-limit:])]

    def get_by_run_id(self, run_id: str) -> Optional[OptimizationRunRecord]:
        for r in self._history:
            if r.run_id == run_id:
                return r
        return None


optimization_history = OptimizationHistoryTracker()
