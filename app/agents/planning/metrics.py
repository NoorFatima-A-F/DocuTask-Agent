"""
Planning Metrics Collector Subsystem.
Tracks generated plans, validation results, and DAG complexity metrics.
"""

from pydantic import BaseModel, Field


class PlanningMetricRecord(BaseModel):
    plans_generated_count: int = Field(default=0, ge=0)
    plans_validated_count: int = Field(default=0, ge=0)
    validation_failures_count: int = Field(default=0, ge=0)
    total_nodes_planned: int = Field(default=0, ge=0)


class PlanningMetricsCollector:
    """Collector recording metrics for plan creation and graph validations."""

    def __init__(self):
        self._record = PlanningMetricRecord()

    def record_plan_generated(self, node_count: int = 1) -> None:
        self._record.plans_generated_count += 1
        self._record.total_nodes_planned += node_count

    def record_validation(self, is_valid: bool) -> None:
        self._record.plans_validated_count += 1
        if not is_valid:
            self._record.validation_failures_count += 1

    def get_metrics(self) -> PlanningMetricRecord:
        return self._record
