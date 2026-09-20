"""Tests for Model Risk Assessment and Policy Enforcement (Phase 8C)."""

import pytest
from app.model_governance.risk.assessment import ModelRiskProfile
from app.model_governance.risk.scoring import ModelRiskScorer
from app.model_governance.policies.rules import ModelGovernancePolicyRule
from app.model_governance.policies.enforcement import ModelPolicyEnforcer
from app.model_governance.registry.models import (
    Model,
    ModelCategory,
    ModelLifecycleState,
    ModelProvider,
    RiskLevel,
)


def test_model_risk_scoring_and_rating():
    scorer = ModelRiskScorer()

    profile_low = ModelRiskProfile(
        model_id="gpt-4o",
        security_score=0.90,
        compliance_score=0.95,
        robustness_score=0.88,
        fairness_score=0.92,
    )
    res_low = scorer.assess_risk(profile_low)
    assert res_low.rating == RiskLevel.LOW

    profile_high = ModelRiskProfile(
        model_id="experimental-unvetted",
        security_score=0.30,
        compliance_score=0.20,
        robustness_score=0.40,
        fairness_score=0.35,
    )
    res_high = scorer.assess_risk(profile_high)
    assert res_high.rating in (RiskLevel.HIGH, RiskLevel.CRITICAL)


def test_policy_enforcement_blocking_unapproved_or_high_cost_models():
    enforcer = ModelPolicyEnforcer()

    # Rule: Max cost per 1k input tokens is $0.05, allowed providers OPENAI, GOOGLE
    rule = ModelGovernancePolicyRule(
        rule_id="RULE-PROD-01",
        name="Production Foundation LLM Boundary",
        max_input_cost_per_1k=0.05,
        allowed_providers=["OPENAI", "GOOGLE"],
        allowed_regions=["us-east-1", "eu-west-1"],
    )
    enforcer.add_rule(rule)

    model_valid = Model(
        model_id="gpt-4o",
        model_name="GPT-4o",
        organization_id="org_prod",
        family_id="gpt-4o",
        version="2024-08-06",
        category=ModelCategory.FOUNDATION_LLM,
        provider=ModelProvider.OPENAI,
        lifecycle_state=ModelLifecycleState.ACTIVE,
        input_token_cost_per_1k=0.0025,
        residency_regions=["us-east-1"],
    )

    # Valid model passes
    assert enforcer.validate_execution(model_valid, "org_prod", target_region="us-east-1") is True

    # Model not in ACTIVE state
    model_unapproved = model_valid.model_copy(update={"lifecycle_state": ModelLifecycleState.REGISTERED})
    with pytest.raises(ValueError, match="is not in ACTIVE state"):
        enforcer.validate_execution(model_unapproved, "org_prod")

    # Model exceeding cost boundary
    model_expensive = model_valid.model_copy(update={"input_token_cost_per_1k": 0.10})
    with pytest.raises(ValueError, match="exceeds allowed limit"):
        enforcer.validate_execution(model_expensive, "org_prod")

    # Model in unallowed region
    with pytest.raises(ValueError, match="not approved for execution in region"):
        enforcer.validate_execution(model_valid, "org_prod", target_region="ap-southeast-1")
