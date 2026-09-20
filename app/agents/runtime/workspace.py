"""
Workspace Manager.
Manages per-tenant and per-agent workspace directories, sandboxing, and file isolation.
"""

import os
from pathlib import Path
from typing import Optional


class WorkspaceManager:
    """Manages file storage isolation across tenants and execution sessions."""

    def __init__(self, root_dir: Optional[str] = None) -> None:
        self.root_dir = Path(root_dir or "/tmp/antigravity/workspaces")

    def get_tenant_workspace(self, tenant_id: str) -> Path:
        """Returns isolated workspace path for a specific tenant."""
        tenant_path = self.root_dir / tenant_id
        return tenant_path

    def get_session_workspace(self, tenant_id: str, session_id: str) -> Path:
        """Returns isolated workspace path for an individual execution session."""
        session_path = self.root_dir / tenant_id / "sessions" / session_id
        return session_path
