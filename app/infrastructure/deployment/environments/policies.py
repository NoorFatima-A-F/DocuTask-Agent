"""Environment Deployment Policies and Security Gating."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class EnvironmentPolicy:
    """Governance and security policy for an environment."""
    env_id: str
    require_approvals_count: int = 0
    require_signed_artifacts: bool = True
    block_on_critical_vulnerabilities: bool = True
    min_test_coverage_percent: float = 80.0
    allowed_source_branches: List[str] = field(default_factory=lambda: ["main", "release/*"])
    enforce_network_isolation: bool = True
