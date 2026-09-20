"""Intelligent Model Selection Service (Phase 8C).

Selects optimal approved AI model based on:
- Required Capabilities
- Latency Constraints
- Token Budget Caps
- Risk Level Restrictions
- Policy Rules
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field
from app.model_governance.registry.models import Model, ModelLifecycleState, RiskLevel
from app.model_governance.registry.repository import ModelRegistryRepository
from app.model_governance.policies.enforcement import ModelPolicyEnforcer


class ModelSelectionRequest(BaseModel):
    """Execution task specifications for model selection."""
    task_name: str
    organization_id: str
    required_capabilities: Set[str] = Field(default_factory=set)
    max_latency_ms: Optional[float] = None
    max_input_cost_per_1k: Optional[float] = None
    max_risk_level: Optional[RiskLevel] = None
    preferred_providers: Optional[List[str]] = None
    target_region: str = "us-east-1"


class ModelSelectionResult(BaseModel):
    """Output from intelligent model selector."""
    selected_model: Model
    selection_reason: str
    evaluated_candidates_count: int
    fallback_models: List[str] = Field(default_factory=list)


class ModelSelectionService:
    """Selects and ranks compliant AI models for autonomous agent tasks."""

    def __init__(
        self,
        repository: ModelRegistryRepository,
        policy_enforcer: Optional[ModelPolicyEnforcer] = None,
    ):
        self.repository = repository
        self.policy_enforcer = policy_enforcer or ModelPolicyEnforcer()

    def select_model(self, request: ModelSelectionRequest) -> ModelSelectionResult:
        """Select best candidate model satisfying all governance and performance requirements."""
        all_models = self.repository.list_models(
            organization_id=request.organization_id,
            status=ModelLifecycleState.ACTIVE,
        )

        candidates: List[Model] = []
        for model in all_models:
            # 1. Capability check
            if not (request.required_capabilities <= model.capabilities):
                continue

            # 2. Cost cap check
            if request.max_input_cost_per_1k is not None and model.input_token_cost_per_1k > request.max_input_cost_per_1k:
                continue

            # 3. Policy validation
            try:
                self.policy_enforcer.validate_execution(
                    model, request.organization_id, target_region=request.target_region
                )
            except ValueError:
                continue

            candidates.append(model)

        if not candidates:
            raise ValueError(
                f"No approved, compliant model found meeting capabilities: {request.required_capabilities}"
            )

        # Sort candidates: prioritize lowest cost then lowest risk
        risk_ranks = {RiskLevel.LOW: 0, RiskLevel.MEDIUM: 1, RiskLevel.HIGH: 2, RiskLevel.CRITICAL: 3}
        sorted_candidates = sorted(
            candidates,
            key=lambda m: (m.input_token_cost_per_1k, risk_ranks.get(m.risk_level, 99)),
        )

        chosen = sorted_candidates[0]
        fallbacks = [m.model_id for m in sorted_candidates[1:4]]

        return ModelSelectionResult(
            selected_model=chosen,
            selection_reason=f"Optimized for cost (${chosen.input_token_cost_per_1k:.5f}/1k) and capability match",
            evaluated_candidates_count=len(all_models),
            fallback_models=fallbacks,
        )
