"""Model Deprecation & Sunset Management Service (Phase 8C).

Manages model deprecation schedules, sunset timelines, migration paths to replacement models,
and automated deprecation warnings for dependent workflows and agents.
"""

from __future__ import annotations

import time
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from app.model_governance.registry.models import ModelLifecycleState
from app.model_governance.registry.repository import ModelRegistryRepository
from app.model_governance.lifecycle.manager import ModelLifecycleManager


class DeprecationPlan(BaseModel):
    """Structured plan for deprecating and retiring an AI model."""
    model_id: str
    organization_id: str
    replacement_model_id: Optional[str] = None
    deprecation_date: float = Field(default_factory=time.time)
    sunset_date: float
    migration_guide_url: Optional[str] = None
    reason: str
    affected_workflows: List[str] = Field(default_factory=list)
    affected_agents: List[str] = Field(default_factory=list)


class ModelDeprecationManager:
    """Manages model sunsetting workflows and replacement migrations."""

    def __init__(
        self,
        repository: ModelRegistryRepository,
        lifecycle_manager: ModelLifecycleManager,
    ):
        self.repository = repository
        self.lifecycle_manager = lifecycle_manager
        self._plans: Dict[str, DeprecationPlan] = {}

    def schedule_deprecation(self, plan: DeprecationPlan, actor: str) -> DeprecationPlan:
        """Transitions model to DEPRECATED state and registers sunset schedule."""
        model = self.repository.get_model(plan.model_id, plan.organization_id)
        if not model:
            raise KeyError(f"Model not found: {plan.model_id}")

        # Update model replacement pointers
        model.replacement_model_id = plan.replacement_model_id
        self.repository.save_model(model)

        # Transition lifecycle state to DEPRECATED
        self.lifecycle_manager.transition(
            model_id=plan.model_id,
            target_state=ModelLifecycleState.DEPRECATED,
            actor=actor,
            reason=f"Scheduled deprecation: {plan.reason}. Sunset on {plan.sunset_date}",
            organization_id=plan.organization_id,
        )

        self._plans[plan.model_id] = plan
        return plan

    def get_deprecation_plan(self, model_id: str) -> Optional[DeprecationPlan]:
        return self._plans.get(model_id)

    def execute_sunset(self, model_id: str, organization_id: str, actor: str) -> None:
        """Executes final retirement when sunset date is reached."""
        self.lifecycle_manager.transition(
            model_id=model_id,
            target_state=ModelLifecycleState.RETIRED,
            actor=actor,
            reason="Sunset date reached. Model retired from service.",
            organization_id=organization_id,
        )
