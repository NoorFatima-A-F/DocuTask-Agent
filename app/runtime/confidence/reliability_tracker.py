"""
Scientific Confidence Engine - Reliability Tracker
Tracks historical empirical accuracy and reliability metrics per worker, domain, and model.
"""

from typing import Dict, List, Any
import math


class ReliabilityTracker:
    """Maintains rolling and cumulative reliability records."""

    def __init__(self):
        self._records: Dict[str, Dict[str, int]] = {}

    def record_outcome(self, entity_key: str, success: bool) -> None:
        if entity_key not in self._records:
            self._records[entity_key] = {"successes": 0, "total": 0}

        self._records[entity_key]["total"] += 1
        if success:
            self._records[entity_key]["successes"] += 1

    def get_reliability(self, entity_key: str, prior_alpha: float = 19.0, prior_beta: float = 1.0) -> float:
        """Bayesian smoothed empirical mean: (alpha + successes) / (alpha + beta + total)."""
        stats = self._records.get(entity_key, {"successes": 0, "total": 0})
        s = stats["successes"]
        t = stats["total"]

        smoothed_mean = (prior_alpha + s) / (prior_alpha + prior_beta + t)
        return round(smoothed_mean, 4)

    def get_sample_size(self, entity_key: str) -> int:
        return self._records.get(entity_key, {}).get("total", 0)


reliability_tracker = ReliabilityTracker()
