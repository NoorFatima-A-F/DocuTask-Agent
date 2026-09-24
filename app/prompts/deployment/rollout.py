"""Prompt Canary & Rollout Strategy Manager (Phase 8D).

Supports Immediate (100%), Canary (10% -> 50% -> 100%), and Traffic Splitting strategies.
"""

from __future__ import annotations

import random
from enum import Enum
from typing import Dict, Optional
from pydantic import BaseModel
from app.prompts.deployment.publisher import DeploymentEnvironment, PromptPublisher


class RolloutStrategyType(str, Enum):
    """Supported rollout strategies."""
    IMMEDIATE = "IMMEDIATE"
    CANARY = "CANARY"
    A_B_SPLIT = "A_B_SPLIT"


class CanaryStage(BaseModel):
    """Canary progression stage."""
    traffic_pct: float
    duration_hours: int = 24


class PromptRolloutManager:
    """Manages progressive deployment and traffic routing between versions."""

    def __init__(self, publisher: PromptPublisher):
        self.publisher = publisher
        # (org_id, prompt_id) -> Dict mapping version_id -> traffic_weight (0.0 to 1.0)
        self._traffic_splits: Dict[tuple[str, str], Dict[str, float]] = {}

    def set_immediate_rollout(
        self,
        prompt_id: str,
        version_id: str,
        organization_id: str,
        deployed_by: str,
    ) -> None:
        """Immediately promote version to 100% traffic."""
        self.publisher.deploy_version(
            prompt_id=prompt_id,
            version_id=version_id,
            organization_id=organization_id,
            environment=DeploymentEnvironment.PRODUCTION,
            deployed_by=deployed_by,
            traffic_percentage=100.0,
        )
        self._traffic_splits[(organization_id, prompt_id)] = {version_id: 1.0}

    def set_canary_rollout(
        self,
        prompt_id: str,
        baseline_version_id: str,
        canary_version_id: str,
        organization_id: str,
        canary_traffic_pct: float = 0.10,
    ) -> None:
        """Allocate portion of traffic to canary version."""
        baseline_pct = 1.0 - canary_traffic_pct
        self._traffic_splits[(organization_id, prompt_id)] = {
            baseline_version_id: baseline_pct,
            canary_version_id: canary_traffic_pct,
        }

    def resolve_version_for_execution(
        self,
        prompt_id: str,
        organization_id: str,
    ) -> Optional[str]:
        """Stochastically select version ID based on assigned traffic weights."""
        splits = self._traffic_splits.get((organization_id, prompt_id))
        if not splits:
            active_dep = self.publisher.get_active_deployment(prompt_id, organization_id)
            return active_dep.version_id if active_dep else None

        r = random.random()
        cumulative = 0.0
        for vid, weight in splits.items():
            cumulative += weight
            if r <= cumulative:
                return vid

        return list(splits.keys())[0]
