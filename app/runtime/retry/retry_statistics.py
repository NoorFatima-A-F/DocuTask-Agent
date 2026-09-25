"""
Quantitative Retry Optimization - Retry Statistics
Tracks empirical recovery rates, delay distributions, and cumulative costs.
"""

from typing import Dict, Any


class RetryStatistics:
    """Maintains statistical metrics for retry actions and recovery outcomes."""

    def __init__(self):
        self.total_evaluations = 0
        self.retries_attempted = 0
        self.retries_recovered = 0
        self.escalations_triggered = 0

    def record(self, decision: str, recovered: bool = False) -> None:
        self.total_evaluations += 1
        if decision == "RETRY":
            self.retries_attempted += 1
            if recovered:
                self.retries_recovered += 1
        elif decision == "ESCALATE":
            self.escalations_triggered += 1

    def get_summary(self) -> Dict[str, Any]:
        rec_rate = (self.retries_recovered / self.retries_attempted) if self.retries_attempted > 0 else 0.0
        return {
            "total_evaluations": self.total_evaluations,
            "retries_attempted": self.retries_attempted,
            "retries_recovered": self.retries_recovered,
            "empirical_recovery_rate": round(rec_rate, 4),
            "escalations_triggered": self.escalations_triggered,
        }


retry_statistics = RetryStatistics()
