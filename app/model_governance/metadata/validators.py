"""Model Metadata Validators (Phase 8C)."""

from __future__ import annotations

import re
from typing import List, Tuple
from app.model_governance.metadata.schemas import ComprehensiveModelMetadata


class ModelMetadataValidator:
    """Validates completeness and integrity of model metadata before registration or approval."""

    @staticmethod
    def validate(metadata: ComprehensiveModelMetadata) -> Tuple[bool, List[str]]:
        """Validate metadata properties and return (is_valid, errors_list)."""
        errors: List[str] = []

        # Technical checks
        cw = metadata.technical.context_window_tokens or metadata.technical.context_window
        if cw <= 0:
            errors.append("Context window must be a positive integer")
        if not metadata.technical.architecture:
            errors.append("Architecture cannot be empty")
        if metadata.technical.input_token_price_usd_per_1k < 0:
            errors.append("Token price cannot be negative")

        # Business checks
        owner = metadata.business.owner_email or metadata.business.owner_user_id
        if not owner or (metadata.business.owner_email and not re.match(r"[^@]+@[^@]+\.[^@]+", metadata.business.owner_email)):
            errors.append("Valid business owner email or ID must be specified")
        if not metadata.business.business_unit:
            errors.append("Business unit must be specified")

        # Governance checks
        if not metadata.governance.data_residency_regions:
            errors.append("At least one data residency region must be specified")

        return len(errors) == 0, errors
