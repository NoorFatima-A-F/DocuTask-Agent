"""Environment Platform & Partition Manager (ESP-MOOS)."""

from __future__ import annotations

from typing import Dict, List, Optional
from app.tenancy.core.models import Environment, EnvironmentType
from app.tenancy.core.exceptions import EnvironmentNotFoundError, TenancyError


class EnvironmentManager:
    """Manages execution environments within workspaces."""

    def __init__(self):
        self._environments: Dict[str, Environment] = {}

    def create_environment(
        self,
        environment_id: str,
        workspace_id: str,
        organization_id: str,
        name: str,
        env_type: EnvironmentType = EnvironmentType.DEVELOPMENT,
        variables: Optional[Dict[str, str]] = None,
        secrets: Optional[Dict[str, str]] = None,
        feature_flags: Optional[Dict[str, bool]] = None,
    ) -> Environment:
        """Create a new execution environment partition."""
        if environment_id in self._environments:
            raise TenancyError(f"Environment '{environment_id}' already exists")

        env = Environment(
            environment_id=environment_id,
            workspace_id=workspace_id,
            organization_id=organization_id,
            name=name,
            env_type=env_type,
            variables=variables or {},
            secrets=secrets or {},
            feature_flags=feature_flags or {},
        )
        self._environments[environment_id] = env
        return env

    def get_environment(
        self, environment_id: str, workspace_id: Optional[str] = None
    ) -> Environment:
        """Retrieve an environment with optional workspace ownership check."""
        env = self._environments.get(environment_id)
        if not env:
            raise EnvironmentNotFoundError(f"Environment '{environment_id}' not found")
        if workspace_id and env.workspace_id != workspace_id:
            raise EnvironmentNotFoundError(f"Environment '{environment_id}' not in workspace '{workspace_id}'")
        return env

    def list_environments(self, workspace_id: str) -> List[Environment]:
        """List all environments within a workspace."""
        return [e for e in self._environments.values() if e.workspace_id == workspace_id]

    def set_variables(self, environment_id: str, variables: Dict[str, str]) -> Environment:
        """Update environment-scoped variables."""
        env = self.get_environment(environment_id)
        env.variables.update(variables)
        return env

    def set_secrets(self, environment_id: str, secrets: Dict[str, str]) -> Environment:
        """Update environment-scoped secret references."""
        env = self.get_environment(environment_id)
        env.secrets.update(secrets)
        return env
