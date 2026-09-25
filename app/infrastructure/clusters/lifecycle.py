"""Cluster Lifecycle State Machine and Transition Engine."""

from typing import Dict, Set, Union
from ..core.exceptions import InvalidStateTransitionError
from .models import Cluster, ClusterStatus

InvalidClusterStateTransitionError = InvalidStateTransitionError


class ClusterLifecycleStateMachine:
    """Enforces the 12-state governed cluster lifecycle transitions."""

    ALLOWED_TRANSITIONS: Dict[ClusterStatus, Set[ClusterStatus]] = {
        ClusterStatus.DISCOVERED: {ClusterStatus.REGISTERING, ClusterStatus.REMOVED},
        ClusterStatus.REGISTERING: {ClusterStatus.REGISTERED, ClusterStatus.OFFLINE, ClusterStatus.REMOVED},
        ClusterStatus.REGISTERED: {ClusterStatus.VALIDATING, ClusterStatus.SUSPENDED, ClusterStatus.OFFLINE, ClusterStatus.REMOVED},
        ClusterStatus.VALIDATING: {ClusterStatus.READY, ClusterStatus.SUSPENDED, ClusterStatus.OFFLINE, ClusterStatus.REMOVED},
        ClusterStatus.READY: {ClusterStatus.ACTIVE, ClusterStatus.MAINTENANCE, ClusterStatus.SUSPENDED, ClusterStatus.OFFLINE, ClusterStatus.REMOVED},
        ClusterStatus.ACTIVE: {ClusterStatus.DEGRADED, ClusterStatus.DRAINING, ClusterStatus.MAINTENANCE, ClusterStatus.SUSPENDED, ClusterStatus.OFFLINE},
        ClusterStatus.DEGRADED: {ClusterStatus.ACTIVE, ClusterStatus.DRAINING, ClusterStatus.MAINTENANCE, ClusterStatus.SUSPENDED, ClusterStatus.OFFLINE},
        ClusterStatus.DRAINING: {ClusterStatus.MAINTENANCE, ClusterStatus.SUSPENDED, ClusterStatus.OFFLINE, ClusterStatus.REMOVED},
        ClusterStatus.MAINTENANCE: {ClusterStatus.VALIDATING, ClusterStatus.READY, ClusterStatus.ACTIVE, ClusterStatus.OFFLINE, ClusterStatus.REMOVED},
        ClusterStatus.SUSPENDED: {ClusterStatus.VALIDATING, ClusterStatus.MAINTENANCE, ClusterStatus.OFFLINE, ClusterStatus.REMOVED},
        ClusterStatus.OFFLINE: {ClusterStatus.REGISTERING, ClusterStatus.VALIDATING, ClusterStatus.REMOVED},
        ClusterStatus.REMOVED: set(),
    }

    ROUTABLE_STATES: Set[ClusterStatus] = {
        ClusterStatus.READY,
        ClusterStatus.ACTIVE,
    }

    @classmethod
    def can_transition(cls, from_status: ClusterStatus, to_status: ClusterStatus) -> bool:
        return to_status in cls.ALLOWED_TRANSITIONS.get(from_status, set())

    @classmethod
    def is_routable(cls, status: ClusterStatus) -> bool:
        return status in cls.ROUTABLE_STATES

    @classmethod
    def transition(
        cls,
        target: Union[Cluster, ClusterStatus],
        target_status: ClusterStatus,
        reason: str = "",
    ) -> ClusterStatus:
        if isinstance(target, ClusterStatus):
            from_status = target
            if not cls.can_transition(from_status, target_status):
                raise InvalidClusterStateTransitionError(
                    f"Invalid cluster lifecycle transition from {from_status.value} to {target_status.value}."
                )
            return target_status

        cluster = target
        if not cls.can_transition(cluster.status, target_status):
            raise InvalidClusterStateTransitionError(
                f"Invalid cluster lifecycle transition for '{cluster.cluster_id}' from {cluster.status.value} to {target_status.value}."
            )

        # Prerequisite validations
        if target_status == ClusterStatus.ACTIVE and cluster.identity and cluster.identity.trust_status != "TRUSTED":
            raise InvalidClusterStateTransitionError(
                f"Cannot activate cluster '{cluster.cluster_id}': Workload trust status is '{cluster.identity.trust_status}'."
            )

        if target_status == ClusterStatus.DRAINING:
            cluster.maintenance_reason = reason or "Cluster entering draining state"

        if target_status == ClusterStatus.SUSPENDED:
            cluster.quarantine_reason = reason or "Cluster quarantined by policy"

        cluster.status = target_status
        return target_status
