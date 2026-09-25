"""
Enterprise Execution Exception Hierarchy.
Provides domain exceptions for runtime state transitions, scheduling failures,
worker pool exhaustion, dependency deadlocks, tool invocation errors, rollback errors,
and cancellation.
"""

from app.agents.exceptions import AgentException


class ExecutionException(AgentException):
    """Base exception for all execution and runtime subsystem errors."""
    pass


class IllegalStateTransitionException(ExecutionException):
    """Raised when an invalid task or execution state transition is attempted."""
    pass


class DependencyResolutionException(ExecutionException):
    """Raised when prerequisite task dependencies cannot be resolved or are deadlocked."""
    pass


class WorkerExhaustionException(ExecutionException):
    """Raised when no worker is available within timeout or lease reservation fails."""
    pass


class ToolDispatchException(ExecutionException):
    """Raised when tool lookup, invocation, or payload dispatching fails."""
    pass


class CheckpointException(ExecutionException):
    """Raised when state snapshot or checkpoint capture/restoration fails."""
    pass


class RollbackException(ExecutionException):
    """Raised when compensation actions or rollback graph traversal fails."""
    pass


class ExecutionTimeoutException(ExecutionException):
    """Raised when a task or overall workflow execution exceeds its allotted deadline."""
    pass


class ExecutionCancelledException(ExecutionException):
    """Raised when execution is cancelled via graceful or forced cancellation."""
    pass
