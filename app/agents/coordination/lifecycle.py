"""
Agent Lifecycle and Coordination Lifecycle States.
Enforces validated, deterministic transitions across 12 agent states and coordination run states.
"""

from enum import Enum


class AgentLifecycleState(str, Enum):
    """12-state deterministic lifecycle for distributed agents."""
    CREATED = "CREATED"
    REGISTERED = "REGISTERED"
    AVAILABLE = "AVAILABLE"
    RESERVED = "RESERVED"
    ASSIGNED = "ASSIGNED"
    EXECUTING = "EXECUTING"
    WAITING = "WAITING"
    PAUSED = "PAUSED"
    DEGRADED = "DEGRADED"
    RECOVERING = "RECOVERING"
    UNAVAILABLE = "UNAVAILABLE"
    RETIRED = "RETIRED"

    def is_operational(self) -> bool:
        """Checks if the agent can accept tasks or participate in teams."""
        return self in (
            AgentLifecycleState.AVAILABLE,
            AgentLifecycleState.RESERVED,
            AgentLifecycleState.ASSIGNED,
            AgentLifecycleState.EXECUTING,
            AgentLifecycleState.WAITING,
        )

    def is_terminal(self) -> bool:
        """Checks if the agent has reached a terminal retirement state."""
        return self == AgentLifecycleState.RETIRED


class CoordinationLifecycleState(str, Enum):
    """Lifecycle state of a coordinated multi-agent workflow."""
    PENDING = "PENDING"
    DISCOVERING = "DISCOVERING"
    DELEGATING = "DELEGATING"
    COORDINATING = "COORDINATING"
    EXECUTING = "EXECUTING"
    SYNCHRONIZING = "SYNCHRONIZING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

    def is_terminal(self) -> bool:
        """Checks if coordination has terminated."""
        return self in (CoordinationLifecycleState.COMPLETED, CoordinationLifecycleState.FAILED)
