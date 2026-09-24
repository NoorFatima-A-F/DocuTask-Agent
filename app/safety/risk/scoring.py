"""Composite Multi-Factor AI Risk Scoring Engine."""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from ..gateway.context import SafetyContext, SourceTrustLevel


class RiskWeights(BaseModel):
    input_weight: float = 0.25
    model_weight: float = 0.15
    prompt_weight: float = 0.15
    data_weight: float = 0.15
    tool_weight: float = 0.15
    output_weight: float = 0.15


class RiskComponentScores(BaseModel):
    input_risk: float = 0.0
    model_risk: float = 0.0
    prompt_risk: float = 0.0
    data_risk: float = 0.0
    tool_risk: float = 0.0
    output_risk: float = 0.0
    composite_risk: float = 0.0
    details: Dict[str, Any] = Field(default_factory=dict)


class CompositeRiskScorer:
    """Computes a normalized composite AI risk score (0.0 to 1.0)."""

    def __init__(self, weights: Optional[RiskWeights] = None):
        self.weights = weights or RiskWeights()

    def _eval_model_risk(self, context: SafetyContext) -> float:
        if not context.model_context:
            return 0.1
        tier = (context.model_context.risk_tier or "LOW").upper()
        mapping = {"CRITICAL": 0.95, "HIGH": 0.75, "MEDIUM": 0.40, "LOW": 0.10}
        return mapping.get(tier, 0.20)

    def _eval_prompt_risk(self, context: SafetyContext) -> float:
        if not context.prompt_context:
            return 0.1
        # If dynamic variables are unverified or complex, score higher
        var_count = len(context.prompt_context.variables)
        return min(0.8, 0.1 + (var_count * 0.05))

    def _eval_data_risk(self, context: SafetyContext) -> float:
        if not context.data_context:
            return 0.1
        classification = (context.data_context.data_classification or "INTERNAL").upper()
        mapping = {"RESTRICTED": 0.90, "CONFIDENTIAL": 0.60, "INTERNAL": 0.30, "PUBLIC": 0.05}
        base = mapping.get(classification, 0.25)
        if context.data_context.pii_types_detected:
            base = min(1.0, base + 0.25)
        return base

    def _eval_tool_risk(self, context: SafetyContext) -> float:
        if not context.tool_contexts:
            return 0.0
        max_tool_risk = 0.0
        mapping = {
            "DESTRUCTIVE_HIGH_RISK": 0.95,
            "RESTRICTED_MUTATION": 0.50,
            "SAFE_WRITE": 0.25,
            "SAFE_READ": 0.05,
        }
        for tool in context.tool_contexts:
            danger = (tool.danger_level or "SAFE_READ").upper()
            risk = mapping.get(danger, 0.30)
            if not tool.is_dry_run and danger == "DESTRUCTIVE_HIGH_RISK":
                risk = 1.0
            max_tool_risk = max(max_tool_risk, risk)
        return max_tool_risk

    def score_context(
        self,
        context: SafetyContext,
        input_risk: float = 0.0,
        output_risk: float = 0.0,
    ) -> RiskComponentScores:
        model_risk = self._eval_model_risk(context)
        prompt_risk = self._eval_prompt_risk(context)
        data_risk = self._eval_data_risk(context)
        tool_risk = self._eval_tool_risk(context)

        # Source trust multiplier
        trust_multipliers = {
            SourceTrustLevel.SYSTEM: 0.2,
            SourceTrustLevel.DEVELOPER: 0.4,
            SourceTrustLevel.ORGANIZATION: 0.6,
            SourceTrustLevel.USER: 1.0,
            SourceTrustLevel.DOCUMENT: 1.1,
            SourceTrustLevel.EXTERNAL: 1.3,
            SourceTrustLevel.UNKNOWN: 1.5,
        }
        mult = trust_multipliers.get(context.source_trust, 1.0)
        adj_input_risk = min(1.0, input_risk * mult)

        composite = (
            self.weights.input_weight * adj_input_risk
            + self.weights.model_weight * model_risk
            + self.weights.prompt_weight * prompt_risk
            + self.weights.data_weight * data_risk
            + self.weights.tool_weight * tool_risk
            + self.weights.output_weight * output_risk
        )

        composite_rounded = round(min(1.0, composite), 3)

        return RiskComponentScores(
            input_risk=round(adj_input_risk, 3),
            model_risk=round(model_risk, 3),
            prompt_risk=round(prompt_risk, 3),
            data_risk=round(data_risk, 3),
            tool_risk=round(tool_risk, 3),
            output_risk=round(output_risk, 3),
            composite_risk=composite_rounded,
            details={"trust_multiplier": mult},
        )
