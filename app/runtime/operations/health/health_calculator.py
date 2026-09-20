"""
AOIS-HROP Phase 13.7 - Health Score Calculator
Calculates weighted composite health index (0-100) across all subsystems with penalty scalarization.
"""

from typing import Dict
from app.runtime.operations.health.subsystem_health import SubsystemHealthReport
from app.runtime.operations.events.operation_events import SubsystemType


class HealthScoreCalculator:
    """
    Computes overall platform composite health score from constituent subsystem reports.
    """

    DEFAULT_WEIGHTS: Dict[SubsystemType, float] = {
        SubsystemType.PLANNER: 0.15,
        SubsystemType.WORKERS: 0.15,
        SubsystemType.MEMORY: 0.10,
        SubsystemType.OPTIMIZATION: 0.10,
        SubsystemType.REPLAY: 0.08,
        SubsystemType.LEARNING: 0.08,
        SubsystemType.TRUTH: 0.12,
        SubsystemType.TELEMETRY: 0.07,
        SubsystemType.API: 0.08,
        SubsystemType.DATABASE: 0.07,
    }

    def __init__(self, weights: Dict[SubsystemType, float] = None):
        self.weights = weights or self.DEFAULT_WEIGHTS

    def compute_composite_health(self, reports: Dict[str, SubsystemHealthReport]) -> float:
        total_weight = 0.0
        weighted_sum = 0.0

        for st, weight in self.weights.items():
            report = reports.get(st.value)
            if report:
                weighted_sum += report.score * weight
                total_weight += weight

        if total_weight == 0.0:
            return 100.0

        composite = weighted_sum / total_weight
        return round(max(0.0, min(100.0, composite)), 2)

    def determine_system_status(self, composite_score: float) -> str:
        if composite_score >= 92.0:
            return "OPERATIONAL_EXCELLENT"
        elif composite_score >= 80.0:
            return "OPERATIONAL_STABLE"
        elif composite_score >= 60.0:
            return "DEGRADED_PERFORMANCE"
        elif composite_score >= 35.0:
            return "SEVERELY_IMPAIRED"
        return "OUTAGE_CRITICAL"
