"""Deployment Domain Model."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional
import uuid
from .lifecycle import DeploymentStateEngine, DeploymentStatus


class DeploymentStrategyType(str, Enum):
    """Supported progressive deployment strategies."""
    ROLLING = "ROLLING"
    BLUE_GREEN = "BLUE_GREEN"
    CANARY = "CANARY"
    SHADOW = "SHADOW"


@dataclass
class Deployment:
    """Represents an active or historic deployment execution."""
    release_id: str
    target_environment: str
    strategy: DeploymentStrategyType = DeploymentStrategyType.ROLLING
    replicas: int = 3
    deployment_id: str = field(default_factory=lambda: f"dep-{uuid.uuid4().hex[:10]}")
    state_engine: DeploymentStateEngine = field(default_factory=DeploymentStateEngine)
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None
    rollback_target_id: Optional[str] = None
    traffic_weight: float = 0.0
    error_details: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def status(self) -> DeploymentStatus:
        """Returns the current deployment status from state engine."""
        return self.state_engine.current_status

    def transition_to(
        self,
        target_status: DeploymentStatus,
        reason: Optional[str] = None,
        triggered_by: Optional[str] = None,
    ) -> None:
        """Transitions the deployment through the lifecycle state machine."""
        self.state_engine.transition_to(target_status, reason=reason, triggered_by=triggered_by)
        if target_status in {DeploymentStatus.ACTIVE, DeploymentStatus.FAILED, DeploymentStatus.ROLLED_BACK, DeploymentStatus.DECOMMISSIONED}:
            self.completed_at = datetime.now(timezone.utc)

    def mark_failed(self, error: str, triggered_by: Optional[str] = "system") -> None:
        """Marks deployment as failed and records error description."""
        self.error_details = error
        self.transition_to(DeploymentStatus.FAILED, reason=error, triggered_by=triggered_by)

    def mark_rolled_back(self, target_release_id: str, reason: str = "Rollback executed") -> None:
        """Marks deployment as rolled back to a specified release."""
        self.rollback_target_id = target_release_id
        self.transition_to(DeploymentStatus.ROLLED_BACK, reason=reason, triggered_by="rollback_manager")

    def to_dict(self) -> Dict[str, Any]:
        """Serializes deployment to dictionary."""
        return {
            "deployment_id": self.deployment_id,
            "release_id": self.release_id,
            "target_environment": self.target_environment,
            "strategy": self.strategy.value,
            "replicas": self.replicas,
            "status": self.status.value,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "rollback_target_id": self.rollback_target_id,
            "traffic_weight": self.traffic_weight,
            "error_details": self.error_details,
            "metadata": self.metadata,
            "history": [
                {
                    "from_status": h.from_status.value,
                    "to_status": h.to_status.value,
                    "timestamp": h.timestamp.isoformat(),
                    "reason": h.reason,
                    "triggered_by": h.triggered_by,
                }
                for h in self.state_engine.history
            ],
        }
