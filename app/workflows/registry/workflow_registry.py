"""
Enterprise Workflow Registry.
Stores, versions, catalogs, and searches workflow definitions with lifecycle management.
"""

from copy import deepcopy
from datetime import datetime, timezone
from typing import Dict, List, Optional
from ..domain.models import WorkflowDefinition, WorkflowLifecycleState
from ..domain.exceptions import WorkflowValidationException
from ...platform.kernel.versioning import SemanticVersion


class WorkflowRegistry:
    """Central catalog and repository for all platform workflow definitions."""

    def __init__(self):
        # Key: f"{workflow_id}:{version}"
        self._definitions: Dict[str, WorkflowDefinition] = {}

    def _format_key(self, workflow_id: str, version: SemanticVersion) -> str:
        return f"{workflow_id}:{str(version)}"

    def register(self, definition: WorkflowDefinition) -> WorkflowDefinition:
        """Register a workflow definition in CREATED/REGISTERED state."""
        key = self._format_key(definition.id, definition.version)
        definition.status = WorkflowLifecycleState.REGISTERED
        definition.updated_at = datetime.now(timezone.utc)
        self._definitions[key] = definition
        return definition

    def publish(self, workflow_id: str, version: Optional[SemanticVersion] = None) -> WorkflowDefinition:
        """Publish a registered workflow definition."""
        defn = self.get(workflow_id, version)
        if not defn:
            raise WorkflowValidationException(f"Workflow '{workflow_id}' not found")
        defn.status = WorkflowLifecycleState.PUBLISHED
        defn.updated_at = datetime.now(timezone.utc)
        return defn

    def activate(self, workflow_id: str, version: Optional[SemanticVersion] = None) -> WorkflowDefinition:
        """Set a published workflow to ACTIVE for execution."""
        defn = self.get(workflow_id, version)
        if not defn:
            raise WorkflowValidationException(f"Workflow '{workflow_id}' not found")
        defn.status = WorkflowLifecycleState.ACTIVE
        defn.updated_at = datetime.now(timezone.utc)
        return defn

    def deprecate(self, workflow_id: str, version: Optional[SemanticVersion] = None) -> WorkflowDefinition:
        """Mark a workflow as DEPRECATED (no new executions, existing finish)."""
        defn = self.get(workflow_id, version)
        if not defn:
            raise WorkflowValidationException(f"Workflow '{workflow_id}' not found")
        defn.status = WorkflowLifecycleState.DEPRECATED
        defn.updated_at = datetime.now(timezone.utc)
        return defn

    def archive(self, workflow_id: str, version: Optional[SemanticVersion] = None) -> WorkflowDefinition:
        """Archive a workflow."""
        defn = self.get(workflow_id, version)
        if not defn:
            raise WorkflowValidationException(f"Workflow '{workflow_id}' not found")
        defn.status = WorkflowLifecycleState.ARCHIVED
        defn.updated_at = datetime.now(timezone.utc)
        return defn

    def clone(self, source_id: str, new_id: str, new_version: Optional[SemanticVersion] = None) -> WorkflowDefinition:
        """Clone an existing workflow definition to a new ID/version."""
        source = self.get(source_id)
        if not source:
            raise WorkflowValidationException(f"Source workflow '{source_id}' not found")

        cloned = deepcopy(source)
        cloned.id = new_id
        if new_version:
            cloned.version = new_version
        cloned.status = WorkflowLifecycleState.CREATED
        cloned.created_at = datetime.now(timezone.utc)
        cloned.updated_at = datetime.now(timezone.utc)

        return self.register(cloned)

    def get(self, workflow_id: str, version: Optional[SemanticVersion] = None) -> Optional[WorkflowDefinition]:
        """Retrieve workflow definition by ID and optional version (defaults to latest version)."""
        if version:
            return self._definitions.get(self._format_key(workflow_id, version))

        # Find latest version for workflow_id
        matching = [d for d in self._definitions.values() if d.id == workflow_id]
        if not matching:
            return None
        matching.sort(key=lambda d: d.version, reverse=True)
        return matching[0]

    def list_all(self, status: Optional[WorkflowLifecycleState] = None) -> List[WorkflowDefinition]:
        """List all workflow definitions, optionally filtered by status."""
        if status is None:
            return list(self._definitions.values())
        return [d for d in self._definitions.values() if d.status == status]

    def search(self, query: str) -> List[WorkflowDefinition]:
        """Search workflows by name, category, or tags."""
        q = query.lower()
        return [
            d for d in self._definitions.values()
            if q in d.name.lower() or q in d.category.lower() or any(q in t.lower() for t in d.tags)
        ]
