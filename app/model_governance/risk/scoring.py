"""Model Risk Scoring Engine (Phase 8C)."""

from __future__ import annotations

import uuid
from typing import Dict, List, Optional, Union
from app.model_governance.registry.models import Model, RiskLevel, ModelProvider, DeploymentType
from app.model_governance.risk.assessment import ModelRiskProfile


class ModelRiskScorer:
    """Calculates quantitative risk profiles for AI models."""

    def assess_risk(self, profile_or_model: Union[ModelRiskProfile, Model]) -> ModelRiskProfile:
        """Calculate or return assessed risk profile."""
        if isinstance(profile_or_model, ModelRiskProfile):
            return profile_or_model
        return self.assess_model_risk(profile_or_model)

    def assess_model_risk(
        self,
        model: Model,
        jailbreak_test_score: float = 0.05,
        explainability_score: float = 0.85,
    ) -> ModelRiskProfile:
        """Calculate composite risk score and tier."""
        # 1. Provider Trust Risk
        provider_weights = {
            ModelProvider.GOOGLE: 0.15,
            ModelProvider.GOOGLE_GEMINI: 0.15,
            ModelProvider.AZURE_OPENAI: 0.15,
            ModelProvider.AWS_BEDROCK: 0.15,
            ModelProvider.OPENAI: 0.25,
            ModelProvider.ANTHROPIC: 0.20,
            ModelProvider.ANTHROPIC_CLAUDE: 0.20,
            ModelProvider.OLLAMA: 0.10,
            ModelProvider.CUSTOM: 0.35,
        }
        provider_risk = provider_weights.get(model.provider, 0.30)

        # 2. Deployment Risk
        deploy_risk = 0.10 if model.deployment_type in (DeploymentType.ON_PREMISES, DeploymentType.VPC_PRIVATE) else 0.25

        # 3. Jailbreak Vulnerability
        jailbreak_risk = jailbreak_test_score

        # 4. Explainability limitation
        explain_risk = 1.0 - explainability_score

        composite = (
            provider_risk * 0.30
            + deploy_risk * 0.25
            + jailbreak_risk * 0.25
            + explain_risk * 0.20
        )

        if composite >= 0.70:
            level = RiskLevel.CRITICAL
        elif composite >= 0.45:
            level = RiskLevel.HIGH
        elif composite >= 0.25:
            level = RiskLevel.MEDIUM
        else:
            level = RiskLevel.LOW

        return ModelRiskProfile(
            assessment_id=f"risk_{uuid.uuid4().hex[:8]}",
            model_id=model.model_id,
            data_sensitivity_risk=deploy_risk,
            provider_trust_risk=provider_risk,
            jailbreak_vulnerability_risk=jailbreak_risk,
            explainability_limitation_risk=explain_risk,
            composite_risk_score=round(composite, 4),
            overall_risk_level=level,
            rating=level,
            mitigations=["Output Guardrails", "PII Redaction", "Audit Logging"],
        )
