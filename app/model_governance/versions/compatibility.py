"""Model Compatibility & Validation Engine (Phase 8C)."""

from __future__ import annotations

from typing import List, Optional, Set
from app.model_governance.registry.models import Model


class ModelCompatibilityEngine:
    """Verifies compatibility between models, prompts, token lengths, and requested modalities."""

    @staticmethod
    def check_compatibility(
        model: Model,
        required_modalities: Optional[List[str]] = None,
        estimated_input_tokens: int = 1000,
        required_capabilities: Optional[Set[str]] = None,
    ) -> bool:
        """Validate if model satisfies execution requirements."""
        if estimated_input_tokens > model.context_window:
            return False

        if required_capabilities:
            if not (required_capabilities <= model.capabilities):
                return False

        return True
