"""
Workflow Versioning and Migration Management.
Guarantees that active running workflow executions remain pinned to their original definition version.
"""

from typing import Dict, List, Optional
from ..domain.models import WorkflowDefinition
from ..domain.exceptions import WorkflowValidationException
from ...platform.kernel.versioning import SemanticVersion


class WorkflowVersionManager:
    """Manages version pinning and semantic compatibility across workflow definitions."""

    def __init__(self):
        # Key: execution_id -> SemanticVersion
        self._pinned_execution_versions: Dict[str, SemanticVersion] = {}

    def pin_execution_version(self, execution_id: str, version: SemanticVersion) -> None:
        """Pin a running workflow execution to its creation version."""
        self._pinned_execution_versions[execution_id] = version

    def get_execution_version(self, execution_id: str) -> Optional[SemanticVersion]:
        """Retrieve pinned version for an execution."""
        return self._pinned_execution_versions.get(execution_id)
