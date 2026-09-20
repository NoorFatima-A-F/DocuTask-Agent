"""Prompt Approval Policy & Gate Validators (Phase 8D)."""

from __future__ import annotations

from typing import List, Tuple
from app.prompts.registry.models import Prompt, PromptVersion, RiskLevel


class PromptApprovalGateValidator:
    """Validates if a prompt version meets all pre-conditions before production approval."""

    @staticmethod
    def validate_for_approval(
        prompt: Prompt,
        version: PromptVersion,
        min_evaluation_score: float = 0.85,
    ) -> Tuple[bool, List[str]]:
        """Validate whether version is eligible for production promotion."""
        violations: List[str] = []

        # 1. Evaluation score check
        if version.evaluation_score is not None and version.evaluation_score < min_evaluation_score:
            violations.append(
                f"Evaluation score {version.evaluation_score:.2f} is below required threshold {min_evaluation_score:.2f}"
            )

        # 2. Risk check: Critical prompts must have owner and change reason
        if prompt.risk_level in (RiskLevel.HIGH, RiskLevel.CRITICAL):
            if not version.change_reason or len(version.change_reason.strip()) < 5:
                violations.append("High/Critical risk prompts require detailed change_reason")
            if not prompt.owner:
                violations.append("High/Critical risk prompts must have a designated owner")

        # 3. Variable completeness
        if not version.prompt_template.strip():
            violations.append("Prompt template cannot be empty")

        return len(violations) == 0, violations
