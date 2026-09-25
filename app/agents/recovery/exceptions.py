"""
Enterprise Recovery Exception Hierarchy.
Provides domain exceptions for failure classification, strategy selection,
checkpoint restoration, state reconciliation, rollback coordination, and circuit breaker trip.
"""

from app.agents.exceptions import AgentException


class RecoveryException(AgentException):
    """Base exception for all recovery and self-healing subsystem errors."""
    pass


class FailureClassificationException(RecoveryException):
    """Raised when failure diagnostic or taxonomy evaluation fails."""
    pass


class UnrecoverableFailureException(RecoveryException):
    """Raised when a failure cannot be resolved and requires permanent escalation."""
    pass


class CheckpointRestorationException(RecoveryException):
    """Raised when state restoration from snapshot or checkpoint fails."""
    pass


class RollbackCoordinationException(RecoveryException):
    """Raised when compensation rollback execution fails."""
    pass


class StateInconsistencyException(RecoveryException):
    """Raised when state reconciliation detects irreconcilable drift or orphan leaks."""
    pass


class CircuitBreakerOpenException(RecoveryException):
    """Raised when an operation is rejected because a circuit breaker is in OPEN state."""
    pass


class BulkheadExhaustionException(RecoveryException):
    """Raised when an operation is rejected due to bulkhead pool saturation."""
    pass


class EscalationException(RecoveryException):
    """Raised when incident escalation or human handoff fails."""
    pass
