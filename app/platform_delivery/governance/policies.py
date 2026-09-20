"""Release Freeze and Change Window Policies (Req 54)."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Set


class FreezeScope(str, Enum):
    GLOBAL_FREEZE = "GLOBAL_FREEZE"
    REGION_FREEZE = "REGION_FREEZE"
    TENANT_FREEZE = "TENANT_FREEZE"
    COMPONENT_FREEZE = "COMPONENT_FREEZE"


@dataclass
class ActiveFreeze:
    scope: FreezeScope
    target: str  # e.g. "ALL", "us-east-1", "tenant-alpha", "core-runtime"
    reason: str
    active_until: Optional[datetime] = None


class ReleaseFreezeManager:
    """Blocks deployments during active freeze windows."""

    def __init__(self):
        self._freezes: List[ActiveFreeze] = []

    def set_freeze(self, scope: FreezeScope, target: str, reason: str) -> ActiveFreeze:
        f = ActiveFreeze(scope=scope, target=target, reason=reason)
        self._freezes.append(f)
        return f

    def clear_freezes(self) -> None:
        self._freezes.clear()

    def is_deployment_frozen(self, environment: str, region: str, component: str) -> Tuple[bool, Optional[str]]:
        for f in self._freezes:
            if f.scope == FreezeScope.GLOBAL_FREEZE:
                return True, f"Global Release Freeze active: {f.reason}"
            if f.scope == FreezeScope.REGION_FREEZE and f.target == region:
                return True, f"Region {region} Freeze active: {f.reason}"
            if f.scope == FreezeScope.COMPONENT_FREEZE and f.target == component:
                return True, f"Component {component} Freeze active: {f.reason}"
        return False, None
