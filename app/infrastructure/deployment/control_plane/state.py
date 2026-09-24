"""Deployment State, Lifecycle Enums, and Record Tracking."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import threading


class DeploymentStatus(str, Enum):
    """Lifecycle statuses for a deployment execution."""
    PENDING = "pending"
    VALIDATING = "validating"
    RUNNING = "running"
    PROMOTING = "promoting"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLING_BACK = "rolling_back"
    ROLLED_BACK = "rolled_back"


class DeploymentStrategyType(str, Enum):
    """Supported deployment strategies."""
    ROLLING = "rolling"
    CANARY = "canary"
    BLUE_GREEN = "blue_green"
    SHADOW = "shadow"


@dataclass
class DeploymentRecord:
    """Represents an active or historic deployment execution."""
    deployment_id: str
    release_id: str
    service_name: str
    target_environment: str
    target_version: str
    previous_version: Optional[str] = None
    strategy: DeploymentStrategyType = DeploymentStrategyType.ROLLING
    status: DeploymentStatus = DeploymentStatus.PENDING
    progress_percentage: float = 0.0
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    rollback_reason: Optional[str] = None
    audit_trail: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def transition_to(self, new_status: DeploymentStatus, message: Optional[str] = None) -> None:
        """Record a status transition with timestamp and audit log."""
        self.status = new_status
        self.updated_at = datetime.now(timezone.utc)
        if new_status in (DeploymentStatus.COMPLETED, DeploymentStatus.FAILED, DeploymentStatus.ROLLED_BACK):
            self.completed_at = self.updated_at

        self.audit_trail.append({
            "status": new_status.value,
            "timestamp": self.updated_at.isoformat(),
            "message": message or f"Transitioned to {new_status.value}",
        })


class DeploymentHistoryTracker:
    """Thread-safe storage and query registry for all deployment records."""

    def __init__(self) -> None:
        self._deployments: Dict[str, DeploymentRecord] = {}
        self._service_history: Dict[str, List[str]] = {}  # service_name -> [deployment_id]
        self._lock = threading.RLock()

    def record_deployment(self, record: DeploymentRecord) -> None:
        """Store or update a deployment record."""
        with self._lock:
            self._deployments[record.deployment_id] = record
            hist = self._service_history.setdefault(record.service_name, [])
            if record.deployment_id not in hist:
                hist.append(record.deployment_id)

    def get_deployment(self, deployment_id: str) -> Optional[DeploymentRecord]:
        """Fetch deployment by ID."""
        with self._lock:
            return self._deployments.get(deployment_id)

    def list_deployments(
        self,
        service_name: Optional[str] = None,
        environment: Optional[str] = None,
        status: Optional[DeploymentStatus] = None,
    ) -> List[DeploymentRecord]:
        """Query deployments matching filters."""
        with self._lock:
            res = list(self._deployments.values())

            if service_name:
                res = [d for d in res if d.service_name == service_name]
            if environment:
                res = [d for d in res if d.target_environment == environment]
            if status:
                res = [d for d in res if d.status == status]

            return sorted(res, key=lambda d: d.created_at, reverse=True)

    def get_latest_deployment(self, service_name: str, environment: str) -> Optional[DeploymentRecord]:
        """Retrieve most recent completed deployment for a service in an environment."""
        with self._lock:
            deps = [
                d for d in self._deployments.values()
                if d.service_name == service_name and d.target_environment == environment and d.status == DeploymentStatus.COMPLETED
            ]
            if not deps:
                return None
            return max(deps, key=lambda d: d.created_at)
