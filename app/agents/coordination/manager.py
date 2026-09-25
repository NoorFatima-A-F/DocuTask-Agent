"""
Coordination Manager.
Coordinates session tracking, lease lifecycle, and active team memberships.
"""

from typing import Optional
from app.agents.coordination.agent_registry import AgentRegistry
from app.agents.coordination.lease_manager import LeaseManager
from app.agents.coordination.presence import PresenceManager
from app.agents.coordination.repository import InMemoryTeamRepository, TeamRepository


class CoordinationManager:
    """Manages active coordination infrastructure: registries, leases, presence, and team stores."""

    def __init__(
        self,
        registry: Optional[AgentRegistry] = None,
        lease_manager: Optional[LeaseManager] = None,
        presence_manager: Optional[PresenceManager] = None,
        team_repository: Optional[TeamRepository] = None
    ):
        self.registry = registry or AgentRegistry()
        self.lease_manager = lease_manager or LeaseManager()
        self.presence_manager = presence_manager or PresenceManager()
        self.team_repository = team_repository or InMemoryTeamRepository()
