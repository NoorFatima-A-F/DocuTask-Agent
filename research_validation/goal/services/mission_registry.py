"""
Mission Registry Service
========================
Provides central registry, query, and lookup capabilities for all missions.
"""

from typing import List, Optional
from research_validation.goal.models.mission import Mission
from research_validation.goal.models.mission_state import MissionState
from research_validation.goal.interfaces.repository import IMissionRepository


class MissionRegistry:
    """Central registry and lookup engine for autonomous missions."""

    def __init__(self, repository: IMissionRepository):
        self.repo = repository

    def register_mission(self, mission: Mission) -> None:
        self.repo.save_mission(mission)

    def get_mission(self, mission_id: str) -> Optional[Mission]:
        return self.repo.get_mission_by_id(mission_id)

    def get_mission_by_goal(self, goal_id: str) -> Optional[Mission]:
        return self.repo.get_mission_by_goal_id(goal_id)

    def get_active_missions(self) -> List[Mission]:
        return self.repo.list_missions(state=MissionState.ACTIVE.value)

    def get_ready_missions(self) -> List[Mission]:
        return self.repo.list_missions(state=MissionState.READY_FOR_OBSERVATION.value)
