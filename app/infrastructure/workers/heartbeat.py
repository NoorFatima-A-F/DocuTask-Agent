"""Worker Heartbeat Processing and Telemetry Tracking."""

from datetime import datetime, timezone
import threading
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from app.infrastructure.workers.models import WorkerStatus
from app.infrastructure.workers.leases import WorkerLeaseManager


class WorkerHeartbeatPayload(BaseModel):
    """Telemetry payload periodically sent by active workers."""

    worker_id: str
    status: WorkerStatus = WorkerStatus.AVAILABLE
    cpu_usage_pct: float = 0.0
    memory_usage_pct: float = 0.0
    gpu_usage_pct: float = 0.0
    active_tasks_count: int = 0
    available_slots: int = 10
    queue_pressure_pct: float = 0.0
    current_version: str = "3.1.0"
    health_status: str = "HEALTHY"
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class WorkerHeartbeatManager:
    """Processes heartbeats, updates metrics, and detects missed heartbeat leases."""

    def __init__(self, lease_manager: Optional[WorkerLeaseManager] = None) -> None:
        self.lease_manager = lease_manager or WorkerLeaseManager()
        self._telemetry: Dict[str, WorkerHeartbeatPayload] = {}
        self._lock = threading.RLock()

    def process_heartbeat(self, payload: WorkerHeartbeatPayload) -> bool:
        """Process heartbeat from worker and renew its active lease."""
        with self._lock:
            self._telemetry[payload.worker_id] = payload
            renewed = self.lease_manager.renew_lease(payload.worker_id)
            return renewed is not None

    def get_latest_telemetry(self, worker_id: str) -> Optional[WorkerHeartbeatPayload]:
        with self._lock:
            return self._telemetry.get(worker_id)

    def check_worker_liveness(self, worker_id: str) -> bool:
        """Verify if worker lease is valid and active."""
        return self.lease_manager.is_lease_valid(worker_id)

    def scan_dead_workers(self) -> List[str]:
        """Return list of workers whose heartbeats have timed out."""
        return self.lease_manager.find_expired_leases()
