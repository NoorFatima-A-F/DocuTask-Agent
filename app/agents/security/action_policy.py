"""
Action Policy and Prohibited Action Matrix for Security Governance Layer.
Explicitly forbids dangerous operations, resource tampering, and privilege escalation.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set

from app.agents.security.agent_permission import AgentPermission, AgentRole, ROLE_PERMISSION_MATRIX

logger = logging.getLogger(__name__)


@dataclass
class ActionAuthResult:
    """Outcome of action authorization check."""

    allowed: bool
    reason: str = ""
    violating_permission: Optional[AgentPermission] = None


class ActionPolicy:
    """Validates requested actions against the RBAC permissions matrix and explicit prohibition rules."""

    def __init__(self, permission_matrix: Optional[Dict[AgentRole, Set[AgentPermission]]] = None) -> None:
        self.matrix = permission_matrix or ROLE_PERMISSION_MATRIX

    def is_action_allowed(
        self,
        role: AgentRole,
        permission: AgentPermission,
        target_resource: str = "",
    ) -> ActionAuthResult:
        """Determines if the agent role possesses the necessary permission for target resource."""
        granted = self.matrix.get(role, set())

        # 1. Base RBAC Check
        if permission not in granted:
            msg = f"Role '{role.value}' lacks required permission '{permission.value}' for resource '{target_resource}'."
            logger.warning("Security denial: %s", msg)
            return ActionAuthResult(allowed=False, reason=msg, violating_permission=permission)

        # 2. Explicit Constraint: Only ADMIN may delete raw documents
        if permission == AgentPermission.DELETE_DATA and role != AgentRole.ADMIN:
            msg = f"Operation '{permission.value}' restricted exclusively to ADMIN role."
            logger.warning("Security denial: %s", msg)
            return ActionAuthResult(allowed=False, reason=msg, violating_permission=permission)

        # 3. Explicit Constraint: Extractor agents cannot directly mutate graph topology
        if permission == AgentPermission.MUTATE_GRAPH and role == AgentRole.EXTRACTOR:
            msg = "EXTRACTOR agents are forbidden from mutating execution graph topology."
            logger.warning("Security denial: %s", msg)
            return ActionAuthResult(allowed=False, reason=msg, violating_permission=permission)

        return ActionAuthResult(allowed=True, reason="Operation authorized.")
