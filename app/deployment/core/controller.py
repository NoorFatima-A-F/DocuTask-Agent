"""Deployment Controller Control Plane."""
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from .deployment import Deployment, DeploymentStrategyType
from .exceptions import DeploymentException, ReleaseException
from .lifecycle import DeploymentStatus
from .release import Release, ReleaseStatus


class DeploymentController:
    """Central control plane for managing releases and deployment lifecycles."""

    def __init__(self):
        self._releases: Dict[str, Release] = {}
        self._deployments: Dict[str, Deployment] = {}
        self._active_deployments: Dict[str, str] = {}  # environment -> deployment_id

    def create_release(
        self,
        version: str,
        name: str,
        commit_sha: str,
        artifact_ids: Optional[List[str]] = None,
        changelog: str = "",
        created_by: str = "system",
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Release:
        """Creates and registers a new release package."""
        # Validate unique version
        for rel in self._releases.values():
            if rel.version == version:
                raise ReleaseException(f"Release version '{version}' already exists (ID: {rel.release_id})")

        release = Release(
            version=version,
            name=name,
            commit_sha=commit_sha,
            artifact_ids=artifact_ids or [],
            changelog=changelog,
            created_by=created_by,
            tags=tags or [],
            metadata=metadata or {},
        )
        self._releases[release.release_id] = release
        return release

    def get_release(self, release_id: str) -> Optional[Release]:
        """Fetches release by ID."""
        return self._releases.get(release_id)

    def get_release_by_version(self, version: str) -> Optional[Release]:
        """Fetches release by semantic version."""
        for rel in self._releases.values():
            if rel.version == version:
                return rel
        return None

    def list_releases(
        self,
        status: Optional[ReleaseStatus] = None,
        tag: Optional[str] = None,
    ) -> List[Release]:
        """Lists registered releases filtered by status or tag."""
        releases = list(self._releases.values())
        if status:
            releases = [r for r in releases if r.status == status]
        if tag:
            releases = [r for r in releases if tag in r.tags]
        return sorted(releases, key=lambda r: r.created_at, reverse=True)

    def publish_release(self, release_id: str) -> Release:
        """Publishes a release for deployment."""
        release = self.get_release(release_id)
        if not release:
            raise ReleaseException(f"Release '{release_id}' not found")
        release.publish()
        return release

    def create_deployment(
        self,
        release_id: str,
        target_environment: str,
        strategy: DeploymentStrategyType = DeploymentStrategyType.ROLLING,
        replicas: int = 3,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Deployment:
        """Creates and initializes a new deployment for a given release."""
        release = self.get_release(release_id)
        if not release:
            raise DeploymentException(f"Cannot deploy non-existent release '{release_id}'")
        if release.status != ReleaseStatus.PUBLISHED:
            raise DeploymentException(
                f"Release '{release_id}' is in state {release.status.value}, must be PUBLISHED to deploy"
            )

        deployment = Deployment(
            release_id=release_id,
            target_environment=target_environment.lower(),
            strategy=strategy,
            replicas=replicas,
            metadata=metadata or {},
        )
        self._deployments[deployment.deployment_id] = deployment
        return deployment

    def get_deployment(self, deployment_id: str) -> Optional[Deployment]:
        """Fetches deployment by ID."""
        return self._deployments.get(deployment_id)

    def list_deployments(
        self,
        environment: Optional[str] = None,
        status: Optional[DeploymentStatus] = None,
    ) -> List[Deployment]:
        """Lists deployments filtered by environment and/or status."""
        deployments = list(self._deployments.values())
        if environment:
            deployments = [d for d in deployments if d.target_environment == environment.lower()]
        if status:
            deployments = [d for d in deployments if d.status == status]
        return sorted(deployments, key=lambda d: d.started_at, reverse=True)

    def get_active_deployment(self, environment: str) -> Optional[Deployment]:
        """Returns the currently active deployment for the given environment."""
        dep_id = self._active_deployments.get(environment.lower())
        if dep_id:
            return self._deployments.get(dep_id)
        return None

    def execute_deployment(
        self,
        deployment_id: str,
        auto_rollback_on_failure: bool = True,
    ) -> Deployment:
        """Executes a deployment through validation, preparation, rollout, and verification."""
        deployment = self.get_deployment(deployment_id)
        if not deployment:
            raise DeploymentException(f"Deployment '{deployment_id}' not found")

        try:
            # 1. Validating
            deployment.transition_to(DeploymentStatus.VALIDATING, reason="Validating pre-deployment criteria")
            
            # 2. Preparing
            deployment.transition_to(DeploymentStatus.PREPARING, reason="Allocating target cluster resources")
            
            # 3. Deploying
            deployment.transition_to(DeploymentStatus.DEPLOYING, reason=f"Rolling out with strategy {deployment.strategy.value}")
            deployment.traffic_weight = 1.0

            # 4. Verifying
            deployment.transition_to(DeploymentStatus.VERIFYING, reason="Executing post-rollout health verifications")

            # 5. Active
            # Decommission previously active deployment if present
            env = deployment.target_environment
            prev_active_id = self._active_deployments.get(env)
            if prev_active_id and prev_active_id != deployment_id:
                prev_dep = self._deployments.get(prev_active_id)
                if prev_dep and prev_dep.status == DeploymentStatus.ACTIVE:
                    prev_dep.transition_to(
                        DeploymentStatus.DECOMMISSIONED,
                        reason=f"Superceded by deployment {deployment_id}",
                    )

            deployment.transition_to(DeploymentStatus.ACTIVE, reason="Deployment verified and active")
            self._active_deployments[env] = deployment_id

        except Exception as exc:
            deployment.mark_failed(str(exc))
            if auto_rollback_on_failure:
                # If there was a previously active deployment, mark rollback target
                prev_active_id = self._active_deployments.get(deployment.target_environment)
                if prev_active_id and prev_active_id != deployment_id:
                    deployment.mark_rolled_back(prev_active_id, reason=f"Auto-rollback after failure: {exc}")
            raise DeploymentException(f"Deployment execution failed: {exc}") from exc

        return deployment

    def rollback_deployment(
        self,
        deployment_id: str,
        target_release_id: Optional[str] = None,
        reason: str = "Manual operator rollback",
    ) -> Deployment:
        """Rolls back an active or failed deployment."""
        deployment = self.get_deployment(deployment_id)
        if not deployment:
            raise DeploymentException(f"Deployment '{deployment_id}' not found")

        env = deployment.target_environment
        # Determine target release
        target_rel_id = target_release_id
        if not target_rel_id:
            # Find the most recent active deployment before this one
            past_deployments = [
                d for d in self.list_deployments(environment=env)
                if d.deployment_id != deployment_id and d.status in {DeploymentStatus.ACTIVE, DeploymentStatus.DECOMMISSIONED}
            ]
            if past_deployments:
                target_rel_id = past_deployments[0].release_id
            else:
                target_rel_id = "rel-baseline"

        deployment.mark_rolled_back(target_release_id=target_rel_id, reason=reason)
        
        # Remove from active if it was active
        if self._active_deployments.get(env) == deployment_id:
            del self._active_deployments[env]

        return deployment
