"""Environment Promotion Manager and Promotion Gate Verification."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional
import threading

from .manager import EnvironmentManager
from .policies import EnvironmentPolicy
from ..artifacts.registry import ArtifactRegistry, ArtifactMetadata


@dataclass
class PromotionChecklist:
    """Audit verification checklist for promoting a release across environments."""
    from_env: str
    to_env: str
    release_id: str
    artifact_signed: bool = False
    vulnerability_scan_passed: bool = False
    tests_passed: bool = False
    approvals_obtained: int = 0
    approved_by: List[str] = field(default_factory=list)
    promoted_at: Optional[datetime] = None

    @property
    def is_eligible(self) -> bool:
        """Check if all requirements are satisfied."""
        return self.artifact_signed and self.vulnerability_scan_passed and self.tests_passed


class EnvironmentPromotionManager:
    """Orchestrates stage-by-stage environment promotion (Dev -> Test -> Staging -> Prod)."""

    PROMOTION_PIPELINE = ["dev", "test", "staging", "prod"]

    def __init__(
        self,
        env_manager: Optional[EnvironmentManager] = None,
        artifact_registry: Optional[ArtifactRegistry] = None,
    ) -> None:
        self.env_manager = env_manager or EnvironmentManager()
        self.artifact_registry = artifact_registry or ArtifactRegistry()
        self._policies: Dict[str, EnvironmentPolicy] = {
            "dev": EnvironmentPolicy("dev", require_approvals_count=0, block_on_critical_vulnerabilities=False),
            "test": EnvironmentPolicy("test", require_approvals_count=0),
            "staging": EnvironmentPolicy("staging", require_approvals_count=1),
            "prod": EnvironmentPolicy("prod", require_approvals_count=2, block_on_critical_vulnerabilities=True),
        }
        self._checklists: List[PromotionChecklist] = []
        self._lock = threading.RLock()

    def evaluate_promotion(
        self,
        from_env: str,
        to_env: str,
        release_id: str,
        artifact: ArtifactMetadata,
        tests_passed: bool = True,
        approvers: Optional[List[str]] = None,
    ) -> PromotionChecklist:
        """Evaluate if an artifact can be promoted to the target environment."""
        policy = self._policies.get(to_env, EnvironmentPolicy(to_env))
        approvers = approvers or []

        checklist = PromotionChecklist(
            from_env=from_env,
            to_env=to_env,
            release_id=release_id,
            artifact_signed=artifact.signature is not None,
            vulnerability_scan_passed=not artifact.has_critical_vulnerabilities if policy.block_on_critical_vulnerabilities else True,
            tests_passed=tests_passed,
            approvals_obtained=len(approvers),
            approved_by=approvers,
        )

        if len(approvers) < policy.require_approvals_count:
            checklist.tests_passed = False  # Mark ineligible due to missing required approvals

        if checklist.is_eligible and len(approvers) >= policy.require_approvals_count:
            checklist.promoted_at = datetime.now(timezone.utc)
            # Promote artifact tier in registry
            if to_env in ("staging", "prod"):
                self.artifact_registry.promote_artifact(artifact.artifact_id, target_tier=to_env)

        with self._lock:
            self._checklists.append(checklist)

        return checklist
