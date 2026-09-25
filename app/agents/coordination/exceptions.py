"""
Coordination Exception Hierarchy.
Defines strongly typed exceptions for multi-agent coordination, lifecycle, and delegation failures.
"""

from typing import Optional
from uuid import UUID


class CoordinationException(Exception):
    """Base exception for all multi-agent coordination errors."""

    def __init__(self, message: str, agent_id: Optional[UUID] = None):
        super().__init__(message)
        self.agent_id = agent_id


class DuplicateAgentIdError(CoordinationException):
    """Raised when registering an agent with an ID that already exists in the registry."""
    pass


class AgentNotFoundError(CoordinationException):
    """Raised when an operation targets an unregistered or non-existent agent."""
    pass


class MissingCapabilityError(CoordinationException):
    """Raised when no registered agent satisfies the mandatory capability constraints."""
    pass


class CircularDelegationError(CoordinationException):
    """Raised when a task delegation forms a circular loop between agents."""
    pass


class OrphanedTeamError(CoordinationException):
    """Raised when a team has no designated leader or active members."""
    pass


class InvalidCommunicationRouteError(CoordinationException):
    """Raised when routing a message to an unreachable, dead, or unregistered channel."""
    pass


class StaleLeaseError(CoordinationException):
    """Raised when an operation is attempted with an expired or stolen task lease."""
    pass


class InconsistentSharedStateError(CoordinationException):
    """Raised when concurrent state updates violate optimistic locking or version consistency."""
    pass


class UnsupportedProtocolError(CoordinationException):
    """Raised when an unsupported coordination or negotiation protocol is invoked."""
    pass


class ConsensusNotReachedError(CoordinationException):
    """Raised when voting fails to achieve required quorum or majority threshold."""
    pass
