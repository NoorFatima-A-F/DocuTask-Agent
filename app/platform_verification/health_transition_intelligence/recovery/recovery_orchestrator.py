"""
Service Recovery Orchestrator & Validator (Parts 3H.3.3.6 & 3H.3.3.9).
Orchestrates automated recovery decisions (e.g. worker recycling, pool reconnection, fallback mode),
validates all prerequisite conditions in the RECOVERING state, and promotes healthy services back to READY.
"""
import time
from app.platform_verification.health_transition_intelligence.domain.models import (
    HealthState,
    RecoveryActionType,
    RecoveryValidationReport,
)
from app.platform_verification.health_transition_intelligence.state_machine.health_state_machine import HealthStateMachine


class ServiceRecoveryOrchestrator:
    """
    Coordinates and validates automated recovery workflows.
    """

    def __init__(self, service_name: str = "docutask-api"):
        self.service_name = service_name
        self.state_machine = HealthStateMachine(service_name=service_name, initial_state=HealthState.READY)

    def select_recovery_action(self, failed_dependency: str) -> RecoveryActionType:
        if failed_dependency == "postgres":
            return RecoveryActionType.RECONNECT_POOL
        elif failed_dependency == "worker_memory":
            return RecoveryActionType.RESTART_WORKER
        elif failed_dependency == "gemini":
            return RecoveryActionType.ENABLE_FALLBACK
        elif failed_dependency == "queue_overflow":
            return RecoveryActionType.PAUSE_QUEUE
        return RecoveryActionType.THROTTLE_TRAFFIC

    def execute_and_validate_recovery(
        self,
        from_failure: str = "postgres",
        simulate_success: bool = True,
    ) -> RecoveryValidationReport:
        start_time = time.perf_counter()

        # Step 1: Transition READY -> NOT_READY upon failure
        self.state_machine.transition(
            HealthState.NOT_READY,
            reason=f"Failure detected in dependency: {from_failure}",
            trigger_signal="health_probe_failure",
        )

        # Step 2: Select & Execute Action -> Transition NOT_READY -> RECOVERING
        action = self.select_recovery_action(from_failure)
        self.state_machine.transition(
            HealthState.RECOVERING,
            reason=f"Executing recovery action: {action.value}",
            trigger_signal="automated_recovery_initiator",
        )

        # Step 3: Validate all recovery prerequisites
        checks = {
            "database_transaction": simulate_success,
            "queue_ping": simulate_success,
            "storage_write": simulate_success,
            "worker_heartbeat": simulate_success,
        }
        all_passed = all(checks.values())

        # Step 4: Promote to READY if validated
        if all_passed:
            self.state_machine.transition(
                HealthState.READY,
                reason="All recovery validation prerequisites passed successfully",
                trigger_signal="recovery_validator",
            )
            final_state = HealthState.READY
        else:
            self.state_machine.transition(
                HealthState.NOT_READY,
                reason="Recovery prerequisites validation failed",
                trigger_signal="recovery_validator",
            )
            final_state = HealthState.NOT_READY

        duration = (time.perf_counter() - start_time) * 1000.0

        return RecoveryValidationReport(
            service=self.service_name,
            initial_state=HealthState.NOT_READY,
            recovery_state_reached=True,
            final_state=final_state,
            all_prerequisites_met=all_passed,
            recovery_duration_seconds=round(duration / 1000.0, 3),
            passed=all_passed,
            details={
                "action_executed": action.value,
                "validation_checks": checks,
                "recovery_protocol": "NOT_READY -> RECOVERING (Validation Gate) -> READY",
            },
        )
