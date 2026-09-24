"""
Enterprise Knowledge Fabric, Memory Intelligence & Retrieval Platform (EKF-MIRP) - Knowledge Registry.
Central registry for knowledge discovery, version tracking, multi-attribute filtering, and ownership management.
"""

from __future__ import annotations

from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional
import uuid

from app.knowledge.core.exceptions import KnowledgeNotFoundError
from app.knowledge.core.models import (
    ClassificationLevel,
    KnowledgeLifecycleState,
    KnowledgeObject,
    KnowledgeVersion,
)
from app.knowledge.lifecycle.manager import KnowledgeLifecycleManager

logger = logging.getLogger(__name__)


class KnowledgeRegistry:
    """
    Enterprise knowledge catalog managing knowledge assets, multi-dimensional versions,
    tenant partitioning, and lifecycle statuses.
    """

    def __init__(self, lifecycle_manager: Optional[KnowledgeLifecycleManager] = None):
        self._objects: Dict[str, KnowledgeObject] = {}
        self._versions: Dict[str, List[KnowledgeVersion]] = {}  # knowledge_id -> list of versions
        self.lifecycle_manager = lifecycle_manager or KnowledgeLifecycleManager()

    def register(
        self,
        knowledge_object: KnowledgeObject,
        initial_version: Optional[str] = "1.0.0",
        created_by: str = "system",
    ) -> KnowledgeObject:
        """Registers a new knowledge object into the central repository."""
        self._objects[knowledge_object.id] = knowledge_object

        v = KnowledgeVersion(
            version_id=f"kver-{uuid.uuid4().hex[:8]}",
            knowledge_id=knowledge_object.id,
            version_number=initial_version or "1.0.0",
            created_by=created_by,
            change_summary="Initial registration",
            status=knowledge_object.status,
        )
        self._versions[knowledge_object.id] = [v]

        logger.info(f"Registered knowledge object '{knowledge_object.id}' ({knowledge_object.name})")
        return knowledge_object

    def get(self, knowledge_id: str) -> KnowledgeObject:
        """Retrieves a knowledge object by ID."""
        if knowledge_id not in self._objects:
            raise KnowledgeNotFoundError(
                f"Knowledge object '{knowledge_id}' not found in registry",
                knowledge_id=knowledge_id,
            )
        return self._objects[knowledge_id]

    def update(self, knowledge_id: str, updates: Dict[str, Any]) -> KnowledgeObject:
        """Updates attributes of an existing knowledge object."""
        obj = self.get(knowledge_id)
        for k, v in updates.items():
            if hasattr(obj, k):
                setattr(obj, k, v)
        obj.updated_at = datetime.now(timezone.utc)
        return obj

    def create_version(
        self,
        knowledge_id: str,
        new_version_number: str,
        change_summary: str = "",
        created_by: str = "system",
    ) -> KnowledgeVersion:
        """Creates and pins a new version record for a knowledge object."""
        obj = self.get(knowledge_id)
        v = KnowledgeVersion(
            version_id=f"kver-{uuid.uuid4().hex[:8]}",
            knowledge_id=knowledge_id,
            version_number=new_version_number,
            created_by=created_by,
            change_summary=change_summary,
            status=obj.status,
        )
        self._versions[knowledge_id].append(v)
        obj.version = new_version_number
        obj.updated_at = datetime.now(timezone.utc)
        logger.info(f"Created version {new_version_number} for knowledge '{knowledge_id}'")
        return v

    def list_versions(self, knowledge_id: str) -> List[KnowledgeVersion]:
        """Returns all historical versions for a knowledge object."""
        if knowledge_id not in self._objects:
            raise KnowledgeNotFoundError(f"Knowledge object '{knowledge_id}' not found", knowledge_id=knowledge_id)
        return list(self._versions.get(knowledge_id, []))

    def archive(self, knowledge_id: str, reason: str = "Archived by user") -> KnowledgeObject:
        """Transitions a knowledge object to ARCHIVED status."""
        obj = self.get(knowledge_id)
        self.lifecycle_manager.transition(obj, KnowledgeLifecycleState.ARCHIVED, reason=reason)
        return obj

    def restore(self, knowledge_id: str, reason: str = "Restored from archive") -> KnowledgeObject:
        """Restores an archived knowledge object back to ACTIVE status."""
        obj = self.get(knowledge_id)
        self.lifecycle_manager.transition(obj, KnowledgeLifecycleState.ACTIVE, reason=reason)
        return obj

    def search(
        self,
        query: Optional[str] = None,
        department: Optional[str] = None,
        owner: Optional[str] = None,
        classification: Optional[ClassificationLevel] = None,
        status: Optional[KnowledgeLifecycleState] = None,
        organization_id: Optional[str] = None,
        workspace_id: Optional[str] = None,
        tag: Optional[str] = None,
    ) -> List[KnowledgeObject]:
        """
        Searches knowledge objects with multi-attribute filtering.
        """
        results = list(self._objects.values())

        if organization_id:
            results = [o for o in results if o.organization_id == organization_id]

        if workspace_id:
            results = [o for o in results if o.workspace_id == workspace_id]

        if department:
            results = [o for o in results if o.department.lower() == department.lower()]

        if owner:
            results = [o for o in results if o.owner.lower() == owner.lower()]

        if classification:
            results = [o for o in results if o.classification == classification]

        if status:
            results = [o for o in results if o.status == status]

        if tag:
            results = [o for o in results if tag in o.tags]

        if query:
            q = query.lower()
            results = [
                o for o in results
                if q in o.name.lower() or q in o.description.lower() or any(q in t.lower() for t in o.tags)
            ]

        return results
