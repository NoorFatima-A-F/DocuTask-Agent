"""
Team Domain Models.
Defines team structures, roles, memberships, and team lifecycle management.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class TeamType(str, Enum):
    """Structural topology of an agent team."""
    SUPERVISOR_LED = "SUPERVISOR_LED"
    PEER_TEAM = "PEER_TEAM"
    DYNAMIC_EPHEMERAL = "DYNAMIC_EPHEMERAL"
    FIXED_STANDING = "FIXED_STANDING"
    SWARM = "SWARM"


class TeamRole(str, Enum):
    """Roles within a team."""
    LEADER = "LEADER"
    SUPERVISOR = "SUPERVISOR"
    WORKER = "WORKER"
    CRITIC = "CRITIC"
    SPECIALIST = "SPECIALIST"


class TeamMember(BaseModel):
    """Membership record of an agent in a team."""
    agent_id: UUID
    role: TeamRole = TeamRole.WORKER
    joined_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = {"frozen": True}


class Team(BaseModel):
    """Team entity representing a cooperative group of agents working toward a common objective."""
    team_id: UUID = Field(default_factory=uuid4)
    name: str
    team_type: TeamType = TeamType.SUPERVISOR_LED
    leader_id: Optional[UUID] = None
    members: List[TeamMember] = Field(default_factory=list)
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def add_member(self, agent_id: UUID, role: TeamRole = TeamRole.WORKER) -> "Team":
        """Adds a new member to the team."""
        new_members = [*self.members, TeamMember(agent_id=agent_id, role=role)]
        leader = agent_id if role in (TeamRole.LEADER, TeamRole.SUPERVISOR) and not self.leader_id else self.leader_id
        return self.model_copy(update={"members": new_members, "leader_id": leader})

    def disband(self) -> "Team":
        """Marks team as inactive/disbanded."""
        return self.model_copy(update={"is_active": False})
