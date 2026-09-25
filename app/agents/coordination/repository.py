"""
Coordination Repositories.
Abstract contracts and in-memory implementations for persisting agent records, teams, and sessions.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from uuid import UUID
from app.agents.coordination.team import Team


class TeamRepository(ABC):
    """Persistence contract for agent teams."""

    @abstractmethod
    async def save_team(self, team: Team) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_team(self, team_id: UUID) -> Optional[Team]:
        raise NotImplementedError


class InMemoryTeamRepository(TeamRepository):
    """In-memory storage for active and archived teams."""

    def __init__(self):
        self._teams: Dict[UUID, Team] = {}

    async def save_team(self, team: Team) -> None:
        self._teams[team.team_id] = team

    async def get_team(self, team_id: UUID) -> Optional[Team]:
        return self._teams.get(team_id)

    async def list_all(self) -> List[Team]:
        return list(self._teams.values())
