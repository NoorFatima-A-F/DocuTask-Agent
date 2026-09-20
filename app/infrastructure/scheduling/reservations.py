"""Two-Phase Resource Reservation Management."""

from datetime import datetime, timezone, timedelta
from enum import Enum
import secrets
import threading
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from app.infrastructure.executions.workload import ResourceRequirements
from app.infrastructure.workers.models import Worker
from app.infrastructure.workers.registry import WorkerRegistry


class ReservationStatus(str, Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    RELEASED = "RELEASED"
    EXPIRED = "EXPIRED"


class ResourceReservation(BaseModel):
    """Temporary reservation of worker compute resources."""

    reservation_id: str = Field(default_factory=lambda: f"res_{secrets.token_hex(8)}")
    workload_id: str
    worker_id: str
    resources: ResourceRequirements
    status: ReservationStatus = ReservationStatus.PENDING
    ttl_seconds: int = 30
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(seconds=30))


class ResourceReservationManager:
    """Manages two-phase capacity reservations to prevent overcommit."""

    def __init__(self, worker_registry: WorkerRegistry) -> None:
        self.worker_registry = worker_registry
        self._reservations: Dict[str, ResourceReservation] = {}
        self._lock = threading.RLock()

    def create_reservation(
        self,
        workload_id: str,
        worker: Worker,
        resources: ResourceRequirements,
        ttl_seconds: int = 30,
    ) -> Optional[ResourceReservation]:
        """Atomically reserve capacity on worker if available."""
        with self._lock:
            avail = worker.resource_available
            if (
                avail.cpu_cores < resources.cpu_cores
                or avail.memory_gb < resources.memory_gb
                or (resources.gpu_count > 0 and avail.gpu_count < resources.gpu_count)
                or avail.worker_slots < resources.worker_slots
            ):
                return None

            now = datetime.now(timezone.utc)
            res = ResourceReservation(
                workload_id=workload_id,
                worker_id=worker.worker_id,
                resources=resources,
                status=ReservationStatus.PENDING,
                ttl_seconds=ttl_seconds,
                created_at=now,
                expires_at=now + timedelta(seconds=ttl_seconds),
            )
            self._reservations[res.reservation_id] = res

            # Deduct from worker allocated capacity
            worker.resource_allocated.cpu_cores += resources.cpu_cores
            worker.resource_allocated.memory_gb += resources.memory_gb
            worker.resource_allocated.gpu_count += resources.gpu_count
            worker.resource_allocated.worker_slots += resources.worker_slots

            return res

    def activate_reservation(self, reservation_id: str) -> bool:
        """Mark reservation as ACTIVE upon worker assignment ACK."""
        with self._lock:
            res = self._reservations.get(reservation_id)
            if not res or res.status != ReservationStatus.PENDING:
                return False
            res.status = ReservationStatus.ACTIVE
            return True

    def release_reservation(self, reservation_id: str) -> bool:
        """Release reservation and return capacity to worker."""
        with self._lock:
            res = self._reservations.get(reservation_id)
            if not res or res.status in (ReservationStatus.RELEASED, ReservationStatus.EXPIRED):
                return False

            worker = self.worker_registry.get_worker(res.worker_id)
            if worker:
                worker.resource_allocated.cpu_cores = max(
                    0.0, worker.resource_allocated.cpu_cores - res.resources.cpu_cores
                )
                worker.resource_allocated.memory_gb = max(
                    0.0, worker.resource_allocated.memory_gb - res.resources.memory_gb
                )
                worker.resource_allocated.gpu_count = max(
                    0, worker.resource_allocated.gpu_count - res.resources.gpu_count
                )
                worker.resource_allocated.worker_slots = max(
                    0, worker.resource_allocated.worker_slots - res.resources.worker_slots
                )

            res.status = ReservationStatus.RELEASED
            return True

    def clean_expired_reservations(self) -> List[str]:
        """Release any pending reservations that passed their TTL without ACK."""
        with self._lock:
            expired_ids = []
            now = datetime.now(timezone.utc)
            for res_id, res in list(self._reservations.items()):
                if res.status == ReservationStatus.PENDING and now > res.expires_at:
                    self.release_reservation(res_id)
                    res.status = ReservationStatus.EXPIRED
                    expired_ids.append(res_id)
            return expired_ids
