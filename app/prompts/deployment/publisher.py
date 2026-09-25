"""Prompt Multi-Environment Deployment Publisher (Phase 8D).

Deploys approved prompt versions across environments: Development, Testing, Staging, and Production.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Dict, Optional
from pydantic import BaseModel, Field
from app.prompts.registry.models import PromptApprovalStatus, PromptLifecycleState
from app.prompts.registry.repository import PromptRegistryRepository


class DeploymentEnvironment(str, Enum):
    """Target runtime environments."""
    DEVELOPMENT = "Development"
    TESTING = "Testing"
    STAGING = "Staging"
    PRODUCTION = "Production"


class PromptDeploymentRecord(BaseModel):
    """Immutable record of prompt deployment to an environment."""
    deployment_id: str
    prompt_id: str
    version_id: str
    environment: DeploymentEnvironment
    organization_id: str
    deployed_by: str
    traffic_percentage: float = 100.0
    deployed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PromptPublisher:
    """Manages publishing prompt versions into target operational environments."""

    def __init__(self, repository: PromptRegistryRepository):
        self.repository = repository
        # (org_id, env, prompt_id) -> PromptDeploymentRecord
        self._deployments: Dict[tuple[str, str, str], PromptDeploymentRecord] = {}

    def deploy_version(
        self,
        prompt_id: str,
        version_id: str,
        organization_id: str,
        environment: DeploymentEnvironment,
        deployed_by: str,
        traffic_percentage: float = 100.0,
    ) -> PromptDeploymentRecord:
        """Deploy prompt version to target environment."""
        prompt = self.repository.get_prompt(prompt_id, organization_id)
        if not prompt:
            raise KeyError(f"Prompt not found: {prompt_id}")

        version = self.repository.get_version(prompt_id, version_id, organization_id)
        if not version:
            raise KeyError(f"Version not found: {version_id}")

        # Production gate requires approval
        if environment == DeploymentEnvironment.PRODUCTION:
            if version.approval_status != PromptApprovalStatus.APPROVED:
                raise ValueError("Cannot deploy unapproved prompt version to Production")

        deployment_id = f"dep_{environment.value.lower()}_{prompt_id}_{version.version_number}"
        record = PromptDeploymentRecord(
            deployment_id=deployment_id,
            prompt_id=prompt_id,
            version_id=version_id,
            environment=environment,
            organization_id=organization_id,
            deployed_by=deployed_by,
            traffic_percentage=traffic_percentage,
        )

        self._deployments[(organization_id, environment.value, prompt_id)] = record

        if environment == DeploymentEnvironment.PRODUCTION:
            prompt.active_version_id = version_id
            prompt.current_version = version.version_number
            prompt.status = PromptLifecycleState.ACTIVE
            prompt.lifecycle_state = PromptLifecycleState.ACTIVE
            self.repository.save_prompt(prompt)

        return record

    def get_active_deployment(
        self,
        prompt_id: str,
        organization_id: str,
        environment: DeploymentEnvironment = DeploymentEnvironment.PRODUCTION,
    ) -> Optional[PromptDeploymentRecord]:
        """Get active deployment for prompt in environment."""
        return self._deployments.get((organization_id, environment.value, prompt_id))
