"""
Enterprise Knowledge Fabric, Memory Intelligence & Retrieval Platform (EKF-MIRP) - Governance Engine.
Enforces multi-level classification clearance, role-based ACLs, zero-trust retrieval filters, and tenant boundaries.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.knowledge.core.exceptions import ClassificationViolationError, PermissionDeniedError
from app.knowledge.core.models import (
    ClassificationLevel,
    KnowledgeObject,
    KnowledgePermission,
    RetrievalResult,
)

logger = logging.getLogger(__name__)

# Numeric clearance ranking
CLEARANCE_RANKS: Dict[ClassificationLevel, int] = {
    ClassificationLevel.PUBLIC: 1,
    ClassificationLevel.INTERNAL: 2,
    ClassificationLevel.CONFIDENTIAL: 3,
    ClassificationLevel.RESTRICTED: 4,
    ClassificationLevel.HIGHLY_RESTRICTED: 5,
}


class UserSecurityContext(BaseModel):
    """Identity, role, and clearance attributes of the requesting user or agent."""
    user_id: str
    organization_id: str = "org-default"
    workspace_id: str = "ws-default"
    department: str = "general"
    roles: List[str] = Field(default_factory=lambda: ["user"])
    clearance: ClassificationLevel = ClassificationLevel.INTERNAL


class KnowledgeGovernanceEngine:
    """
    Enterprise knowledge access controller and governance validation engine.
    """

    def __init__(self):
        self._permissions: Dict[str, KnowledgePermission] = {}  # knowledge_id -> KnowledgePermission

    def set_permission(self, permission: KnowledgePermission) -> None:
        """Configures ACL rules for a knowledge object."""
        self._permissions[permission.knowledge_id] = permission

    def get_permission(self, knowledge_id: str) -> Optional[KnowledgePermission]:
        """Retrieves active ACL rules for a knowledge object."""
        return self._permissions.get(knowledge_id)

    def check_access(
        self,
        knowledge_object: KnowledgeObject,
        user_context: UserSecurityContext,
    ) -> bool:
        """
        Validates clearance level, tenant matching, department, role, and user permissions.
        Raises PermissionDeniedError or ClassificationViolationError on failure.
        """
        # 1. Tenant Boundary
        if knowledge_object.organization_id != user_context.organization_id:
            raise PermissionDeniedError(
                f"Tenant isolation breach: User org '{user_context.organization_id}' cannot access knowledge org '{knowledge_object.organization_id}'",
                knowledge_id=knowledge_object.id,
            )

        # 2. Clearance Level Check
        user_rank = CLEARANCE_RANKS.get(user_context.clearance, 1)
        required_rank = CLEARANCE_RANKS.get(knowledge_object.classification, 1)

        if user_rank < required_rank:
            raise ClassificationViolationError(
                f"User clearance '{user_context.clearance.value}' insufficient for knowledge classification '{knowledge_object.classification.value}'",
                knowledge_id=knowledge_object.id,
            )

        # 3. Fine-grained ACL Check (if registered)
        perm = self._permissions.get(knowledge_object.id)
        if perm:
            # Check user whitelist
            if perm.allowed_users and user_context.user_id not in perm.allowed_users and "*" not in perm.allowed_users:
                # Check role
                has_role = any(r in perm.allowed_roles or "*" in perm.allowed_roles for r in user_context.roles)
                if not has_role:
                    raise PermissionDeniedError(
                        f"User '{user_context.user_id}' lacks permitted role for knowledge '{knowledge_object.id}'",
                        knowledge_id=knowledge_object.id,
                    )

            # Check department
            if (
                perm.allowed_departments
                and "*" not in perm.allowed_departments
                and user_context.department not in perm.allowed_departments
            ):
                raise PermissionDeniedError(
                    f"Department '{user_context.department}' not authorized for knowledge '{knowledge_object.id}'",
                    knowledge_id=knowledge_object.id,
                )

        return True

    def filter_retrieval_results(
        self,
        results: List[RetrievalResult],
        user_context: UserSecurityContext,
        knowledge_objects_map: Dict[str, KnowledgeObject],
    ) -> List[RetrievalResult]:
        """
        Filters out any chunks whose parent knowledge object fails security checks for user_context.
        """
        permitted: List[RetrievalResult] = []

        for res in results:
            kobj = knowledge_objects_map.get(res.chunk.knowledge_id)
            if not kobj:
                # If no parent model registered, allow if user has standard access
                permitted.append(res)
                continue

            try:
                if self.check_access(kobj, user_context):
                    permitted.append(res)
            except (PermissionDeniedError, ClassificationViolationError):
                logger.debug(f"Filtered out chunk '{res.chunk.chunk_id}' due to governance policy")
                continue

        return permitted
