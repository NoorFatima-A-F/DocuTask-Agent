"""Prompt Automated Deployment Rollback Engine (Phase 8D).

Monitors error rates and triggers automated rollback if error thresholds are exceeded.
"""

from __future__ import annotations

from app.prompts.deployment.publisher import DeploymentEnvironment, PromptPublisher
from app.prompts.versions.rollback import PromptRollbackService


class AutomatedRollbackManager:
    """Monitors deployment health and automatically executes rollbacks on degradation."""

    def __init__(
        self,
        publisher: PromptPublisher,
        rollback_service: PromptRollbackService,
        error_rate_threshold: float = 0.05,
    ):
        self.publisher = publisher
        self.rollback_service = rollback_service
        self.error_rate_threshold = error_rate_threshold

    def evaluate_and_rollback_if_degraded(
        self,
        prompt_id: str,
        current_version_id: str,
        fallback_version_id: str,
        organization_id: str,
        observed_error_rate: float,
    ) -> bool:
        """Check observed error rate and trigger immediate rollback if threshold breached."""
        if observed_error_rate > self.error_rate_threshold:
            self.rollback_service.rollback(
                prompt_id=prompt_id,
                target_version_id=fallback_version_id,
                organization_id=organization_id,
                actor="AutomatedRollbackManager",
                reason=f"Error rate {observed_error_rate:.2%} exceeded threshold {self.error_rate_threshold:.2%}",
            )
            # Re-publish fallback to Production
            self.publisher.deploy_version(
                prompt_id=prompt_id,
                version_id=fallback_version_id,
                organization_id=organization_id,
                environment=DeploymentEnvironment.PRODUCTION,
                deployed_by="AutomatedRollbackManager",
                traffic_percentage=100.0,
            )
            return True
        return False
