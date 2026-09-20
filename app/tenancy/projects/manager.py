"""Project Platform & Deployment Boundary Manager (ESP-MOOS)."""

from __future__ import annotations

from typing import Dict, List, Optional
from app.tenancy.core.models import Project
from app.tenancy.core.exceptions import ProjectNotFoundError, TenancyError


class ProjectManager:
    """Manages project deployment boundaries within workspaces."""

    def __init__(self):
        self._projects: Dict[str, Project] = {}

    def create_project(
        self,
        project_id: str,
        workspace_id: str,
        organization_id: str,
        name: str,
        description: str = "",
        workflows: Optional[List[str]] = None,
        agents: Optional[List[str]] = None,
        knowledge_spaces: Optional[List[str]] = None,
        connectors: Optional[List[str]] = None,
        variables: Optional[Dict[str, str]] = None,
    ) -> Project:
        """Create a new project boundary."""
        if project_id in self._projects:
            raise TenancyError(f"Project '{project_id}' already exists")

        project = Project(
            project_id=project_id,
            workspace_id=workspace_id,
            organization_id=organization_id,
            name=name,
            description=description,
            workflows=workflows or [],
            agents=agents or [],
            knowledge_spaces=knowledge_spaces or [],
            connectors=connectors or [],
            variables=variables or {},
        )
        self._projects[project_id] = project
        return project

    def get_project(self, project_id: str, workspace_id: Optional[str] = None) -> Project:
        """Retrieve project with optional workspace ownership check."""
        proj = self._projects.get(project_id)
        if not proj:
            raise ProjectNotFoundError(f"Project '{project_id}' not found")
        if workspace_id and proj.workspace_id != workspace_id:
            raise ProjectNotFoundError(f"Project '{project_id}' does not belong to workspace '{workspace_id}'")
        return proj

    def list_projects(self, workspace_id: str) -> List[Project]:
        """List all projects within a workspace."""
        return [p for p in self._projects.values() if p.workspace_id == workspace_id]

    def add_resource(self, project_id: str, resource_type: str, resource_id: str) -> Project:
        """Attach a platform resource to a project boundary."""
        proj = self.get_project(project_id)
        if resource_type == "workflow" and resource_id not in proj.workflows:
            proj.workflows.append(resource_id)
        elif resource_type == "agent" and resource_id not in proj.agents:
            proj.agents.append(resource_id)
        elif resource_type == "knowledge" and resource_id not in proj.knowledge_spaces:
            proj.knowledge_spaces.append(resource_id)
        elif resource_type == "connector" and resource_id not in proj.connectors:
            proj.connectors.append(resource_id)
        return proj
