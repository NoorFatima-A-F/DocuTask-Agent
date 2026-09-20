"""
Autonomous Agent Exception Hierarchy.
Provides custom domain exceptions for agent state transitions, planning, execution, observation, reflection, memory, and recovery.
"""


class AgentException(Exception):
    """Base exception for all autonomous agent errors."""

    def __init__(self, message: str, details: dict | None = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class InvalidStateTransitionException(AgentException):
    """Raised when an invalid agent state transition is attempted."""
    pass


class PlanningException(AgentException):
    """Raised when an error occurs during agent goal planning."""
    pass


class ExecutionException(AgentException):
    """Raised when an error occurs during agent plan execution."""
    pass


class ObservationException(AgentException):
    """Raised when an error occurs during agent environment observation."""
    pass


class ReflectionException(AgentException):
    """Raised when an error occurs during agent self-reflection."""
    pass


class MemoryException(AgentException):
    """Raised when an error occurs during agent memory operations."""
    pass


class RecoveryException(AgentException):
    """Raised when an error occurs during agent failure recovery."""
    pass


class ConfigurationException(AgentException):
    """Raised when invalid agent configuration parameters are provided."""
    pass


class ToolSelectionException(AgentException):
    """Raised when tool selection or invocation fails."""
    pass


class WorkflowException(AgentException):
    """Raised when agent workflow orchestration fails."""
    pass
