"""
Memory Metrics Collector Subsystem.
Tracks memory storage operations, hit/miss counters, and context token allocations.
"""

from pydantic import BaseModel, Field


class MemoryMetricRecord(BaseModel):
    """Execution metrics for memory operations."""

    total_stores: int = Field(default=0, ge=0)
    total_retrievals: int = Field(default=0, ge=0)
    hit_count: int = Field(default=0, ge=0)
    miss_count: int = Field(default=0, ge=0)


class MemoryMetricsCollector:
    """Collector tracking memory subsystem metrics."""

    def __init__(self):
        self._record = MemoryMetricRecord()

    def record_store(self) -> None:
        self._record.total_stores += 1

    def record_hit(self) -> None:
        self._record.total_retrievals += 1
        self._record.hit_count += 1

    def record_miss(self) -> None:
        self._record.total_retrievals += 1
        self._record.miss_count += 1

    def get_metrics(self) -> MemoryMetricRecord:
        return self._record
