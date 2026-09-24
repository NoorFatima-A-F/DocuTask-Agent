"""CQRS Command Models for Platform Delivery Control Plane."""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class RequestDeploymentCommand:
    """Command to initiate a new deployment."""
    release_id: str
    environment_id: str
    strategy: str = "ROLLING"
    application: str = "docutask-agent"
    component: str = "core-runtime"
    version: str = "1.0.0"
    region_id: str = "us-east-1"
    cluster_ids: List[str] = field(default_factory=lambda: ["cluster-primary-01"])
    requested_by: str = "developer"
    metadata: Dict[str, Any] = field(default_factory=dict)
    idempotency_key: Optional[str] = None


@dataclass
class ApproveDeploymentCommand:
    """Command to grant governance approval to an awaiting deployment."""
    deployment_id: str
    approved_by: str
    role: str
    comments: str = "Approved for rollout"
    approval_token: Optional[str] = None


@dataclass
class RollbackDeploymentCommand:
    """Command to execute a controlled rollback."""
    deployment_id: str
    target_release_id: Optional[str] = None
    reason: str = "Automated SLO or operator rollback trigger"
    initiated_by: str = "sre_controller"


@dataclass
class QuarantineArtifactCommand:
    """Command to quarantine an artifact due to security or integrity violation."""
    artifact_digest: str
    reason: str
    reported_by: str = "security_scanner"
