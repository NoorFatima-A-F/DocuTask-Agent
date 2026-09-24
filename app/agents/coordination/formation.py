"""
Team Formation Engine.
Assembles and provisions dynamic, supervisor-led, peer, and ephemeral teams from candidate agent pools.
"""

from typing import List, Optional
from uuid import uuid4
from app.agents.coordination.agent import Agent
from app.agents.coordination.team import Team, TeamMember, TeamRole, TeamType


class TeamFormationEngine:
    """Forms cohesive agent teams based on task composition and topological requirements."""

    def form_supervisor_team(
        self,
        name: str,
        supervisor: Agent,
        workers: List[Agent]
    ) -> Team:
        """Forms a supervisor-led hierarchical team."""
        members = [TeamMember(agent_id=supervisor.agent_id, role=TeamRole.SUPERVISOR)]
        for w in workers:
            members.append(TeamMember(agent_id=w.agent_id, role=TeamRole.WORKER))

        return Team(
            team_id=uuid4(),
            name=name,
            team_type=TeamType.SUPERVISOR_LED,
            leader_id=supervisor.agent_id,
            members=members
        )

    def form_peer_team(
        self,
        name: str,
        peers: List[Agent]
    ) -> Team:
        """Forms a decentralized peer-to-peer team."""
        members = [TeamMember(agent_id=p.agent_id, role=TeamRole.WORKER) for p in peers]
        leader_id = peers[0].agent_id if peers else None

        return Team(
            team_id=uuid4(),
            name=name,
            team_type=TeamType.PEER_TEAM,
            leader_id=leader_id,
            members=members
        )

    def form_dynamic_team(
        self,
        name: str,
        selected_agents: List[Agent],
        leader: Optional[Agent] = None
    ) -> Team:
        """Forms an ephemeral, task-specific dynamic team."""
        leader_id = leader.agent_id if leader else (selected_agents[0].agent_id if selected_agents else None)
        members = []
        for a in selected_agents:
            role = TeamRole.LEADER if a.agent_id == leader_id else TeamRole.WORKER
            members.append(TeamMember(agent_id=a.agent_id, role=role))

        return Team(
            team_id=uuid4(),
            name=name,
            team_type=TeamType.DYNAMIC_EPHEMERAL,
            leader_id=leader_id,
            members=members
        )
