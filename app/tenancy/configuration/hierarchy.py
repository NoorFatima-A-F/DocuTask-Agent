"""Configuration Precedence & Hierarchy Engine (ESP-MOOS).

Resolves configuration with 6-tier precedence:
Platform Defaults -> Organization Overrides -> Workspace Overrides -> Project Overrides -> Environment Overrides -> Execution Overrides.
"""

from __future__ import annotations

from typing import Any, Dict, Optional


class ConfigurationHierarchyEngine:
    """Merges and resolves hierarchical tenant configuration settings."""

    DEFAULT_PLATFORM_CONFIG: Dict[str, Any] = {
        "ai.default_model": "gemini-2.5-flash",
        "ai.temperature": 0.2,
        "ai.max_tokens": 4096,
        "security.mfa_required": False,
        "security.session_timeout_minutes": 60,
        "retention.audit_logs_days": 90,
        "retention.workflow_history_days": 30,
        "connectors.max_concurrent_calls": 50,
        "notifications.email_alerts": True,
    }

    def __init__(self, platform_defaults: Optional[Dict[str, Any]] = None):
        self.platform_defaults = platform_defaults or dict(self.DEFAULT_PLATFORM_CONFIG)

    def resolve(
        self,
        org_config: Optional[Dict[str, Any]] = None,
        workspace_config: Optional[Dict[str, Any]] = None,
        project_config: Optional[Dict[str, Any]] = None,
        environment_config: Optional[Dict[str, Any]] = None,
        execution_config: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Merge configurations in ascending order of precedence."""
        resolved = dict(self.platform_defaults)

        # 1. Organization Overrides
        if org_config:
            resolved.update(org_config)

        # 2. Workspace Overrides
        if workspace_config:
            resolved.update(workspace_config)

        # 3. Project Overrides
        if project_config:
            resolved.update(project_config)

        # 4. Environment Overrides
        if environment_config:
            resolved.update(environment_config)

        # 5. Execution Overrides
        if execution_config:
            resolved.update(execution_config)

        return resolved

    def get_value(
        self,
        key: str,
        org_config: Optional[Dict[str, Any]] = None,
        workspace_config: Optional[Dict[str, Any]] = None,
        project_config: Optional[Dict[str, Any]] = None,
        environment_config: Optional[Dict[str, Any]] = None,
        execution_config: Optional[Dict[str, Any]] = None,
        default: Any = None,
    ) -> Any:
        """Get a specific resolved configuration parameter."""
        resolved = self.resolve(
            org_config, workspace_config, project_config, environment_config, execution_config
        )
        return resolved.get(key, default)
