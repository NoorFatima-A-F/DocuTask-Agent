"""
AOIS-HROP Phase 13.7 - Subsystem Health Evaluator
Individual health scoring and status tracking across all 10 platform subsystems.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List
from app.runtime.operations.events.operation_events import SubsystemType


@dataclass
class SubsystemHealthReport:
    subsystem: SubsystemType
    score: float  # 0.0 - 100.0
    status: str   # HEALTHY, DEGRADED, CRITICAL, FAILING
    metrics: Dict[str, float] = field(default_factory=dict)
    active_issues: List[str] = field(default_factory=list)
    evaluated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class SubsystemHealthEvaluator:
    """
    Evaluates individual subsystem health based on latency, error rates, queue depths, and resource saturation.
    """

    def __init__(self):
        self._subsystems_weight = {
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

    def evaluate_subsystem(
        self,
        subsystem: SubsystemType,
        error_rate: float = 0.0,
        latency_p95_ms: float = 250.0,
        saturation_pct: float = 30.0,
        unresponsive_tasks: int = 0,
    ) -> SubsystemHealthReport:
        # Score calculation: base 100 minus penalties
        penalty = (error_rate * 50.0) + (max(0.0, latency_p95_ms - 500.0) / 50.0) + (max(0.0, saturation_pct - 75.0) * 0.8) + (unresponsive_tasks * 15.0)
        score = max(0.0, min(100.0, 100.0 - penalty))

        if score >= 90.0:
            status = "HEALTHY"
        elif score >= 70.0:
            status = "DEGRADED"
        elif score >= 40.0:
            status = "CRITICAL"
        else:
            status = "FAILING"

        issues = []
        if error_rate > 0.05:
            issues.append(f"Elevated error rate: {round(error_rate * 100, 1)}%")
        if latency_p95_ms > 1000.0:
            issues.append(f"High P95 latency: {round(latency_p95_ms, 1)}ms")
        if saturation_pct > 85.0:
            issues.append(f"High resource saturation: {round(saturation_pct, 1)}%")
        if unresponsive_tasks > 0:
            issues.append(f"{unresponsive_tasks} unresponsive tasks detected")

        return SubsystemHealthReport(
            subsystem=subsystem,
            score=round(score, 2),
            status=status,
            metrics={
                "error_rate": error_rate,
                "latency_p95_ms": latency_p95_ms,
                "saturation_pct": saturation_pct,
                "unresponsive_tasks": unresponsive_tasks,
            },
            active_issues=issues,
            evaluated_at=datetime.now(timezone.utc).isoformat(),
        )

    def evaluate_all(self) -> Dict[str, SubsystemHealthReport]:
        return {st.value: self.evaluate_subsystem(st) for st in SubsystemType}
