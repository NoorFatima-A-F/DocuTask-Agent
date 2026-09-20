"""Model Governance Policy Rules (Phase 8C)."""

from __future__ import annotations

from typing import Any, List, Optional, Set, Union
from pydantic import BaseModel, Field, model_validator
from app.model_governance.registry.models import ModelCategory, ModelProvider, RiskLevel


class ModelGovernancePolicyRule(BaseModel):
    """Governance constraints defining permitted model executions."""
    policy_id: str = "default_policy"
    rule_id: Optional[str] = None
    name: str = "Default Model Governance Rule"
    organization_id: str = "org_default"
    allowed_providers: Set[str] = Field(default_factory=lambda: {"GOOGLE", "GOOGLE_GEMINI", "OPENAI", "ANTHROPIC", "ANTHROPIC_CLAUDE", "AZURE_OPENAI", "AWS_BEDROCK", "VERTEX_AI", "COHERE", "MISTRAL", "OLLAMA", "HUGGINGFACE", "SELF_HOSTED", "CUSTOM"})
    max_risk_level: RiskLevel = RiskLevel.HIGH
    allowed_regions: Set[str] = Field(default_factory=lambda: {"us-east-1", "eu-west-1", "eu-central-1"})
    max_input_cost_per_1k: float = 0.05
    block_unapproved_models: bool = True
    enforce_human_review_for_high_risk: bool = True

    @model_validator(mode="before")
    @classmethod
    def sync_rule_and_policy(cls, values: Any) -> Any:
        if isinstance(values, dict):
            if "rule_id" in values and "policy_id" not in values:
                values["policy_id"] = values["rule_id"]
            elif "policy_id" in values and not values.get("rule_id"):
                values["rule_id"] = values["policy_id"]

            # Normalize providers to set of strings
            provs = values.get("allowed_providers")
            if provs is not None:
                norm = set()
                for p in provs:
                    if hasattr(p, "value"):
                        norm.add(p.value)
                    else:
                        norm.add(str(p))
                values["allowed_providers"] = norm

            # Normalize regions to set of strings
            regs = values.get("allowed_regions")
            if regs is not None:
                values["allowed_regions"] = set(regs)

        return values
