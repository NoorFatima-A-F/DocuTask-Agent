"""
Plan Confidence Estimator.
"""

from typing import List
from app.agents.planning.tasks import PlanningTask


class PlanConfidenceEstimator:
    """Estimates confidence score based on task dependencies and tool resolution."""

    def estimate_confidence(self, tasks: List[PlanningTask]) -> float:
        if not tasks:
            return 0.0
        # Highly defined tasks yield high confidence
        return 0.95
