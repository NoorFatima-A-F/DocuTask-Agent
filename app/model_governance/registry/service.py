"""Model Registry Management Service (Phase 8C)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Set, Union
from app.model_governance.registry.models import (
    Model,
    ModelCategory,
    ModelProvider,
    ModelLifecycleState,
    ApprovalStatus,
    DeploymentType,
    RiskLevel,
)
from app.model_governance.registry.repository import ModelRegistryRepository


class ModelRegistryService:
    """Manages AI model registration, updates, catalog search, and verification."""

    def __init__(self, repository: Optional[ModelRegistryRepository] = None):
        self.repository = repository or ModelRegistryRepository()

    def register_model(
        self,
        model_or_id: Union[Model, str],
        name: Optional[str] = None,
        provider: Optional[ModelProvider] = None,
        organization_id: Optional[str] = None,
        owner_id: str = "system",
        category: ModelCategory = ModelCategory.LLM,
        version: str = "1.0.0",
        capabilities: Optional[Set[str]] = None,
        deployment_type: DeploymentType = DeploymentType.MANAGED_CLOUD,
        region: str = "us-east-1",
        risk_level: RiskLevel = RiskLevel.MEDIUM,
        context_window: int = 128000,
        input_cost_per_1k: float = 0.00015,
        output_cost_per_1k: float = 0.00060,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Model:
        """Register a new AI model into the governance registry."""
        if isinstance(model_or_id, Model):
            model = model_or_id
            self.repository.save(model)
            return model

        model = Model(
            model_id=model_or_id,
            name=name,
            provider=provider or ModelProvider.CUSTOM,
            organization_id=organization_id or "org_default",
            owner_id=owner_id,
            category=category,
            version=version,
            status=ModelLifecycleState.REGISTERED,
            approval_status=ApprovalStatus.PENDING_SUBMISSION,
            capabilities=capabilities or set(),
            deployment_type=deployment_type,
            region=region,
            risk_level=risk_level,
            context_window=context_window,
            input_token_cost_per_1k=input_cost_per_1k,
            output_token_cost_per_1k=output_cost_per_1k,
            metadata=metadata or {},
        )
        self.repository.save(model)
        return model

    def get_model(self, model_id: str, organization_id: str) -> Optional[Model]:
        """Retrieve model by ID."""
        return self.repository.get_by_id(model_id, organization_id)

    def list_models(
        self,
        organization_id: str,
        category: Optional[ModelCategory] = None,
        provider: Optional[ModelProvider] = None,
        status: Optional[ModelLifecycleState] = None,
    ) -> List[Model]:
        """List models matching criteria."""
        return self.repository.list_models(
            organization_id=organization_id,
            category=category,
            provider=provider,
            status=status,
        )
