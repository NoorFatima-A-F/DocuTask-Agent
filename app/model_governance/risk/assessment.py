"""Model Risk Assessment Models (Phase 8C)."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, List, Optional
from pydantic import BaseModel, Field, model_validator
from app.model_governance.registry.models import RiskLevel


class ModelRiskProfile(BaseModel):
    """Risk evaluation profile for an AI model."""
    assessment_id: str = Field(default_factory=lambda: f"risk_{uuid.uuid4().hex[:8]}")
    model_id: str = "default_model"
    security_score: Optional[float] = None
    compliance_score: Optional[float] = None
    robustness_score: Optional[float] = None
    fairness_score: Optional[float] = None
    data_sensitivity_risk: float = 0.20
    provider_trust_risk: float = 0.20
    jailbreak_vulnerability_risk: float = 0.05
    explainability_limitation_risk: float = 0.15
    composite_risk_score: float = 0.20
    overall_risk_level: RiskLevel = RiskLevel.MEDIUM
    rating: Optional[RiskLevel] = None
    mitigations: List[str] = Field(default_factory=lambda: ["Output Guardrails", "PII Redaction"])
    assessed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @model_validator(mode="before")
    @classmethod
    def sync_risk_fields(cls, values: Any) -> Any:
        if isinstance(values, dict):
            if "rating" in values and not values.get("overall_risk_level"):
                values["overall_risk_level"] = values["rating"]
            elif "overall_risk_level" in values and not values.get("rating"):
                values["rating"] = values["overall_risk_level"]

            # If scores are given, derive risk metrics
            sec = values.get("security_score")
            comp = values.get("compliance_score")
            rob = values.get("robustness_score")
            fair = values.get("fairness_score")
            if sec is not None and comp is not None:
                jailbreak = 1.0 - sec
                provider = 1.0 - comp
                explain = 1.0 - (rob or 0.8)
                data_sens = 1.0 - (fair or 0.8)
                composite = (provider * 0.30 + data_sens * 0.25 + jailbreak * 0.25 + explain * 0.20)
                values["jailbreak_vulnerability_risk"] = jailbreak
                values["provider_trust_risk"] = provider
                values["explainability_limitation_risk"] = explain
                values["data_sensitivity_risk"] = data_sens
                values["composite_risk_score"] = round(composite, 4)

                if composite >= 0.70:
                    level = RiskLevel.CRITICAL
                elif composite >= 0.45:
                    level = RiskLevel.HIGH
                elif composite >= 0.25:
                    level = RiskLevel.MEDIUM
                else:
                    level = RiskLevel.LOW
                values["overall_risk_level"] = level
                values["rating"] = level

        return values
