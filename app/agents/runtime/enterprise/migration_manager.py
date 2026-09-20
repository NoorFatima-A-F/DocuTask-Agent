"""
Runtime State Migration Manager.
Coordinates database schema migrations and in-flight session schema transformations across versions.
"""

from typing import Any, Callable, Dict, List, Optional
from uuid import UUID


class MigrationManager:
    """Manages schema migrations and data transformations across runtime versions."""

    def __init__(self) -> None:
        self._migration_steps: List[Callable[[Dict[str, Any]], Dict[str, Any]]] = []

    def register_step(self, step_fn: Callable[[Dict[str, Any]], Dict[str, Any]]) -> None:
        """Registers a sequential data migration step."""
        self._migration_steps.append(step_fn)

    def migrate_session_state(self, state_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Applies registered migrations in order to transform state to current schema."""
        current = dict(state_dict)
        for step in self._migration_steps:
            current = step(current)
        return current
