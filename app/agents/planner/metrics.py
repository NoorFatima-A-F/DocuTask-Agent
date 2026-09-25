"""
Planner Metrics Collector Subsystem.
Tracks goal decompositions, candidate generation count, reflection critiques, and repair actions.
"""

from pydantic import BaseModel, Field


class PlannerMetricRecord(BaseModel):
    goals_analyzed_count: int = Field(default=0, ge=0)
    candidates_generated_count: int = Field(default=0, ge=0)
    reflections_performed_count: int = Field(default=0, ge=0)
    plans_repaired_count: int = Field(default=0, ge=0)
    plans_completed_count: int = Field(default=0, ge=0)


class PlannerMetricsCollector:
    """Collector tracking cognitive planning events and statistics."""

    def __init__(self):
        self._record = PlannerMetricRecord()

    def record_goal_analyzed(self) -> None:
        self._record.goals_analyzed_count += 1

    def record_candidate_generated(self, count: int = 1) -> None:
        self._record.candidates_generated_count += count

    def record_reflection(self, was_repaired: bool = False) -> None:
        self._record.reflections_performed_count += 1
        if was_repaired:
            self._record.plans_repaired_count += 1

    def record_plan_completed(self) -> None:
        self._record.plans_completed_count += 1

    def get_metrics(self) -> PlannerMetricRecord:
        return self._record
