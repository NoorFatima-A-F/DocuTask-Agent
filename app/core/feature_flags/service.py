"""
Enterprise Feature Flag Engine.
Supports Boolean flags, Org/Workspace/Env scoping, Percentage rollouts, Canary releases, and Kill switches.
"""

from dataclasses import dataclass, field
import hashlib
from typing import Any, Dict, List, Optional, Set


@dataclass
class FeatureFlagRule:
    """Evaluation rule for a feature flag."""
    flag_key: str
    default_enabled: bool = False
    enabled_orgs: Set[str] = field(default_factory=set)
    disabled_orgs: Set[str] = field(default_factory=set)
    enabled_workspaces: Set[str] = field(default_factory=set)
    disabled_workspaces: Set[str] = field(default_factory=set)
    enabled_environments: Set[str] = field(default_factory=set)
    percentage_rollout: int = 0  # 0 to 100
    kill_switch_active: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


class FeatureFlagService:
    """Central service for evaluating feature flags."""

    def __init__(self):
        self._flags: Dict[str, FeatureFlagRule] = {}

    def register_flag(
        self,
        key: str,
        default_enabled: bool = False,
        percentage_rollout: int = 0,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> FeatureFlagRule:
        """Register a new feature flag."""
        rule = FeatureFlagRule(
            flag_key=key,
            default_enabled=default_enabled,
            percentage_rollout=percentage_rollout,
            metadata=metadata or {},
        )
        self._flags[key] = rule
        return rule

    def set_kill_switch(self, key: str, active: bool = True) -> None:
        """Activate or deactivate instant kill switch."""
        if key in self._flags:
            self._flags[key].kill_switch_active = active

    def enable_for_org(self, key: str, org_id: str) -> None:
        """Explicitly enable flag for organization."""
        if key in self._flags:
            self._flags[key].enabled_orgs.add(org_id)
            self._flags[key].disabled_orgs.discard(org_id)

    def disable_for_org(self, key: str, org_id: str) -> None:
        """Explicitly disable flag for organization."""
        if key in self._flags:
            self._flags[key].disabled_orgs.add(org_id)
            self._flags[key].enabled_orgs.discard(org_id)

    def enable_for_workspace(self, key: str, workspace_id: str) -> None:
        """Explicitly enable flag for workspace."""
        if key in self._flags:
            self._flags[key].enabled_workspaces.add(workspace_id)
            self._flags[key].disabled_workspaces.discard(workspace_id)

    def disable_for_workspace(self, key: str, workspace_id: str) -> None:
        """Explicitly disable flag for workspace."""
        if key in self._flags:
            self._flags[key].disabled_workspaces.add(workspace_id)
            self._flags[key].enabled_workspaces.discard(workspace_id)

    def set_percentage(self, key: str, percentage: int) -> None:
        """Set percentage rollout (0-100)."""
        if key in self._flags:
            self._flags[key].percentage_rollout = max(0, min(100, percentage))

    def is_enabled(
        self,
        key: str,
        org_id: Optional[str] = None,
        workspace_id: Optional[str] = None,
        env: Optional[str] = None,
        entity_id: Optional[str] = None,
    ) -> bool:
        """
        Evaluate if a feature flag is enabled for the specified context.
        """
        rule = self._flags.get(key)
        if not rule:
            return False

        # 1. Kill Switch Check (Instant Disabling)
        if rule.kill_switch_active:
            return False

        # 2. Workspace Disables (Highest specificity disable)
        if workspace_id and workspace_id in rule.disabled_workspaces:
            return False

        # 3. Workspace Enables
        if workspace_id and workspace_id in rule.enabled_workspaces:
            return True

        # 4. Org Disables
        if org_id and org_id in rule.disabled_orgs:
            return False

        # 5. Org Enables
        if org_id and org_id in rule.enabled_orgs:
            return True

        # 6. Environment Checks
        if env and rule.enabled_environments and env not in rule.enabled_environments:
            return False

        # 7. Percentage Rollout (Deterministic Hash Evaluation)
        if rule.percentage_rollout > 0:
            target = entity_id or workspace_id or org_id
            if target:
                hash_input = f"{key}:{target}".encode("utf-8")
                hash_val = int(hashlib.sha256(hash_input).hexdigest()[:8], 16)
                bucket = hash_val % 100
                if bucket < rule.percentage_rollout:
                    return True

        # 8. Default fallback
        return rule.default_enabled
