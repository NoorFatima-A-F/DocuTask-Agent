"""Workspace Platform & Boundary Manager (ESP-MOOS)."""

from __future__ import annotations

from typing import Dict, List, Optional
from app.tenancy.core.models import Workspace, Region
from app.tenancy.core.exceptions import WorkspaceNotFoundError, TenancyError


class WorkspaceManager:
    """Manages workspaces within tenant organizations."""

    def __init__(self):
        self._workspaces: Dict[str, Workspace] = {}

    def create_workspace(
        self,
        workspace_id: str,
        organization_id: str,
        name: str,
        description: str = "",
        department: str = "General",
        region: Region = Region.US_EAST,
        policies: Optional[Dict[str, any]] = None,
        configuration: Optional[Dict[str, any]] = None,
    ) -> Workspace:
        """Create a new workspace boundary."""
        if workspace_id in self._workspaces:
            raise TenancyError(f"Workspace '{workspace_id}' already exists")

        workspace = Workspace(
            workspace_id=workspace_id,
            organization_id=organization_id,
            name=name,
            description=description,
            department=department,
            region=region,
            policies=policies or {},
            configuration=configuration or {},
        )
        self._workspaces[workspace_id] = workspace
        return workspace

    def get_workspace(self, workspace_id: str, organization_id: Optional[str] = None) -> Workspace:
        """Retrieve workspace with optional cross-tenant ownership check."""
        ws = self._workspaces.get(workspace_id)
        if not ws:
            raise WorkspaceNotFoundError(f"Workspace '{workspace_id}' not found")
        if organization_id and ws.organization_id != organization_id:
            raise WorkspaceNotFoundError(f"Workspace '{workspace_id}' does not belong to organization '{organization_id}'")
        return ws

    def list_workspaces(self, organization_id: str) -> List[Workspace]:
        """List all workspaces belonging to an organization."""
        return [ws for ws in self._workspaces.values() if ws.organization_id == organization_id]

    def delete_workspace(self, workspace_id: str, organization_id: str) -> None:
        """Delete a workspace after verifying organization ownership."""
        ws = self.get_workspace(workspace_id, organization_id=organization_id)
        del self._workspaces[ws.workspace_id]
