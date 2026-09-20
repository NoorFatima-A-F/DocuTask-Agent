"""Model Registry Repository (Phase 8C)."""

from __future__ import annotations

from typing import Dict, List, Optional
from app.model_governance.registry.models import Model, ModelCategory, ModelProvider, ModelLifecycleState


class ModelRegistryRepository:
    """In-memory tenant-isolated repository for registered AI models."""

    def __init__(self):
        # org_id -> (model_id -> Model)
        self._models: Dict[str, Dict[str, Model]] = {}

    def save(self, model: Model) -> Model:
        """Store or update a model record."""
        if model.organization_id not in self._models:
            self._models[model.organization_id] = {}
        self._models[model.organization_id][model.model_id] = model
        return model

    def save_model(self, model: Model) -> Model:
        return self.save(model)

    def get_by_id(self, model_id: str, organization_id: str) -> Optional[Model]:
        """Retrieve model ensuring organization boundary."""
        return self._models.get(organization_id, {}).get(model_id)

    def get_model(self, model_id: str, organization_id: str) -> Optional[Model]:
        return self.get_by_id(model_id, organization_id)

    def list_models(
        self,
        organization_id: str,
        category: Optional[ModelCategory] = None,
        provider: Optional[ModelProvider] = None,
        status: Optional[ModelLifecycleState] = None,
    ) -> List[Model]:
        """List models matching filter constraints."""
        org_models = list(self._models.get(organization_id, {}).values())
        results = org_models

        if category:
            results = [m for m in results if m.category == category]
        if provider:
            results = [m for m in results if m.provider == provider]
        if status:
            results = [m for m in results if m.status == status]

        return results

    def delete(self, model_id: str, organization_id: str) -> bool:
        """Remove model from registry."""
        if organization_id in self._models and model_id in self._models[organization_id]:
            del self._models[organization_id][model_id]
            return True
        return False
