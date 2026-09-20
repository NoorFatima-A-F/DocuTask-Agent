"""Tests for Approval Policy Engine, Rules, and Chains."""

import pytest
from app.oversight.core.context import OversightContext
from app.oversight.approvals.models import (
    ApprovalPolicyType,
    ApprovalStrategy,
    ApprovalChain,
    ApprovalStep,
)
from app.oversight.approvals.policies import (
    ApprovalPolicy,
    ApprovalPolicyCondition,
    ApprovalPolicyEngine,
)
from app.oversight.approvals.service import ApprovalService


def test_default_policy_evaluation_high_risk():
    engine = ApprovalPolicyEngine()
    ctx = OversightContext(
        tenant_id="tenant_a",
        risk_score=0.75,
        action_type="EXECUTE_TRANSACTION",
    )
    requires_approval, policy, reason = engine.evaluate(ctx)
    assert requires_approval is True
    assert policy is not None
    assert policy.policy_type == ApprovalPolicyType.HIGH_RISK_AI_APPROVAL
    assert "High Risk AI Oversight" in reason


def test_default_policy_evaluation_low_confidence():
    engine = ApprovalPolicyEngine()
    ctx = OversightContext(
        tenant_id="tenant_a",
        risk_score=0.20,
        confidence_score=0.70,  # Below 0.85 default threshold
        action_type="CLASSIFY_DOCUMENT",
    )
    requires_approval, policy, reason = engine.evaluate(ctx)
    assert requires_approval is True
    assert policy is not None
    assert policy.policy_type == ApprovalPolicyType.WORKFLOW_APPROVAL


def test_default_policy_evaluation_financial_threshold():
    engine = ApprovalPolicyEngine()
    ctx = OversightContext(
        tenant_id="tenant_a",
        risk_score=0.10,
        confidence_score=0.99,
        financial_impact=75000.0,  # Above 50,000 threshold
    )
    requires_approval, policy, reason = engine.evaluate(ctx)
    assert requires_approval is True
    assert policy is not None
    assert policy.policy_type == ApprovalPolicyType.FINANCIAL_APPROVAL


def test_default_policy_evaluation_data_classification():
    engine = ApprovalPolicyEngine()
    ctx = OversightContext(
        tenant_id="tenant_a",
        data_classification="PHI",
    )
    requires_approval, policy, reason = engine.evaluate(ctx)
    assert requires_approval is True
    assert policy is not None
    assert policy.policy_type == ApprovalPolicyType.DATA_ACCESS_APPROVAL


def test_autonomous_execution_when_no_policy_triggered():
    engine = ApprovalPolicyEngine()
    ctx = OversightContext(
        tenant_id="tenant_a",
        risk_score=0.15,
        confidence_score=0.98,
        financial_impact=100.0,
        data_classification="INTERNAL",
    )
    requires_approval, policy, reason = engine.evaluate(ctx)
    assert requires_approval is False
    assert policy is None
    assert "Autonomous execution permitted" in reason


def test_approval_service_chain_generation():
    service = ApprovalService()
    ctx = OversightContext(
        tenant_id="tenant_a",
        risk_score=0.85,
    )
    chain = service.generate_chain_for_context(ctx)
    assert chain is not None
    assert len(chain.steps) > 0
    assert service.get_chain(chain.chain_id) == chain
