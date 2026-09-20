"""Model Capability Matching & Discovery Engine (Phase 8C)."""

from __future__ import annotations

from typing import List, Optional, Set
from app.model_governance.registry.models import Model, ModelLifecycleState
from app.model_governance.registry.repository import ModelRegistryRepository


class CapabilityMatchingEngine:
    """Discovers and filters approved models based on required capabilities and constraints."""

    def __init__(self, repository: Optional[ModelRegistryRepository] = None):
        self.repository = repository

    def find_matching_models(
        self,
        organization_id: str,
        required_capabilities: Set[str],
        max_cost_per_1k: Optional[float] = None,
        only_active: bool = True,
    ) -> List[Model]:
        """Find models meeting all capability and cost constraints."""
        if not self.repository:
            return []
        all_models = self.repository.list_models(organization_id)
        matching = []

        for model in all_models:
            if only_active and model.status != ModelLifecycleState.ACTIVE:
                continue

            # Check capabilities
            if not (required_capabilities <= model.capabilities):
                continue

            # Check cost cap
            if max_cost_per_1k is not None:
                if model.input_token_cost_per_1k > max_cost_per_1k:
                    continue

            matching.append(model)

        return matching

    def calculate_match_score(self, model: Model, required_capabilities: Set[str]) -> float:
        """Calculate proportion of required capabilities satisfied by the model."""
        if not required_capabilities:
            return 1.0
        matched = len(required_capabilities.intersection(model.capabilities))
        return round(matched / len(required_capabilities), 4)

    def filter_models_by_capabilities(
        self,
        models: List[Model],
        required_capabilities: Set[str],
    ) -> List[Model]:
        """Filter list of models to those satisfying all required capabilities."""
        return [m for m in models if required_capabilities <= m.capabilities]
