"""
Fluent Builders for Coordination Models.
Ensures validated, fail-fast construction of teams, delegation requests, and coordination sessions.
"""

from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from app.agents.coordination.delegation import DelegationMode, DelegationRequest, DelegationTask
from app.agents.coordination.team import Team, TeamMember, TeamRole, TeamType


class DelegationRequestBuilder:
    """Fluent builder for DelegationRequest."""

    def __init__(self, delegator_agent_id: UUID):
        self._delegator_id = delegator_agent_id
        self._mode = DelegationMode.SINGLE
        self._tasks: List[DelegationTask] = []
        self._max_depth = 3
        self._timeout = 60.0

    def with_mode(self, mode: DelegationMode) -> "DelegationRequestBuilder":
        self._mode = mode
        return self

    def add_task(self, task_id: str, task_name: str, skills: List[str], payload: Dict[str, Any] = None) -> "DelegationRequestBuilder":
        self._tasks.append(DelegationTask(
            task_id=task_id,
            task_name=task_name,
            required_skills=skills,
            payload=payload or {}
        ))
        return self

    def with_timeout(self, timeout_sec: float) -> "DelegationRequestBuilder":
        self._timeout = timeout_sec
        return self

    def build(self) -> DelegationRequest:
        return DelegationRequest(
            delegation_id=uuid4(),
            delegator_agent_id=self._delegator_id,
            mode=self._mode,
            tasks=self._tasks,
            max_recursion_depth=self._max_depth,
            timeout_seconds=self._timeout
        )


class TeamBuilder:
    """Fluent builder for Team."""

    def __init__(self, name: str):
        self._name = name
        self._team_type = TeamType.SUPERVISOR_LED
        self._leader_id: Optional[UUID] = None
        self._members: List[TeamMember] = []

    def with_type(self, team_type: TeamType) -> "TeamBuilder":
        self._team_type = team_type
        return self

    def with_leader(self, leader_id: UUID) -> "TeamBuilder":
        self._leader_id = leader_id
        self._members.append(TeamMember(agent_id=leader_id, role=TeamRole.LEADER))
        return self

    def add_member(self, member_id: UUID, role: TeamRole = TeamRole.WORKER) -> "TeamBuilder":
        self._members.append(TeamMember(agent_id=member_id, role=role))
        return self

    def build(self) -> Team:
        return Team(
            team_id=uuid4(),
            name=self._name,
            team_type=self._team_type,
            leader_id=self._leader_id or (self._members[0].agent_id if self._members else None),
            members=self._members
        )
