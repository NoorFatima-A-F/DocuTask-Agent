"""
Execution Metrics Collector.
Collects task latency, execution latency, throughput, worker utilization, retries, and failed nodes.
"""

from pydantic import BaseModel, Field


class ExecutionMetricRecord(BaseModel):
    executions_started_count: int = Field(default=0, ge=0)
    executions_completed_count: int = Field(default=0, ge=0)
    executions_failed_count: int = Field(default=0, ge=0)
    total_nodes_executed: int = Field(default=0, ge=0)
    total_retries_count: int = Field(default=0, ge=0)
    total_checkpoints_created: int = Field(default=0, ge=0)


class ExecutionMetricsCollector:
    """Collector recording runtime execution metrics."""

    def __init__(self):
        self._record = ExecutionMetricRecord()

    def record_execution_started(self) -> None:
        self._record.executions_started_count += 1

    def record_execution_completed(self, nodes_count: int) -> None:
        self._record.executions_completed_count += 1
        self._record.total_nodes_executed += nodes_count

    def record_execution_failed(self) -> None:
        self._record.executions_failed_count += 1

    def record_retry(self) -> None:
        self._record.total_retries_count += 1

    def record_checkpoint(self) -> None:
        self._record.total_checkpoints_created += 1

    def get_metrics(self) -> ExecutionMetricRecord:
        return self._record
