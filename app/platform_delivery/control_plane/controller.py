"""Authoritative Deployment Control Plane for Platform Delivery Operating System."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from .commands import (
    ApproveDeploymentCommand,
    QuarantineArtifactCommand,
    RequestDeploymentCommand,
    RollbackDeploymentCommand,
)
from .queries import GetDeploymentQuery, ListDeploymentsQuery
from .state_machine import DeploymentState, DeploymentStateMachine


@dataclass
class DeploymentRecord:
    """Authoritative Deployment Entity Model (Req 7)."""
    deployment_id: str
    release_id: str
    artifact_id: str
    artifact_digest: str
    application: str
    component: str
    version: str
    environment_id: str
    region_id: str
    cluster_ids: List[str]
    strategy: str
    requested_by: str
    approved_by: Optional[str] = None
    state_machine: DeploymentStateMachine = field(default_factory=DeploymentStateMachine)
    desired_state: Dict[str, Any] = field(default_factory=dict)
    actual_state: Dict[str, Any] = field(default_factory=dict)
    governance_decision_id: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    rollback_reference: Optional[str] = None
    trace_id: str = field(default_factory=lambda: f"trace-{uuid.uuid4().hex[:12]}")
    traffic_weight: float = 0.0
    idempotency_key: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def status(self) -> DeploymentState:
        return self.state_machine.current_state

    def to_dict(self) -> Dict[str, Any]:
        return {
            "deployment_id": self.deployment_id,
            "release_id": self.release_id,
            "artifact_id": self.artifact_id,
            "artifact_digest": self.artifact_digest,
            "application": self.application,
            "component": self.component,
            "version": self.version,
            "environment_id": self.environment_id,
            "region_id": self.region_id,
            "cluster_ids": self.cluster_ids,
            "strategy": self.strategy,
            "requested_by": self.requested_by,
            "approved_by": self.approved_by,
            "status": self.status.value,
            "governance_decision_id": self.governance_decision_id,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "rollback_reference": self.rollback_reference,
            "trace_id": self.trace_id,
            "traffic_weight": self.traffic_weight,
            "idempotency_key": self.idempotency_key,
            "metadata": self.metadata,
            "transition_history": [
                {
                    "from": t.from_state,
                    "to": t.to_state,
                    "timestamp": t.timestamp.isoformat(),
                    "reason": t.reason,
                    "actor": t.actor,
                }
                for t in self.state_machine.history
            ],
        }


class DeploymentControlPlane:
    """The authoritative mechanism through which all deployments are requested, governed, and operated."""

    def __init__(self):
        self._deployments: Dict[str, DeploymentRecord] = {}
        self._idempotency_index: Dict[str, str] = {}  # idempotency_key -> deployment_id
        self._quarantined_digests: Dict[str, str] = {}  # digest -> reason

    def request_deployment(self, cmd: RequestDeploymentCommand) -> DeploymentRecord:
        """Intake new deployment with idempotency and quarantine pre-checks."""
        # 1. Idempotency check
        if cmd.idempotency_key and cmd.idempotency_key in self._idempotency_index:
            existing_id = self._idempotency_index[cmd.idempotency_key]
            return self._deployments[existing_id]

        dep_id = f"dep-{uuid.uuid4().hex[:10]}"
        artifact_digest = cmd.metadata.get("artifact_digest", f"sha256:{uuid.uuid4().hex}")
        artifact_id = cmd.metadata.get("artifact_id", f"art-{cmd.component}-{cmd.version}")

        # 2. Check quarantine
        if artifact_digest in self._quarantined_digests:
            raise PermissionError(
                f"Deployment Blocked: Artifact {artifact_digest} is QUARANTINED: {self._quarantined_digests[artifact_digest]}"
            )

        record = DeploymentRecord(
            deployment_id=dep_id,
            release_id=cmd.release_id,
            artifact_id=artifact_id,
            artifact_digest=artifact_digest,
            application=cmd.application,
            component=cmd.component,
            version=cmd.version,
            environment_id=cmd.environment_id.lower(),
            region_id=cmd.region_id,
            cluster_ids=cmd.cluster_ids,
            strategy=cmd.strategy.upper(),
            requested_by=cmd.requested_by,
            desired_state={"version": cmd.version, "replicas": cmd.metadata.get("replicas", 3)},
            idempotency_key=cmd.idempotency_key,
            metadata=cmd.metadata,
        )

        self._deployments[dep_id] = record
        if cmd.idempotency_key:
            self._idempotency_index[cmd.idempotency_key] = dep_id

        return record

    def get_deployment(self, query: GetDeploymentQuery) -> Optional[DeploymentRecord]:
        return self._deployments.get(query.deployment_id)

    def list_deployments(self, query: Optional[ListDeploymentsQuery] = None) -> List[DeploymentRecord]:
        results = list(self._deployments.values())
        if query:
            if query.environment_id:
                results = [d for d in results if d.environment_id == query.environment_id.lower()]
            if query.status:
                results = [d for d in results if d.status.value == query.status.upper()]
            if query.application:
                results = [d for d in results if d.application == query.application]
            results = results[:query.limit]
        return sorted(results, key=lambda d: d.created_at, reverse=True)

    def approve_deployment(self, cmd: ApproveDeploymentCommand) -> DeploymentRecord:
        dep = self._deployments.get(cmd.deployment_id)
        if not dep:
            raise KeyError(f"Deployment '{cmd.deployment_id}' not found")

        if dep.status == DeploymentState.AWAITING_APPROVAL:
            dep.approved_by = f"{cmd.approved_by} ({cmd.role})"
            dep.state_machine.transition_to(
                DeploymentState.APPROVED,
                reason=f"Approved by {cmd.approved_by}: {cmd.comments}",
                actor=cmd.approved_by,
            )
        elif dep.status != DeploymentState.APPROVED:
            raise ValueError(f"Cannot approve deployment in status '{dep.status.value}'")
        return dep

    def quarantine_artifact(self, cmd: QuarantineArtifactCommand) -> None:
        self._quarantined_digests[cmd.artifact_digest] = cmd.reason
        # Quarantine any in-flight deployments using this artifact
        for dep in self._deployments.values():
            if dep.artifact_digest == cmd.artifact_digest and dep.status not in {
                DeploymentState.FAILED,
                DeploymentState.ROLLED_BACK,
                DeploymentState.ABORTED,
                DeploymentState.QUARANTINED,
            }:
                dep.state_machine.transition_to(
                    DeploymentState.QUARANTINED,
                    reason=f"Artifact quarantined: {cmd.reason}",
                    actor=cmd.reported_by,
                )

    def is_artifact_quarantined(self, digest: str) -> bool:
        return digest in self._quarantined_digests
