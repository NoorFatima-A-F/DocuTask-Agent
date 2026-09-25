"""
Tool Access Control Lists (ACLs) for Security Governance Layer.
Maintains granular mapping of which agent roles and identities may invoke specific tools.
"""

from __future__ import annotations

import logging
from typing import Dict, Optional, Set

from app.agents.security.agent_permission import AgentRole

logger = logging.getLogger(__name__)

# Default Tool Role Grants
DEFAULT_TOOL_PERMISSIONS: Dict[str, Set[AgentRole]] = {
    "tesseract_ocr": {AgentRole.ADMIN, AgentRole.EXTRACTOR, AgentRole.COORDINATOR},
    "pdf_plumber": {AgentRole.ADMIN, AgentRole.EXTRACTOR, AgentRole.COORDINATOR},
    "gemini_vision": {AgentRole.ADMIN, AgentRole.EXTRACTOR, AgentRole.COORDINATOR},
    "claude_opus": {AgentRole.ADMIN, AgentRole.EXTRACTOR, AgentRole.COORDINATOR},
    "regex_extractor": {AgentRole.ADMIN, AgentRole.EXTRACTOR, AgentRole.COORDINATOR},
    "rule_validator": {AgentRole.ADMIN, AgentRole.VALIDATOR, AgentRole.COORDINATOR},
    "schema_validator": {AgentRole.ADMIN, AgentRole.VALIDATOR, AgentRole.COORDINATOR},
    "audit_logger": {AgentRole.ADMIN, AgentRole.AUDITOR, AgentRole.COORDINATOR},
    "graph_mutator": {AgentRole.ADMIN, AgentRole.COORDINATOR, AgentRole.RECOVERY_SPECIALIST},
    "checkpoint_restorer": {AgentRole.ADMIN, AgentRole.COORDINATOR, AgentRole.RECOVERY_SPECIALIST},
}


class ToolAccessController:
    """Enforces tool access control lists based on calling agent's role."""

    def __init__(self, tool_grants: Optional[Dict[str, Set[AgentRole]]] = None) -> None:
        self.tool_grants = tool_grants or dict(DEFAULT_TOOL_PERMISSIONS)

    def is_tool_accessible(self, role: AgentRole, tool_name: str) -> bool:
        """Checks whether the specified role is permitted to invoke the tool."""
        # Admin is universally permitted
        if role == AgentRole.ADMIN:
            return True

        normalized_tool = tool_name.lower().strip()
        allowed_roles = self.tool_grants.get(normalized_tool)

        # If tool is not explicitly registered, allow general non-sensitive tools by default
        if allowed_roles is None:
            return True

        allowed = role in allowed_roles
        if not allowed:
            logger.warning("Access denied: Role '%s' not authorized to call tool '%s'", role.value, tool_name)
        return allowed

    def grant_tool_access(self, tool_name: str, role: AgentRole) -> None:
        """Dynamically grants access for a role to a tool."""
        normalized_tool = tool_name.lower().strip()
        if normalized_tool not in self.tool_grants:
            self.tool_grants[normalized_tool] = set()
        self.tool_grants[normalized_tool].add(role)

    def revoke_tool_access(self, tool_name: str, role: AgentRole) -> bool:
        """Revokes access for a role to a tool."""
        normalized_tool = tool_name.lower().strip()
        if normalized_tool in self.tool_grants and role in self.tool_grants[normalized_tool]:
            self.tool_grants[normalized_tool].remove(role)
            return True
        return False
