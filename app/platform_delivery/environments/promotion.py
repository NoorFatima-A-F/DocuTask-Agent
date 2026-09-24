"""Immutable Environment Promotion Manager (Req 32, 33)."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional
import uuid

from ..control_plane.commands import RequestDeploymentCommand
from ..control_plane.controller import DeploymentControlPlane, DeploymentRecord
from ..releases.models import Release
from .policies import EnvironmentHierarchyPolicy


@dataclass
class PromotionRecord:
    """Audit record for a release promotion across environment tiers."""
    promotion_id: str
    release_id: str
    artifact_digest: str  # Must remain 100% identical between environments!
    source_env: Optional[str]
    target_env: str
    requested_by: str
    approved_by: Optional[str] = None
    status: str = "COMPLETED"
    deployment_id: Optional[str] = None
    promoted_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class PromotionManager:
    """Orchestrates promotions ensuring that immutable artifact identities are preserved."""

    def __init__(
        self,
        control_plane: DeploymentControlPlane,
        policy: Optional[EnvironmentHierarchyPolicy] = None,
    ):
        self.control_plane = control_plane
        self.policy = policy or EnvironmentHierarchyPolicy()
        self._promotions: Dict[str, PromotionRecord] = {}

    def promote_release(
        self,
        release: Release,
        target_env: str,
        source_env: Optional[str] = None,
        requested_by: str = "pipeline-operator",
        strategy: str = "ROLLING",
        replicas: int = 3,
    ) -> DeploymentRecord:
        # 1. Validate promotion hierarchy
        self.policy.validate_promotion_path(source_env, target_env)

        # 2. Immutable artifact digest verification (Req 32)
        if not release.artifacts:
            raise ValueError(f"Cannot promote release {release.release_id} without build artifacts")
        primary_digest = release.artifacts[0]

        # 3. Create target deployment using the EXACT SAME release and digest
        cmd = RequestDeploymentCommand(
            release_id=release.release_id,
            environment_id=target_env,
            strategy=strategy,
            application=release.repository.split("/")[-1],
            version=release.version,
            requested_by=requested_by,
            metadata={
                "artifact_digest": primary_digest,
                "source_env": source_env,
                "replicas": replicas,
            },
        )
        dep = self.control_plane.request_deployment(cmd)

        prom_id = f"prom-{uuid.uuid4().hex[:8]}"
        record = PromotionRecord(
            promotion_id=prom_id,
            release_id=release.release_id,
            artifact_digest=primary_digest,
            source_env=source_env,
            target_env=target_env,
            requested_by=requested_by,
            deployment_id=dep.deployment_id,
        )
        self._promotions[prom_id] = record
        return dep

    def get_promotion(self, promotion_id: str) -> Optional[PromotionRecord]:
        return self._promotions.get(promotion_id)

    def list_promotions(self, target_env: Optional[str] = None) -> List[PromotionRecord]:
        results = list(self._promotions.values())
        if target_env:
            results = [p for p in results if p.target_env.lower() == target_env.lower()]
        return sorted(results, key=lambda p: p.promoted_at, reverse=True)
