"""Plugin Capability Sandboxing and Permission Enforcement (Req 62)."""
from dataclasses import dataclass, field
from typing import List, Set


@dataclass
class PluginSandboxPolicy:
    allowed_permissions: Set[str] = field(default_factory=lambda: {"storage:read", "telemetry:emit", "artifacts:verify"})
    max_memory_mb: int = 512
    allow_network: bool = False
    allow_raw_secrets: bool = False


class PluginSandbox:
    """Validates that a plugin does not exceed its declared sandbox permissions."""

    def __init__(self, policy: Optional[PluginSandboxPolicy] = None):
        self.policy = policy or PluginSandboxPolicy()

    def check_permissions(self, requested_permissions: List[str]) -> bool:
        for perm in requested_permissions:
            if perm not in self.policy.allowed_permissions:
                return False
        return True
