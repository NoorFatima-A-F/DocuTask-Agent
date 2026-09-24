"""
Repository Interfaces
=====================
Abstract repository contracts for persisting and retrieving immutable Goal and Mission entities.
"""

from abc import ABC, abstractmethod
from typing import Any, List, Optional


class IGoalRepository(ABC):
    """Repository interface for Goal entity storage and retrieval."""

    @abstractmethod
    def save_goal(self, goal: Any) -> None:
        """Persists a new or updated Goal version."""
        raise NotImplementedError

    @abstractmethod
    def get_goal_by_id(self, goal_id: str) -> Optional[Any]:
        """Retrieves the latest version of a Goal by its ID."""
        raise NotImplementedError

    @abstractmethod
    def get_goal_version(self, goal_id: str, version: str) -> Optional[Any]:
        """Retrieves a specific historical version of a Goal."""
        raise NotImplementedError

    @abstractmethod
    def list_goals(self, status: Optional[str] = None, owner: Optional[str] = None) -> List[Any]:
        """Lists goals with optional status or owner filtering."""
        raise NotImplementedError

    @abstractmethod
    def get_version_history(self, goal_id: str) -> List[Any]:
        """Returns the full historical version chain for a Goal."""
        raise NotImplementedError


class IMissionRepository(ABC):
    """Repository interface for Mission entity storage and retrieval."""

    @abstractmethod
    def save_mission(self, mission: Any) -> None:
        """Persists a new or updated Mission version."""
        raise NotImplementedError

    @abstractmethod
    def get_mission_by_id(self, mission_id: str) -> Optional[Any]:
        """Retrieves the latest version of a Mission by ID."""
        raise NotImplementedError

    @abstractmethod
    def get_mission_by_goal_id(self, goal_id: str) -> Optional[Any]:
        """Retrieves the Mission associated with a specific Goal."""
        raise NotImplementedError

    @abstractmethod
    def list_missions(self, state: Optional[str] = None) -> List[Any]:
        """Lists all missions matching an optional lifecycle state."""
        raise NotImplementedError

    @abstractmethod
    def get_version_history(self, mission_id: str) -> List[Any]:
        """Returns the full historical version chain for a Mission."""
        raise NotImplementedError
