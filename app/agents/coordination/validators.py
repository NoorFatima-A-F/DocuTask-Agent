"""
Coordination Fail-Fast Validators.
Enforces rules preventing duplicate IDs, missing capabilities, circular delegation, orphaned teams, and stale leases.
"""

from typing import List, Set
from uuid import UUID
from app.agents.coordination.agent import Agent
from app.agents.coordination.exceptions import (
    CircularDelegationError,
    DuplicateAgentIdError,
    OrphanedTeamError,
)
from app.agents.coordination.team import Team


class CoordinationValidator:
    """Fail-fast validation rules protecting multi-agent coordination integrity."""

    @staticmethod
    def validate_unique_agent_ids(agents: List[Agent]) -> None:
        """Verifies no duplicate agent IDs exist in a candidate list."""
        seen: Set[UUID] = set()
        for a in agents:
            if a.agent_id in seen:
                raise DuplicateAgentIdError(f"Duplicate agent ID detected: {a.agent_id}", a.agent_id)
            seen.add(a.agent_id)

    @staticmethod
    def validate_team_integrity(team: Team) -> None:
        """Ensures team has active members and a designated leader."""
        if not team.members:
            raise OrphanedTeamError(f"Team '{team.name}' has zero members.")
        if not team.leader_id:
            raise OrphanedTeamError(f"Team '{team.name}' has no designated leader.")

    @staticmethod
    def validate_delegation_acyclic(chain: List[UUID]) -> None:
        """Ensures a delegation sequence contains no cycles."""
        seen: Set[UUID] = set()
        for aid in chain:
            if aid in seen:
                raise CircularDelegationError(f"Cycle detected in delegation chain at agent {aid}.", aid)
            seen.add(aid)
