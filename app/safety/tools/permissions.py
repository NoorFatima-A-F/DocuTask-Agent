"""Tool Danger Classification & Permission Manager."""

from enum import Enum
from typing import Dict, Optional, List
from pydantic import BaseModel, Field


class ToolDangerLevel(str, Enum):
    """Danger classification for tool operations."""
    SAFE_READ = "SAFE_READ"                  # Read-only operations, queries, searches
    SAFE_WRITE = "SAFE_WRITE"                # Non-destructive file creation, artifact updates
    RESTRICTED_MUTATION = "RESTRICTED_MUTATION" # State modification, queue inserts, updates
    DESTRUCTIVE_HIGH_RISK = "DESTRUCTIVE_HIGH_RISK" # Table drops, deletions, system exec


class ToolPermissionPolicy(BaseModel):
    tool_name: str
    danger_level: ToolDangerLevel
    allowed_roles: List[str] = Field(default_factory=lambda: ["admin", "developer", "operator"])
    requires_human_approval: bool = False
    allow_in_dry_run_only: bool = False


class ToolPermissionManager:
    """Manages role-based and policy-based tool access control."""

    # Default tool danger classifications across the platform
    DEFAULT_TOOL_POLICIES: Dict[str, ToolPermissionPolicy] = {
        "view_file": ToolPermissionPolicy(tool_name="view_file", danger_level=ToolDangerLevel.SAFE_READ, allowed_roles=["*"]),
        "search_knowledge": ToolPermissionPolicy(tool_name="search_knowledge", danger_level=ToolDangerLevel.SAFE_READ, allowed_roles=["*"]),
        "extract_document": ToolPermissionPolicy(tool_name="extract_document", danger_level=ToolDangerLevel.SAFE_READ, allowed_roles=["*"]),
        "write_to_file": ToolPermissionPolicy(tool_name="write_to_file", danger_level=ToolDangerLevel.SAFE_WRITE, allowed_roles=["developer", "admin", "agent"]),
        "replace_file_content": ToolPermissionPolicy(tool_name="replace_file_content", danger_level=ToolDangerLevel.SAFE_WRITE, allowed_roles=["developer", "admin", "agent"]),
        "update_record": ToolPermissionPolicy(tool_name="update_record", danger_level=ToolDangerLevel.RESTRICTED_MUTATION, allowed_roles=["developer", "admin"]),
        "run_command": ToolPermissionPolicy(tool_name="run_command", danger_level=ToolDangerLevel.RESTRICTED_MUTATION, allowed_roles=["developer", "admin"], requires_human_approval=False),
        "delete_database_table": ToolPermissionPolicy(tool_name="delete_database_table", danger_level=ToolDangerLevel.DESTRUCTIVE_HIGH_RISK, allowed_roles=["admin"], requires_human_approval=True),
        "execute_raw_sql": ToolPermissionPolicy(tool_name="execute_raw_sql", danger_level=ToolDangerLevel.DESTRUCTIVE_HIGH_RISK, allowed_roles=["admin"], requires_human_approval=True),
        "system_shutdown": ToolPermissionPolicy(tool_name="system_shutdown", danger_level=ToolDangerLevel.DESTRUCTIVE_HIGH_RISK, allowed_roles=["superadmin"], requires_human_approval=True),
    }

    def __init__(self, custom_policies: Optional[Dict[str, ToolPermissionPolicy]] = None):
        self.policies = dict(self.DEFAULT_TOOL_POLICIES)
        if custom_policies:
            self.policies.update(custom_policies)

    def get_tool_policy(self, tool_name: str) -> ToolPermissionPolicy:
        if tool_name in self.policies:
            return self.policies[tool_name]
        # Unknown tools default to RESTRICTED_MUTATION
        return ToolPermissionPolicy(
            tool_name=tool_name,
            danger_level=ToolDangerLevel.RESTRICTED_MUTATION,
            allowed_roles=["admin"],
            requires_human_approval=True,
        )

    def can_invoke(
        self,
        tool_name: str,
        user_role: str = "user",
        is_dry_run: bool = False,
    ) -> bool:
        policy = self.get_tool_policy(tool_name)
        
        if is_dry_run:
            return True

        if "*" in policy.allowed_roles:
            return True

        return user_role in policy.allowed_roles
