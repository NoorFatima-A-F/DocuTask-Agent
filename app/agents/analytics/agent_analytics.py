"""
Enterprise Multi-Agent Intelligence Platform (EMAIP) - Agent Analytics.
Aggregates cognitive metrics, recovery rates, planning accuracy, reflection counts,
and resource telemetry across the autonomous agent fleet.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List
import logging

logger = logging.getLogger(__name__)


@dataclass
class FleetAnalyticsSummary:
    """Consolidated telemetry across all agent executions."""
    total_agents_registered: int = 0
    total_goals_created: int = 0
    total_tasks_completed: int = 0
    total_tasks_failed: int = 0
    recovery_rate: float = 1.0
    planning_accuracy: float = 1.0
    total_reflections_performed: int = 0
    total_cost_usd: float = 0.0
    average_latency_ms: float = 0.0
    average_confidence_score: float = 1.0
    memory_hits: int = 0
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_agents_registered": self.total_agents_registered,
            "total_goals_created": self.total_goals_created,
            "total_tasks_completed": self.total_tasks_completed,
            "total_tasks_failed": self.total_tasks_failed,
            "recovery_rate": self.recovery_rate,
            "planning_accuracy": self.planning_accuracy,
            "total_reflections_performed": self.total_reflections_performed,
            "total_cost_usd": self.total_cost_usd,
            "average_latency_ms": self.average_latency_ms,
            "average_confidence_score": self.average_confidence_score,
            "memory_hits": self.memory_hits,
            "timestamp": self.timestamp.isoformat(),
        }


class AgentAnalytics:
    """
    Centralized analytics collector for agent operations and cognitive health.
    """

    def __init__(self):
        self._completed_tasks = 0
        self._failed_tasks = 0
        self._recovered_tasks = 0
        self._reflections = 0
        self._goals = 0
        self._total_cost = 0.0
        self._latencies: List[float] = []
        self._confidences: List[float] = []
        self._memory_hits = 0

    def record_task_completion(self, latency_ms: float, cost_usd: float, confidence: float) -> None:
        self._completed_tasks += 1
        self._latencies.append(latency_ms)
        self._total_cost += cost_usd
        self._confidences.append(confidence)

    def record_task_failure(self, recovered: bool = False) -> None:
        self._failed_tasks += 1
        if recovered:
            self._recovered_tasks += 1

    def record_reflection(self) -> None:
        self._reflections += 1

    def record_goal(self) -> None:
        self._goals += 1

    def record_memory_hit(self) -> None:
        self._memory_hits += 1

    def get_summary(self, registered_agents_count: int = 0) -> FleetAnalyticsSummary:
        """Returns consolidated analytics snapshot."""
        total_failures = self._failed_tasks
        recovery_rate = (self._recovered_tasks / total_failures) if total_failures > 0 else 1.0
        total_tasks = self._completed_tasks + self._failed_tasks
        planning_accuracy = (self._completed_tasks / total_tasks) if total_tasks > 0 else 1.0

        avg_lat = (sum(self._latencies) / len(self._latencies)) if self._latencies else 0.0
        avg_conf = (sum(self._confidences) / len(self._confidences)) if self._confidences else 1.0

        return FleetAnalyticsSummary(
            total_agents_registered=registered_agents_count,
            total_goals_created=self._goals,
            total_tasks_completed=self._completed_tasks,
            total_tasks_failed=self._failed_tasks,
            recovery_rate=round(recovery_rate, 3),
            planning_accuracy=round(planning_accuracy, 3),
            total_reflections_performed=self._reflections,
            total_cost_usd=round(self._total_cost, 4),
            average_latency_ms=round(avg_lat, 2),
            average_confidence_score=round(avg_conf, 3),
            memory_hits=self._memory_hits,
        )
