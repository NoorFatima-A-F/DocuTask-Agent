"""
Security Guardian Interceptor for Security Governance Layer.
Central runtime security gate validating all agent actions, data access, and tool executions.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import List, Optional

from app.agents.security.action_policy import ActionAuthResult, ActionPolicy
from app.agents.security.agent_permission import AgentPermission, AgentRole
from app.agents.security.tool_access_control import ToolAccessController

logger = logging.getLogger(__name__)


@dataclass
class SecurityAuditLog:
    """Security verification trace entry."""

    agent_id: str
    role: str
    action: str
    target_resource: str
    granted: bool
    reason: str


class SecurityGuardian:
    """Central guardian intercepting and authorizing all platform actions."""

    def __init__(
        self,
        action_policy: Optional[ActionPolicy] = None,
        tool_controller: Optional[ToolAccessController] = None,
    ) -> None:
        self.action_policy = action_policy or ActionPolicy()
        self.tool_controller = tool_controller or ToolAccessController()
        self._audit_log: List[SecurityAuditLog] = []

    def verify_action(
        self,
        agent_id: str,
        role: AgentRole,
        permission: AgentPermission,
        target_resource: str = "",
    ) -> ActionAuthResult:
        """Validates whether an agent has authorization to perform an action."""
        result = self.action_policy.is_action_allowed(
            role=role,
            permission=permission,
            target_resource=target_resource,
        )
        self._audit_log.append(
            SecurityAuditLog(
                agent_id=agent_id,
                role=role.value,
                action=permission.value,
                target_resource=target_resource,
                granted=result.allowed,
                reason=result.reason,
            )
        )
        return result

    def verify_tool_invocation(
        self,
        agent_id: str,
        role: AgentRole,
        tool_name: str,
    ) -> bool:
        """Validates whether an agent has access to invoke a specific tool."""
        # 1. Must possess base INVOKE_TOOL permission
        action_check = self.verify_action(
            agent_id=agent_id,
            role=role,
            permission=AgentPermission.INVOKE_TOOL,
            target_resource=tool_name,
        )
        if not action_check.allowed:
            return False

        # 2. Must be granted tool in ACL
        allowed = self.tool_controller.is_tool_accessible(role=role, tool_name=tool_name)
        if not allowed:
            self._audit_log.append(
                SecurityAuditLog(
                    agent_id=agent_id,
                    role=role.value,
                    action="INVOKE_TOOL_ACL",
                    target_resource=tool_name,
                    granted=False,
                    reason=f"ACL forbids role '{role.value}' from invoking '{tool_name}'",
                )
            )
        return allowed

    def get_audit_trail(self) -> List[SecurityAuditLog]:
        return list(self._audit_log)
