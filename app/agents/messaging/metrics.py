"""
Messaging Metrics Collector.
"""

from pydantic import BaseModel, Field


class MessagingMetricRecord(BaseModel):
    published_events: int = Field(default=0, ge=0)
    dispatched_commands: int = Field(default=0, ge=0)
    executed_queries: int = Field(default=0, ge=0)
    dead_letter_count: int = Field(default=0, ge=0)


class MessagingMetricsCollector:
    """Collector tracking messaging metrics."""

    def __init__(self):
        self._record = MessagingMetricRecord()

    def record_event(self) -> None:
        self._record.published_events += 1

    def record_command(self) -> None:
        self._record.dispatched_commands += 1

    def record_query(self) -> None:
        self._record.executed_queries += 1

    def record_dlq(self) -> None:
        self._record.dead_letter_count += 1

    def get_metrics(self) -> MessagingMetricRecord:
        return self._record
