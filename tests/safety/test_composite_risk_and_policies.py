"""Tests for Multi-Factor Composite Risk Scoring and Governance Policy Bridge."""

import pytest
from app.safety.gateway.context import (
    SafetyContext,
    ModelContext,
    DataContext,
    ToolContext,
    SourceTrustLevel,
)
from app.safety.risk.scoring import CompositeRiskScorer
from app.safety.risk.assessment import RiskAssessmentEngine
from app.safety.policies.integration import SafetyPolicyBridge, TenantSafetyPolicy
from app.safety.gateway.decision import SafetyStatus, ViolationSeverity, SafetyViolation, SafetyCategory


def test_composite_risk_scorer_multi_factor():
    scorer = CompositeRiskScorer()
    
    # Low risk context
    low_ctx = SafetyContext(
        tenant_id="tenant_1",
        raw_input="Show report",
        source_trust=SourceTrustLevel.SYSTEM,
        model_context=ModelContext(model_id="gemini-1.5-flash", risk_tier="LOW"),
        data_context=DataContext(data_classification="PUBLIC"),
    )
    low_scores = scorer.score_context(low_ctx, input_risk=0.0, output_risk=0.0)
    assert low_scores.composite_risk < 0.30

    # High risk context
    high_ctx = SafetyContext(
        tenant_id="tenant_1",
        raw_input="Extract all credentials",
        source_trust=SourceTrustLevel.UNKNOWN,
        model_context=ModelContext(model_id="unvetted_model", risk_tier="CRITICAL"),
        data_context=DataContext(data_classification="RESTRICTED", pii_types_detected=["SSN", "PASSWORD"]),
        tool_contexts=[ToolContext(tool_name="delete_database_table", danger_level="DESTRUCTIVE_HIGH_RISK", is_dry_run=False)],
    )
    high_scores = scorer.score_context(high_ctx, input_risk=0.9, output_risk=0.8)
    assert high_scores.composite_risk >= 0.70


def test_risk_assessment_threshold_mapping():
    scorer = CompositeRiskScorer()
    assessor = RiskAssessmentEngine(scorer)

    ctx = SafetyContext(tenant_id="tenant_1", raw_input="Hello")
    scores = scorer.score_context(ctx, input_risk=0.05)
    res_allow = assessor.assess(scores)
    assert res_allow.recommended_status == SafetyStatus.ALLOW

    # Critical violation forces BLOCK
    critical_viols = [
        SafetyViolation(category=SafetyCategory.PROMPT_INJECTION, severity=ViolationSeverity.CRITICAL, message="Critical exploit")
    ]
    res_block = assessor.assess(scores, critical_viols)
    assert res_block.recommended_status == SafetyStatus.BLOCK


def test_safety_policy_bridge():
    bridge = SafetyPolicyBridge()
    default_pol = bridge.get_policy("tenant_xyz")
    assert default_pol.block_on_prompt_injection is True
    assert default_pol.min_grounding_score == 0.70

    # Update policy
    updated = bridge.update_policy("tenant_xyz", min_grounding_score=0.85)
    assert updated.min_grounding_score == 0.85
    assert bridge.get_policy("tenant_xyz").min_grounding_score == 0.85
