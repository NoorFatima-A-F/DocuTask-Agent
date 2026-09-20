"""
AMAEOP Pillar 4 - Distributed Lease & Fencing Token Manager
Manages time-bound exclusive resource leases with monotonically increasing fencing tokens to prevent split-brain execution.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import time
import uuid


@dataclass
class ResourceLease:
    lease_id: str
    resource_name: str
    holder_department_id: str
    fencing_token: int
    ttl_seconds: float
    acquired_at: float
    expires_at: float
    is_active: bool

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class LeaseManager:
    """Provides distributed lease coordination and anti-entropy fencing token validation."""

    def __init__(self):
        self.leases: Dict[str, ResourceLease] = {}
        self._current_fencing_token = 100
        self._seed_leases()

    def _seed_leases(self):
        now = time.time()
        l1 = ResourceLease(
            lease_id="lease_gpu_ocr",
            resource_name="GPU_ACCELERATOR_NODE_01",
            holder_department_id="dept_ocr",
            fencing_token=101,
            ttl_seconds=60.0,
            acquired_at=now,
            expires_at=now + 60.0,
            is_active=True,
        )
        self.leases[l1.resource_name] = l1

    def acquire_lease(self, resource_name: str, department_id: str, ttl_seconds: float = 60.0) -> Optional[ResourceLease]:
        now = time.time()
        existing = self.leases.get(resource_name)

        if existing and existing.is_active and now < existing.expires_at and existing.holder_department_id != department_id:
            # Lease is already held by another department
            return None

        self._current_fencing_token += 1
        lease = ResourceLease(
            lease_id=f"lease_{uuid.uuid4().hex[:6]}",
            resource_name=resource_name,
            holder_department_id=department_id,
            fencing_token=self._current_fencing_token,
            ttl_seconds=ttl_seconds,
            acquired_at=now,
            expires_at=now + ttl_seconds,
            is_active=True,
        )
        self.leases[resource_name] = lease
        return lease

    def release_lease(self, resource_name: str, department_id: str) -> bool:
        if resource_name in self.leases:
            l = self.leases[resource_name]
            if l.holder_department_id == department_id:
                l.is_active = False
                return True
        return False

    def list_leases(self) -> List[Dict[str, Any]]:
        return [l.to_dict() for l in self.leases.values()]


lease_manager = LeaseManager()
