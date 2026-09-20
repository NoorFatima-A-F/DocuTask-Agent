"""
Task Graph Repository for Persistent Task Graph Intelligence.
Provides abstract persistence contract with In-Memory and File-backed implementations.
"""

from __future__ import annotations

import json
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional
from uuid import UUID

from app.agents.workflow.persistence.workflow_checkpoint import TaskGraphSnapshot

logger = logging.getLogger(__name__)


class TaskGraphRepository(ABC):
    """Abstract persistence interface for task graph snapshots."""

    @abstractmethod
    def save(self, snapshot: TaskGraphSnapshot) -> None:
        """Saves or updates a task graph snapshot."""
        pass

    @abstractmethod
    def get_by_id(self, snapshot_id: UUID) -> Optional[TaskGraphSnapshot]:
        """Retrieves a snapshot by its unique ID."""
        pass

    @abstractmethod
    def get_latest_by_plan(self, plan_id: str) -> Optional[TaskGraphSnapshot]:
        """Retrieves the most recent snapshot for a plan ID."""
        pass

    @abstractmethod
    def list_by_plan(self, plan_id: str) -> List[TaskGraphSnapshot]:
        """Lists all snapshots for a plan ID ordered by step index."""
        pass

    @abstractmethod
    def delete(self, snapshot_id: UUID) -> bool:
        """Deletes a snapshot."""
        pass


class InMemoryTaskGraphRepository(TaskGraphRepository):
    """Thread-safe in-memory store for unit testing and fast ephemeral workflows."""

    def __init__(self) -> None:
        self._store: Dict[UUID, TaskGraphSnapshot] = {}

    def save(self, snapshot: TaskGraphSnapshot) -> None:
        self._store[snapshot.snapshot_id] = snapshot
        logger.debug("Saved snapshot %s for plan %s (step %d)", snapshot.snapshot_id, snapshot.plan_id, snapshot.step_index)

    def get_by_id(self, snapshot_id: UUID) -> Optional[TaskGraphSnapshot]:
        return self._store.get(snapshot_id)

    def get_latest_by_plan(self, plan_id: str) -> Optional[TaskGraphSnapshot]:
        matches = [s for s in self._store.values() if s.plan_id == plan_id]
        if not matches:
            return None
        matches.sort(key=lambda s: (s.step_index, s.created_at), reverse=True)
        return matches[0]

    def list_by_plan(self, plan_id: str) -> List[TaskGraphSnapshot]:
        matches = [s for s in self._store.values() if s.plan_id == plan_id]
        matches.sort(key=lambda s: s.step_index)
        return matches

    def delete(self, snapshot_id: UUID) -> bool:
        if snapshot_id in self._store:
            del self._store[snapshot_id]
            return True
        return False

    def clear(self) -> None:
        self._store.clear()


class FileTaskGraphRepository(TaskGraphRepository):
    """File-backed snapshot repository storing JSON documents on disk."""

    def __init__(self, base_directory: Path) -> None:
        self.base_directory = Path(base_directory)
        self.base_directory.mkdir(parents=True, exist_ok=True)

    def _get_path(self, snapshot_id: UUID) -> Path:
        return self.base_directory / f"{snapshot_id}.json"

    def save(self, snapshot: TaskGraphSnapshot) -> None:
        file_path = self._get_path(snapshot.snapshot_id)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(snapshot.to_dict(), f, indent=2)
        logger.debug("Saved snapshot %s to file %s", snapshot.snapshot_id, file_path)

    def get_by_id(self, snapshot_id: UUID) -> Optional[TaskGraphSnapshot]:
        file_path = self._get_path(snapshot_id)
        if not file_path.exists():
            return None
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return TaskGraphSnapshot.from_dict(data)

    def get_latest_by_plan(self, plan_id: str) -> Optional[TaskGraphSnapshot]:
        all_snapshots = self.list_by_plan(plan_id)
        return all_snapshots[-1] if all_snapshots else None

    def list_by_plan(self, plan_id: str) -> List[TaskGraphSnapshot]:
        results: List[TaskGraphSnapshot] = []
        for file in self.base_directory.glob("*.json"):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if data.get("plan_id") == plan_id:
                    results.append(TaskGraphSnapshot.from_dict(data))
            except Exception as ex:
                logger.warning("Failed to load snapshot from %s: %s", file, ex)
        results.sort(key=lambda s: s.step_index)
        return results

    def delete(self, snapshot_id: UUID) -> bool:
        file_path = self._get_path(snapshot_id)
        if file_path.exists():
            file_path.unlink()
            return True
        return False
