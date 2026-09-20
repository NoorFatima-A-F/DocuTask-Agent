"""Worker Health Aggregation and Failure Detection."""

from typing import Optional
from app.infrastructure.workers.models import Worker, WorkerStatus
from app.infrastructure.workers.heartbeat import WorkerHeartbeatPayload


class WorkerHealthAggregator:
    """Evaluates composite worker health status from heartbeats and resource pressures."""

    MAX_CPU_WARN_THRESHOLD = 95.0
    MAX_MEM_WARN_THRESHOLD = 95.0
    MAX_QUEUE_PRESSURE_THRESHOLD = 90.0

    @classmethod
    def evaluate_health(cls, payload: Optional[WorkerHeartbeatPayload]) -> str:
        if not payload:
            return "UNKNOWN"

        if payload.cpu_usage_pct >= cls.MAX_CPU_WARN_THRESHOLD:
            return "DEGRADED"

        if payload.memory_usage_pct >= cls.MAX_MEM_WARN_THRESHOLD:
            return "DEGRADED"

        if payload.queue_pressure_pct >= cls.MAX_QUEUE_PRESSURE_THRESHOLD:
            return "DEGRADED"

        if payload.health_status != "HEALTHY":
            return payload.health_status

        return "HEALTHY"
