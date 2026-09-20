"""Persistent, Thread-Safe Worker Registry."""

import json
from pathlib import Path
import threading
from typing import Any, Dict, List, Optional, Set, Union

from app.infrastructure.workers.models import (
    ResourceCapacity,
    Worker,
    WorkerLease,
    WorkerStatus,
    WorkerType,
)
from app.infrastructure.workers.lifecycle import WorkerLifecycleStateMachine
from app.infrastructure.workers.capabilities import WorkerCapabilityRegistry
from app.infrastructure.workers.leases import WorkerLeaseManager
from app.infrastructure.workers.heartbeat import (
    WorkerHeartbeatManager,
    WorkerHeartbeatPayload,
)
from app.infrastructure.workers.drain import WorkerDrainManager
from app.infrastructure.workers.health import WorkerHealthAggregator


class WorkerRegistry:
    """Enterprise persistent registry for distributed execution workers."""

    def __init__(
        self,
        capability_registry: Optional[WorkerCapabilityRegistry] = None,
        lease_manager: Optional[WorkerLeaseManager] = None,
        heartbeat_manager: Optional[WorkerHeartbeatManager] = None,
        drain_manager: Optional[WorkerDrainManager] = None,
        persistence_path: Optional[Union[str, Path]] = None,
    ) -> None:
        self._workers: Dict[str, Worker] = {}
        self.capability_registry = capability_registry or WorkerCapabilityRegistry()
        self.lease_manager = lease_manager or WorkerLeaseManager()
        self.heartbeat_manager = heartbeat_manager or WorkerHeartbeatManager(self.lease_manager)
        self.drain_manager = drain_manager or WorkerDrainManager()
        self._lock = threading.RLock()

        self.persistence_path = Path(persistence_path) if persistence_path else None
        if self.persistence_path and self.persistence_path.exists():
            self._load_from_storage()

    def register_worker(self, worker: Worker, ttl_seconds: int = 60) -> Worker:
        """Register a new worker, establish capabilities, issue lease, and mark AVAILABLE."""
        with self._lock:
            # Advance lifecycle: DISCOVERED -> REGISTERING -> REGISTERED -> AVAILABLE
            if worker.status == WorkerStatus.DISCOVERED:
                WorkerLifecycleStateMachine.transition(worker, WorkerStatus.REGISTERING)
                WorkerLifecycleStateMachine.transition(worker, WorkerStatus.REGISTERED)
                WorkerLifecycleStateMachine.transition(worker, WorkerStatus.AVAILABLE)

            # Issue lease
            lease = self.lease_manager.issue_lease(
                worker_id=worker.worker_id,
                cluster_id=worker.cluster_id,
                runtime_version=worker.version,
                ttl_seconds=ttl_seconds,
            )
            worker.active_lease = lease

            # Index capabilities
            self.capability_registry.register_capabilities(worker.worker_id, worker.capabilities)

            self._workers[worker.worker_id] = worker
            self._save_to_storage()
            return worker

    def get_worker(self, worker_id: str) -> Optional[Worker]:
        with self._lock:
            return self._workers.get(worker_id)

    def list_workers(
        self,
        region_id: Optional[str] = None,
        cluster_id: Optional[str] = None,
        worker_type: Optional[WorkerType] = None,
        status: Optional[WorkerStatus] = None,
        tenant_id: Optional[str] = None,
    ) -> List[Worker]:
        """List registered workers with multi-criteria filtering."""
        with self._lock:
            results = list(self._workers.values())
            if region_id:
                results = [w for w in results if w.region_id == region_id]
            if cluster_id:
                results = [w for w in results if w.cluster_id == cluster_id]
            if worker_type:
                results = [w for w in results if w.worker_type == worker_type]
            if status:
                results = [w for w in results if w.status == status]
            if tenant_id:
                results = [
                    w for w in results
                    if not w.tenant_restrictions or tenant_id in w.tenant_restrictions
                ]
            return results

    def find_eligible_workers(
        self,
        region_id: Optional[str] = None,
        cluster_id: Optional[str] = None,
        worker_type: Optional[WorkerType] = None,
        mandatory_capabilities: Optional[Set[str]] = None,
        min_cpu: float = 0.0,
        min_memory_gb: float = 0.0,
        min_gpu: int = 0,
        tenant_id: Optional[str] = None,
    ) -> List[Worker]:
        """Filter active, healthy, and non-expired workers matching resource and policy constraints."""
        with self._lock:
            candidates: List[Worker] = []
            for worker in self._workers.values():
                # 1. State & Schedulability
                if not WorkerLifecycleStateMachine.is_schedulable(worker.status):
                    continue

                # 2. Lease Validity
                if not self.lease_manager.is_lease_valid(worker.worker_id):
                    continue

                # 3. Region & Cluster
                if region_id and worker.region_id != region_id:
                    continue
                if cluster_id and worker.cluster_id != cluster_id:
                    continue

                # 4. Worker Type
                if worker_type and worker.worker_type != worker_type:
                    continue

                # 5. Tenant Restrictions
                if worker.tenant_restrictions and tenant_id:
                    if tenant_id not in worker.tenant_restrictions:
                        continue

                # 6. Capabilities
                if mandatory_capabilities and not self.capability_registry.satisfies_capabilities(
                    worker.worker_id, mandatory_capabilities
                ):
                    continue

                # 7. Available Resources
                avail = worker.resource_available
                if avail.cpu_cores < min_cpu or avail.memory_gb < min_memory_gb or avail.gpu_count < min_gpu:
                    continue

                # 8. Slot & Concurrency Limits
                if avail.worker_slots <= 0 or len(worker.active_assignments) >= worker.concurrency_limit:
                    continue

                candidates.append(worker)

            return candidates

    def heartbeat(self, payload: WorkerHeartbeatPayload) -> Optional[WorkerLease]:
        """Process worker heartbeat and refresh in-memory state."""
        with self._lock:
            worker = self._workers.get(payload.worker_id)
            if not worker:
                return None

            self.heartbeat_manager.process_heartbeat(payload)
            worker.last_heartbeat = payload.timestamp
            worker.health_status = WorkerHealthAggregator.evaluate_health(payload)

            lease = self.lease_manager.get_lease(payload.worker_id)
            worker.active_lease = lease

            self._save_to_storage()
            return lease

    def transition_worker_state(
        self, worker_id: str, target_state: WorkerStatus, reason: Optional[str] = None
    ) -> Optional[Worker]:
        with self._lock:
            worker = self._workers.get(worker_id)
            if not worker:
                return None
            WorkerLifecycleStateMachine.transition(worker, target_state, reason=reason or "")
            self._save_to_storage()
            return worker

    def drain_worker(self, worker_id: str, reason: str = "Administrative drain") -> Optional[Worker]:
        with self._lock:
            worker = self._workers.get(worker_id)
            if not worker:
                return None
            draining = self.drain_manager.start_drain(worker, reason=reason)
            self._save_to_storage()
            return draining

    def remove_worker(self, worker_id: str) -> bool:
        with self._lock:
            worker = self._workers.get(worker_id)
            if not worker:
                return False
            if worker.status != WorkerStatus.TERMINATED:
                WorkerLifecycleStateMachine.transition(worker, WorkerStatus.TERMINATED)
            self.lease_manager.revoke_lease(worker_id)
            del self._workers[worker_id]
            self._save_to_storage()
            return True

    def delete_worker(self, worker_id: str) -> bool:
        return self.remove_worker(worker_id)

    def _save_to_storage(self) -> None:
        if not self.persistence_path:
            return
        try:
            self.persistence_path.parent.mkdir(parents=True, exist_ok=True)
            data = {w_id: w.model_dump(mode="json") for w_id, w in self._workers.items()}
            with open(self.persistence_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass

    def _load_from_storage(self) -> None:
        if not self.persistence_path or not self.persistence_path.exists():
            return
        try:
            with open(self.persistence_path, "r", encoding="utf-8") as f:
                raw = json.load(f)
                for w_id, w_data in raw.items():
                    worker = Worker.model_validate(w_data)
                    self._workers[w_id] = worker
                    self.capability_registry.register_capabilities(w_id, worker.capabilities)
                    if worker.active_lease:
                        self.lease_manager._leases[w_id] = worker.active_lease
        except Exception:
            pass
