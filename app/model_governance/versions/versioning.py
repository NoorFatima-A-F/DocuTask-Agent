"""Model Versioning & Deployment Hierarchy Engine (Phase 8C).

Governs:
Model Family -> Semantic Version -> Deployment Version (e.g. Gemini -> 2.5 -> 2.5-flash-production).
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ModelDeploymentVersion(BaseModel):
    """Specific pinned deployment version of a model."""
    deployment_id: str
    model_id: str
    model_family: str  # e.g. Gemini, Claude, GPT, Mistral
    semantic_version: str  # e.g. 2.5.0
    environment_label: str  # e.g. staging, production, canary
    provider_api_version: str = "2024-05"
    configuration: Dict[str, Any] = Field(default_factory=dict)
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ModelVersioningManager:
    """Manages version hierarchies and active deployment pointers."""

    def __init__(self):
        # model_id -> List[ModelDeploymentVersion]
        self._versions: Dict[str, List[ModelDeploymentVersion]] = {}

    def register_deployment_version(
        self,
        deployment_id: str,
        model_id: str,
        model_family: str,
        semantic_version: str,
        environment_label: str = "production",
        provider_api_version: str = "2024-05",
        configuration: Optional[Dict[str, Any]] = None,
    ) -> ModelDeploymentVersion:
        """Register a new deployment version."""
        ver = ModelDeploymentVersion(
            deployment_id=deployment_id,
            model_id=model_id,
            model_family=model_family,
            semantic_version=semantic_version,
            environment_label=environment_label,
            provider_api_version=provider_api_version,
            configuration=configuration or {},
        )
        if model_id not in self._versions:
            self._versions[model_id] = []
        self._versions[model_id].append(ver)
        return ver

    def get_active_version(self, model_id: str, environment_label: str = "production") -> Optional[ModelDeploymentVersion]:
        """Get currently active deployment version for environment."""
        versions = self._versions.get(model_id, [])
        for v in reversed(versions):
            if v.environment_label == environment_label and v.is_active:
                return v
        return None
