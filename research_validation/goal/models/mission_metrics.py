"""
Mission Metrics Model
=====================
Quantifies mission complexity, readiness, completeness, and feasibility.
"""

from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass(frozen=True)
class MissionMetrics:
    """Quantitative readiness and complexity metrics for an autonomous mission."""
    total_objectives_count: int
    total_milestones_count: int
    total_tasks_count: int
    total_actions_count: int
    graph_depth: int
    estimated_complexity_score: float  # 0.0 to 1.0
    feasibility_score: float           # 0.0 to 1.0
    readiness_score: float             # 0.0 to 1.0
    custom_metrics: Dict[str, float] = field(default_factory=dict)
