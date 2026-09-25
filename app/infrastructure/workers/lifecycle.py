"""Worker Lifecycle State Machine and Transition Engine."""

from typing import Dict, Set, Union
from app.infrastructure.core.exceptions import InvalidStateTransitionError
from app.infrastructure.workers.models import Worker, WorkerStatus

InvalidWorkerStateTransitionError = InvalidStateTransitionError


class WorkerLifecycleStateMachine:
    """Enforces the 11-state governed worker lifecycle transitions."""

    ALLOWED_TRANSITIONS: Dict[WorkerStatus, Set[WorkerStatus]] = {
        WorkerStatus.DISCOVERED: {WorkerStatus.REGISTERING, WorkerStatus.TERMINATED},
        WorkerStatus.REGISTERING: {WorkerStatus.REGISTERED, WorkerStatus.UNAVAILABLE, WorkerStatus.TERMINATED},
        WorkerStatus.REGISTERED: {WorkerStatus.AVAILABLE, WorkerStatus.UNAVAILABLE, WorkerStatus.TERMINATED},
        WorkerStatus.AVAILABLE: {
            WorkerStatus.RESERVED,
            WorkerStatus.ASSIGNED,
            WorkerStatus.DRAINING,
            WorkerStatus.UNAVAILABLE,
            WorkerStatus.TERMINATED,
        },
        WorkerStatus.RESERVED: {
            WorkerStatus.ASSIGNED,
            WorkerStatus.AVAILABLE,
            WorkerStatus.DRAINING,
            WorkerStatus.UNAVAILABLE,
            WorkerStatus.TERMINATED,
        },
        WorkerStatus.ASSIGNED: {
            WorkerStatus.RUNNING,
            WorkerStatus.AVAILABLE,
            WorkerStatus.DRAINING,
            WorkerStatus.UNAVAILABLE,
            WorkerStatus.TERMINATED,
        },
        WorkerStatus.RUNNING: {
            WorkerStatus.AVAILABLE,
            WorkerStatus.RESERVED,
            WorkerStatus.ASSIGNED,
            WorkerStatus.DRAINING,
            WorkerStatus.UNAVAILABLE,
            WorkerStatus.RECOVERING,
            WorkerStatus.TERMINATED,
        },
        WorkerStatus.DRAINING: {
            WorkerStatus.UNAVAILABLE,
            WorkerStatus.TERMINATED,
            WorkerStatus.AVAILABLE,
        },
        WorkerStatus.UNAVAILABLE: {
            WorkerStatus.RECOVERING,
            WorkerStatus.REGISTERING,
            WorkerStatus.TERMINATED,
        },
        WorkerStatus.RECOVERING: {
            WorkerStatus.REGISTERED,
            WorkerStatus.AVAILABLE,
            WorkerStatus.UNAVAILABLE,
            WorkerStatus.TERMINATED,
        },
        WorkerStatus.TERMINATED: set(),
    }

    SCHEDULABLE_STATES: Set[WorkerStatus] = {
        WorkerStatus.AVAILABLE,
        WorkerStatus.RESERVED,
        WorkerStatus.RUNNING,
    }

    @classmethod
    def can_transition(cls, from_status: WorkerStatus, to_status: WorkerStatus) -> bool:
        return to_status in cls.ALLOWED_TRANSITIONS.get(from_status, set())

    @classmethod
    def is_schedulable(cls, status: WorkerStatus) -> bool:
        return status in cls.SCHEDULABLE_STATES

    @classmethod
    def transition(
        cls,
        target: Union[Worker, WorkerStatus],
        target_status: WorkerStatus,
        reason: str = "",
    ) -> WorkerStatus:
        if isinstance(target, WorkerStatus):
            from_status = target
            if not cls.can_transition(from_status, target_status):
                raise InvalidWorkerStateTransitionError(
                    f"Invalid worker lifecycle transition from {from_status.value} to {target_status.value}."
                )
            return target_status

        worker = target
        if not cls.can_transition(worker.status, target_status):
            raise InvalidWorkerStateTransitionError(
                f"Invalid worker lifecycle transition for '{worker.worker_id}' from {worker.status.value} to {target_status.value}."
            )

        if target_status == WorkerStatus.DRAINING:
            worker.drain_reason = reason or "Worker entering draining state"

        if target_status == WorkerStatus.UNAVAILABLE:
            worker.quarantine_reason = reason or "Worker marked unavailable"

        worker.status = target_status
        return target_status
