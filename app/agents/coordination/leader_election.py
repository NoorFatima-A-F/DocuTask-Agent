"""
Leader Election Engine.
Implements Bully-style priority election and Raft-inspired heartbeats for electing team leaders or supervisors.
"""

from typing import List, Optional
from uuid import UUID
from app.agents.coordination.agent import Agent
from app.agents.coordination.interfaces import ILeaderElectionEngine


class LeaderElectionEngine(ILeaderElectionEngine):
    """Elects a leader from candidate agents based on priority, reputation, and uptime."""

    async def elect_leader(self, candidates: List[Agent]) -> Optional[Agent]:
        """Selects leader with highest priority level, breaking ties with reputation and completed tasks."""
        if not candidates:
            return None

        # Filter to operational agents
        operational = [a for a in candidates if a.state.is_operational()]
        if not operational:
            return None

        sorted_candidates = sorted(
            operational,
            key=lambda a: (
                a.profile.priority_level,
                a.reputation_score,
                a.completed_task_count
            ),
            reverse=True
        )

        return sorted_candidates[0]
