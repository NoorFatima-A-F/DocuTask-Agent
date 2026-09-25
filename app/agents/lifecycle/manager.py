"""
Enterprise Multi-Agent Intelligence Platform (EMAIP) - Agent Lifecycle Manager.
Implements the 20-state finite state machine, state transition validation,
event emission, audit records, and telemetry metrics.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional, Set
import logging

from app.agents.domain.agent_entity import Agent, AgentLifecycleState

logger = logging.getLogger(__name__)


class InvalidAgentStateTransitionError(Exception):
    """Raised when an illegal agent lifecycle state transition is attempted."""
    pass


@dataclass
class AgentLifecycleEvent:
    """Audit and event record for agent state transitions."""
    agent_id: str
    from_state: AgentLifecycleState
    to_state: AgentLifecycleState
    reason: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "from_state": self.from_state.value if hasattr(self.from_state, "value") else str(self.from_state),
            "to_state": self.to_state.value if hasattr(self.to_state, "value") else str(self.to_state),
            "reason": self.reason,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat(),
        }


class AgentLifecycleManager:
    """
    Manages the lifecycle of autonomous agents, validating state transitions,
    recording audit trails, emitting events, and updating execution metrics.
    """

    # Allowed state transitions
    VALID_TRANSITIONS: Dict[AgentLifecycleState, Set[AgentLifecycleState]] = {
        AgentLifecycleState.CREATED: {
            AgentLifecycleState.REGISTERED,
            AgentLifecycleState.INITIALIZED,
            AgentLifecycleState.FAILED,
            AgentLifecycleState.CANCELLED,
        },
        AgentLifecycleState.REGISTERED: {
            AgentLifecycleState.INITIALIZED,
            AgentLifecycleState.ARCHIVED,
            AgentLifecycleState.FAILED,
            AgentLifecycleState.CANCELLED,
        },
        AgentLifecycleState.INITIALIZED: {
            AgentLifecycleState.PLANNING,
            AgentLifecycleState.REASONING,
            AgentLifecycleState.EXECUTING,
            AgentLifecycleState.WAITING,
            AgentLifecycleState.SUSPENDED,
            AgentLifecycleState.FAILED,
            AgentLifecycleState.CANCELLED,
        },
        AgentLifecycleState.PLANNING: {
            AgentLifecycleState.REASONING,
            AgentLifecycleState.EXECUTING,
            AgentLifecycleState.WAITING,
            AgentLifecycleState.BLOCKED,
            AgentLifecycleState.SUSPENDED,
            AgentLifecycleState.TIMED_OUT,
            AgentLifecycleState.FAILED,
            AgentLifecycleState.CANCELLED,
        },
        AgentLifecycleState.REASONING: {
            AgentLifecycleState.EXECUTING,
            AgentLifecycleState.PLANNING,
            AgentLifecycleState.WAITING,
            AgentLifecycleState.BLOCKED,
            AgentLifecycleState.SUSPENDED,
            AgentLifecycleState.TIMED_OUT,
            AgentLifecycleState.FAILED,
            AgentLifecycleState.CANCELLED,
        },
        AgentLifecycleState.EXECUTING: {
            AgentLifecycleState.OBSERVING,
            AgentLifecycleState.REFLECTING,
            AgentLifecycleState.EVALUATING,
            AgentLifecycleState.WAITING,
            AgentLifecycleState.SUSPENDED,
            AgentLifecycleState.BLOCKED,
            AgentLifecycleState.RECOVERING,
            AgentLifecycleState.TIMED_OUT,
            AgentLifecycleState.FAILED,
            AgentLifecycleState.CANCELLED,
            AgentLifecycleState.COMPLETED,
        },
        AgentLifecycleState.OBSERVING: {
            AgentLifecycleState.REFLECTING,
            AgentLifecycleState.EVALUATING,
            AgentLifecycleState.EXECUTING,
            AgentLifecycleState.FAILED,
            AgentLifecycleState.CANCELLED,
        },
        AgentLifecycleState.REFLECTING: {
            AgentLifecycleState.EVALUATING,
            AgentLifecycleState.CORRECTING,
            AgentLifecycleState.PLANNING,
            AgentLifecycleState.EXECUTING,
            AgentLifecycleState.COMPLETED,
            AgentLifecycleState.FAILED,
        },
        AgentLifecycleState.EVALUATING: {
            AgentLifecycleState.CORRECTING,
            AgentLifecycleState.COMPLETED,
            AgentLifecycleState.WAITING,
            AgentLifecycleState.FAILED,
            AgentLifecycleState.RECOVERING,
        },
        AgentLifecycleState.CORRECTING: {
            AgentLifecycleState.PLANNING,
            AgentLifecycleState.REASONING,
            AgentLifecycleState.EXECUTING,
            AgentLifecycleState.FAILED,
        },
        AgentLifecycleState.WAITING: {
            AgentLifecycleState.RESUMING,
            AgentLifecycleState.EXECUTING,
            AgentLifecycleState.TIMED_OUT,
            AgentLifecycleState.CANCELLED,
            AgentLifecycleState.FAILED,
        },
        AgentLifecycleState.RESUMING: {
            AgentLifecycleState.PLANNING,
            AgentLifecycleState.REASONING,
            AgentLifecycleState.EXECUTING,
            AgentLifecycleState.OBSERVING,
            AgentLifecycleState.FAILED,
        },
        AgentLifecycleState.COMPLETED: {
            AgentLifecycleState.ARCHIVED,
            AgentLifecycleState.INITIALIZED,  # Reuse/reset for new goal
        },
        AgentLifecycleState.ARCHIVED: set(),

        # Failure / Interrupted States
        AgentLifecycleState.FAILED: {
            AgentLifecycleState.RECOVERING,
            AgentLifecycleState.INITIALIZED,
            AgentLifecycleState.ARCHIVED,
        },
        AgentLifecycleState.CANCELLED: {
            AgentLifecycleState.ARCHIVED,
            AgentLifecycleState.INITIALIZED,
        },
        AgentLifecycleState.TIMED_OUT: {
            AgentLifecycleState.RECOVERING,
            AgentLifecycleState.FAILED,
            AgentLifecycleState.ARCHIVED,
        },
        AgentLifecycleState.BLOCKED: {
            AgentLifecycleState.RESUMING,
            AgentLifecycleState.PLANNING,
            AgentLifecycleState.FAILED,
            AgentLifecycleState.CANCELLED,
        },
        AgentLifecycleState.RECOVERING: {
            AgentLifecycleState.RESUMING,
            AgentLifecycleState.PLANNING,
            AgentLifecycleState.EXECUTING,
            AgentLifecycleState.FAILED,
        },
        AgentLifecycleState.SUSPENDED: {
            AgentLifecycleState.RESUMING,
            AgentLifecycleState.CANCELLED,
            AgentLifecycleState.FAILED,
        },
    }

    def __init__(self, event_listener: Optional[Callable[[AgentLifecycleEvent], None]] = None):
        self._history: Dict[str, List[AgentLifecycleEvent]] = {}
        self._listener = event_listener

    def can_transition(self, from_state: AgentLifecycleState | str, to_state: AgentLifecycleState | str) -> bool:
        """Checks if a transition between two states is valid."""
        f_state = from_state if isinstance(from_state, AgentLifecycleState) else AgentLifecycleState(from_state)
        t_state = to_state if isinstance(to_state, AgentLifecycleState) else AgentLifecycleState(to_state)
        allowed = self.VALID_TRANSITIONS.get(f_state, set())
        return t_state in allowed

    def transition(
        self,
        agent: Agent,
        target_state: AgentLifecycleState | str,
        reason: str = "",
        metadata: Optional[Dict[str, Any]] = None
    ) -> AgentLifecycleEvent:
        """
        Executes a validated state transition on an Agent entity, updates timestamps,
        appends to audit history, and emits lifecycle notifications.
        """
        current_state = agent.status if isinstance(agent.status, AgentLifecycleState) else AgentLifecycleState(agent.status)
        to_state = target_state if isinstance(target_state, AgentLifecycleState) else AgentLifecycleState(target_state)

        if not self.can_transition(current_state, to_state):
            msg = f"Illegal transition for agent {agent.id} ({agent.name}) from {current_state.value} to {to_state.value}"
            logger.error(msg)
            raise InvalidAgentStateTransitionError(msg)

        agent.status = to_state
        agent.updated_at = datetime.now(timezone.utc)

        event = AgentLifecycleEvent(
            agent_id=agent.id,
            from_state=current_state,
            to_state=to_state,
            reason=reason,
            metadata=metadata or {},
        )

        if agent.id not in self._history:
            self._history[agent.id] = []
        self._history[agent.id].append(event)

        if self._listener:
            try:
                self._listener(event)
            except Exception as e:
                logger.warning(f"Error in lifecycle event listener: {e}")

        logger.info(f"Agent {agent.id} transitioned: {current_state.value} -> {to_state.value} [{reason}]")
        return event

    def get_history(self, agent_id: str) -> List[AgentLifecycleEvent]:
        """Returns the audit trail of lifecycle events for a given agent."""
        return list(self._history.get(agent_id, []))
