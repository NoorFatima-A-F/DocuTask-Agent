"""
Decision Metrics Collector Subsystem.
"""

from pydantic import BaseModel, Field


class DecisionMetricRecord(BaseModel):
    evaluations_count: int = Field(default=0, ge=0)
    approved_count: int = Field(default=0, ge=0)
    rejected_count: int = Field(default=0, ge=0)


class DecisionMetricsCollector:
    def __init__(self):
        self._record = DecisionMetricRecord()

    def record_evaluation(self, is_approved: bool) -> None:
        self._record.evaluations_count += 1
        if is_approved:
            self._record.approved_count += 1
        else:
            self._record.rejected_count += 1

    def get_metrics(self) -> DecisionMetricRecord:
        return self._record
