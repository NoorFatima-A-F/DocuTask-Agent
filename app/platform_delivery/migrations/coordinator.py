"""Migration Coordinator Platform (Req 45)."""
from typing import Callable, Dict, List, Optional
from .expand_contract import MigrationSafetyValidator, MigrationStep


class MigrationCoordinator:
    """Orchestrates database schema migrations across tenants and environments."""

    def __init__(self, sql_runner: Optional[Callable[[str], bool]] = None):
        self.sql_runner = sql_runner or (lambda sql: True)
        self._migrations: Dict[str, MigrationStep] = {}
        self._applied: List[str] = []

    def register_migration(self, step: MigrationStep) -> None:
        MigrationSafetyValidator.validate_step(step)
        self._migrations[step.version] = step

    def apply_migration(self, version: str) -> MigrationStep:
        step = self._migrations.get(version)
        if not step:
            raise KeyError(f"Migration version '{version}' not found")
        if version in self._applied:
            return step

        self.sql_runner(step.up_sql)
        self._applied.append(version)
        return step

    def rollback_migration(self, version: str) -> MigrationStep:
        step = self._migrations.get(version)
        if not step or not step.down_sql:
            raise ValueError(f"Cannot rollback migration '{version}': missing down_sql")
        if version in self._applied:
            self.sql_runner(step.down_sql)
            self._applied.remove(version)
        return step

    def get_applied(self) -> List[str]:
        return list(self._applied)
