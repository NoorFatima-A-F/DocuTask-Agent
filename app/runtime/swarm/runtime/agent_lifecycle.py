"""
AMCN-SIP Phase 13.8 - Agent Lifecycle Manager
Manages the 11-state agent lifecycle transitions and enforces valid lifecycle invariants.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set, Tuple, Union
from app.runtime.swarm.events.swarm_events import AgentLifecycleState, AgentState


class AgentLifecycleManager:
    """
    State machine enforcing valid transitions for swarm agents.
    """

    VALID_TRANSITIONS: Dict[AgentLifecycleState, Set[AgentLifecycleState]] = {
        AgentLifecycleState.CREATED: {AgentLifecycleState.REGISTERED, AgentLifecycleState.ARCHIVED},
        AgentLifecycleState.REGISTERED: {AgentLifecycleState.AVAILABLE, AgentLifecycleState.ARCHIVED},
        AgentLifecycleState.AVAILABLE: {AgentLifecycleState.ASSIGNED, AgentLifecycleState.NEGOTIATING, AgentLifecycleState.VOTING, AgentLifecycleState.RECOVERING, AgentLifecycleState.ARCHIVED},
        AgentLifecycleState.ASSIGNED: {AgentLifecycleState.EXECUTING, AgentLifecycleState.WAITING, AgentLifecycleState.RECOVERING, AgentLifecycleState.AVAILABLE},
        AgentLifecycleState.EXECUTING: {AgentLifecycleState.WAITING, AgentLifecycleState.COMPLETED, AgentLifecycleState.RECOVERING, AgentLifecycleState.AVAILABLE},
        AgentLifecycleState.WAITING: {AgentLifecycleState.EXECUTING, AgentLifecycleState.RECOVERING, AgentLifecycleState.AVAILABLE},
        AgentLifecycleState.NEGOTIATING: {AgentLifecycleState.ASSIGNED, AgentLifecycleState.AVAILABLE, AgentLifecycleState.RECOVERING},
        AgentLifecycleState.VOTING: {AgentLifecycleState.ASSIGNED, AgentLifecycleState.AVAILABLE, AgentLifecycleState.RECOVERING},
        AgentLifecycleState.RECOVERING: {AgentLifecycleState.AVAILABLE, AgentLifecycleState.ARCHIVED},
        AgentLifecycleState.COMPLETED: {AgentLifecycleState.AVAILABLE, AgentLifecycleState.ARCHIVED},
        AgentLifecycleState.ARCHIVED: set(),
    }

    def __init__(self):
        self._history: Dict[str, List[Dict[str, Any]]] = {}

    def can_transition(self, current_state: AgentLifecycleState, target_state: AgentLifecycleState) -> bool:
        if current_state == target_state:
            return True
        allowed = self.VALID_TRANSITIONS.get(current_state, set())
        return target_state in allowed

    def transition(
        self,
        registry_or_current: Union[Any, AgentLifecycleState],
        agent_id_or_target: Union[str, AgentLifecycleState],
        target_state: Optional[AgentLifecycleState] = None,
        reason: str = "State transition",
    ) -> Union[Tuple[bool, str], AgentLifecycleState]:
        # Overload 1: transition(registry, agent_id, target_state, reason)
        if target_state is not None:
            registry = registry_or_current
            agent_id = str(agent_id_or_target)
            agent = registry.get_agent(agent_id) if hasattr(registry, "get_agent") else None
            if not agent:
                return False, f"Agent {agent_id} not found."

            if not self.can_transition(agent.state, target_state):
                return False, f"Invalid transition from {agent.state.value} to {target_state.value}."

            old_state = agent.state
            agent.state = target_state

            if agent_id not in self._history:
                self._history[agent_id] = []
            self._history[agent_id].append({
                "from_state": old_state.value,
                "to_state": target_state.value,
                "reason": reason,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            return True, f"Agent transitioned to {target_state.value}."

        # Overload 2: transition(current_state, target_state)
        current_state = registry_or_current
        target = agent_id_or_target
        if not self.can_transition(current_state, target):
            return target
        return target

    def get_history(self, agent_id: str) -> List[Dict[str, Any]]:
        return self._history.get(agent_id, [])
