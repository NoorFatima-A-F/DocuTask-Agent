"""
In-Memory Goal and Mission Repositories
=======================================
High-performance in-memory repository implementations supporting immutable version histories.
"""

from typing import Any, Dict, List, Optional
from research_validation.goal.interfaces.repository import IGoalRepository, IMissionRepository
from research_validation.goal.models.goal import Goal
from research_validation.goal.models.mission import Mission


class InMemoryGoalRepository(IGoalRepository):
    """In-memory storage for Goal entities with version indexing."""

    def __init__(self):
        # goal_id -> list of versions in chronological order
        self._goals_by_id: Dict[str, List[Goal]] = {}

    def save_goal(self, goal: Goal) -> None:
        history = self._goals_by_id.setdefault(goal.goal_id, [])
        history.append(goal)

    def get_goal_by_id(self, goal_id: str) -> Optional[Goal]:
        history = self._goals_by_id.get(goal_id)
        if not history:
            return None
        return history[-1]  # Return latest version

    def get_goal_version(self, goal_id: str, version: str) -> Optional[Goal]:
        for g in self._goals_by_id.get(goal_id, []):
            if g.version == version:
                return g
        return None

    def list_goals(self, status: Optional[str] = None, owner: Optional[str] = None) -> List[Goal]:
        results: List[Goal] = []
        for history in self._goals_by_id.values():
            if history:
                latest = history[-1]
                if status and latest.status.value != status:
                    continue
                if owner and latest.owner != owner:
                    continue
                results.append(latest)
        return results

    def get_version_history(self, goal_id: str) -> List[Goal]:
        return list(self._goals_by_id.get(goal_id, []))


class InMemoryMissionRepository(IMissionRepository):
    """In-memory storage for Mission entities with version indexing."""

    def __init__(self):
        # mission_id -> list of versions in chronological order
        self._missions_by_id: Dict[str, List[Mission]] = {}
        self._missions_by_goal_id: Dict[str, str] = {}  # goal_id -> mission_id

    def save_mission(self, mission: Mission) -> None:
        history = self._missions_by_id.setdefault(mission.mission_id, [])
        history.append(mission)
        self._missions_by_goal_id[mission.goal_id] = mission.mission_id

    def get_mission_by_id(self, mission_id: str) -> Optional[Mission]:
        history = self._missions_by_id.get(mission_id)
        if not history:
            return None
        return history[-1]

    def get_mission_by_goal_id(self, goal_id: str) -> Optional[Mission]:
        mission_id = self._missions_by_goal_id.get(goal_id)
        if not mission_id:
            return None
        return self.get_mission_by_id(mission_id)

    def list_missions(self, state: Optional[str] = None) -> List[Mission]:
        results: List[Mission] = []
        for history in self._missions_by_id.values():
            if history:
                latest = history[-1]
                if state and latest.state.value != state:
                    continue
                results.append(latest)
        return results

    def get_version_history(self, mission_id: str) -> List[Mission]:
        return list(self._missions_by_id.get(mission_id, []))
