"""Team Management Platform (ESP-MOOS)."""

from __future__ import annotations

from typing import Dict, List, Optional
from app.tenancy.core.models import Team
from app.tenancy.core.exceptions import TenancyError


class TeamManager:
    """Manages cross-functional teams within organizations."""

    def __init__(self):
        self._teams: Dict[str, Team] = {}

    def create_team(
        self,
        team_id: str,
        organization_id: str,
        name: str,
        department: str,
        description: str = "",
        member_ids: Optional[List[str]] = None,
    ) -> Team:
        """Create a new team within an organization."""
        if team_id in self._teams:
            raise TenancyError(f"Team '{team_id}' already exists")

        team = Team(
            team_id=team_id,
            organization_id=organization_id,
            name=name,
            department=department,
            description=description,
            member_ids=member_ids or [],
        )
        self._teams[team_id] = team
        return team

    def get_team(self, team_id: str) -> Team:
        """Retrieve team by ID."""
        team = self._teams.get(team_id)
        if not team:
            raise TenancyError(f"Team '{team_id}' not found")
        return team

    def list_teams(self, organization_id: str) -> List[Team]:
        """List all teams within an organization."""
        return [t for t in self._teams.values() if t.organization_id == organization_id]

    def add_member(self, team_id: str, user_id: str) -> Team:
        """Add user to team."""
        team = self.get_team(team_id)
        if user_id not in team.member_ids:
            team.member_ids.append(user_id)
        return team

    def remove_member(self, team_id: str, user_id: str) -> Team:
        """Remove user from team."""
        team = self.get_team(team_id)
        if user_id in team.member_ids:
            team.member_ids.remove(user_id)
        return team
