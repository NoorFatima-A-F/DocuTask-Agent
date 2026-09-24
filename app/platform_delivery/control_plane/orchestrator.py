"""Delivery Orchestration Engine linking Build, Governance, Promotion, Rollout, and SRE verification."""
from datetime import datetime, timezone
from typing import Callable, Optional

from .controller import DeploymentControlPlane, DeploymentRecord
from .state_machine import DeploymentState


class DeliveryOrchestrator:
    """Coordinates the end-to-end execution of a deployment across the platform."""

    def __init__(self, control_plane: DeploymentControlPlane):
        self.control_plane = control_plane

    def advance_deployment(
        self,
        deployment_id: str,
        verify_health_fn: Optional[Callable[[], bool]] = None,
        canary_fn: Optional[Callable[[float], bool]] = None,
    ) -> DeploymentRecord:
        dep = self.control_plane.get_deployment(type("Query", (), {"deployment_id": deployment_id})())
        if not dep:
            raise KeyError(f"Deployment '{deployment_id}' not found")

        # 1. VALIDATING
        if dep.status == DeploymentState.REQUESTED:
            dep.state_machine.transition_to(DeploymentState.VALIDATING, reason="Validating supply chain and compatibility")

        # 2. Check if approval is needed (e.g. prod environment)
        if dep.status == DeploymentState.VALIDATING:
            if dep.environment_id == "prod" and not dep.approved_by:
                dep.state_machine.transition_to(DeploymentState.AWAITING_APPROVAL, reason="Production deployment requires approval")
                return dep
            else:
                dep.state_machine.transition_to(DeploymentState.APPROVED, reason="Auto-approved or pre-approved environment")

        # 3. PREPARING
        if dep.status == DeploymentState.APPROVED:
            dep.started_at = datetime.now(timezone.utc)
            dep.state_machine.transition_to(DeploymentState.PREPARING, reason="Allocating target compute and network resources")

        # 4. DEPLOYING
        if dep.status == DeploymentState.PREPARING:
            dep.state_machine.transition_to(DeploymentState.DEPLOYING, reason=f"Executing {dep.strategy} deployment")

        # 5. CANARY / VERIFYING
        if dep.status == DeploymentState.DEPLOYING:
            if dep.strategy == "CANARY":
                dep.state_machine.transition_to(DeploymentState.CANARY, reason="Canary rollout initiated at step traffic")
                dep.traffic_weight = 0.10
                if canary_fn and not canary_fn(dep.traffic_weight):
                    dep.state_machine.transition_to(DeploymentState.ABORTED, reason="Canary metrics breached SLO safety threshold")
                    return dep
            else:
                dep.state_machine.transition_to(DeploymentState.VERIFYING, reason="Running post-rollout health verifications")
                dep.traffic_weight = 1.0

        # 6. PROMOTING
        if dep.status in {DeploymentState.CANARY, DeploymentState.VERIFYING}:
            if verify_health_fn and not verify_health_fn():
                dep.state_machine.transition_to(DeploymentState.FAILED, reason="Health probes failed during verification")
                return dep
            dep.state_machine.transition_to(DeploymentState.PROMOTING, reason="Health verified; promoting to active traffic")
            dep.traffic_weight = 1.0

        # 7. ACTIVE
        if dep.status == DeploymentState.PROMOTING:
            dep.state_machine.transition_to(DeploymentState.ACTIVE, reason="Deployment active in production")
            dep.completed_at = datetime.now(timezone.utc)
            dep.actual_state = dict(dep.desired_state)

        return dep
