"""
Child Workflow Manager.
Manages hierarchical parent-child workflow lifecycles, cascading cancellations, and child result propagation.
"""

from typing import Dict, List, Optional
from uuid import UUID
from pydantic import BaseModel
from app.agents.workflow.exceptions import OrphanedChildWorkflowError


class ChildWorkflowLink(BaseModel):
    """Linkage between parent and child workflow instances."""
    parent_instance_id: UUID
    child_instance_id: UUID
    node_id: str
    is_blocking: bool = True
    propagate_failure: bool = True


class ChildWorkflowManager:
    """Manages parent-child workflow instance hierarchies and cascades."""

    def __init__(self) -> None:
        self._parent_to_children: Dict[UUID, List[UUID]] = {}
        self._child_to_parent: Dict[UUID, UUID] = {}
        self._links: Dict[UUID, ChildWorkflowLink] = {}

    def register_child(
        self,
        parent_instance_id: UUID,
        child_instance_id: UUID,
        node_id: str,
        is_blocking: bool = True,
        propagate_failure: bool = True,
    ) -> ChildWorkflowLink:
        """Links a child workflow to its parent."""
        link = ChildWorkflowLink(
            parent_instance_id=parent_instance_id,
            child_instance_id=child_instance_id,
            node_id=node_id,
            is_blocking=is_blocking,
            propagate_failure=propagate_failure,
        )
        self._parent_to_children.setdefault(parent_instance_id, []).append(child_instance_id)
        self._child_to_parent[child_instance_id] = parent_instance_id
        self._links[child_instance_id] = link
        return link

    def get_parent(self, child_instance_id: UUID) -> UUID:
        """Retrieves parent instance ID or raises OrphanedChildWorkflowError."""
        if child_instance_id not in self._child_to_parent:
            raise OrphanedChildWorkflowError(
                f"Child workflow {child_instance_id} has no registered parent context.",
                workflow_id=child_instance_id,
            )
        return self._child_to_parent[child_instance_id]

    def get_children(self, parent_instance_id: UUID) -> List[UUID]:
        """Returns all child workflow IDs associated with parent."""
        return list(self._parent_to_children.get(parent_instance_id, []))

    def get_link(self, child_instance_id: UUID) -> Optional[ChildWorkflowLink]:
        """Returns the linkage metadata for a child workflow."""
        return self._links.get(child_instance_id)

    def cascade_cancellation(self, parent_instance_id: UUID) -> List[UUID]:
        """Returns list of all descendant child workflow IDs that must be cancelled."""
        descendants: List[UUID] = []
        queue = list(self.get_children(parent_instance_id))
        while queue:
            child = queue.pop(0)
            descendants.append(child)
            queue.extend(self.get_children(child))
        return descendants
