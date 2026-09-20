"""
Agent Presence Manager.
Maintains live presence states: ONLINE, OFFLINE, BUSY, IDLE.
"""

from enum import Enum
from typing import Dict
from uuid import UUID


class PresenceState(str, Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    BUSY = "BUSY"
    IDLE = "IDLE"


class PresenceManager:
    """Manages presence status for registered agents."""

    def __init__(self):
        self._presence: Dict[UUID, PresenceState] = {}

    def set_presence(self, agent_id: UUID, state: PresenceState) -> None:
        self._presence[agent_id] = state

    def get_presence(self, agent_id: UUID) -> PresenceState:
        return self._presence.get(agent_id, PresenceState.OFFLINE)

    def is_available(self, agent_id: UUID) -> bool:
        return self.get_presence(agent_id) in (PresenceState.ONLINE, PresenceState.IDLE)
