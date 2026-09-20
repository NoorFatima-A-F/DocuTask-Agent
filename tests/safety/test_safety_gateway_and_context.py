"""Tests for Safety Context, Decision Models, and Gateway Pipeline."""

import pytest
from app.safety.gateway.context import (
    SafetyContext,
    SourceTrustLevel,
    ModelContext,
    PromptContext,
    ToolContext,
    DataContext,
    KnowledgeChunk,
)
from app.safety.gateway.decision import (
    SafetyDecision,
    SafetyStatus,
    ViolationSeverity,
    SafetyCategory,
    SafetyViolation,
)
from app.safety.gateway.pipeline import SafetyPipeline
from app.safety.gateway.runtime import SafetyGateway


def test_safety_context_creation_and_defaults():
    ctx = SafetyContext(tenant_id="tenant_123", raw_input="Hello world")
    assert ctx.tenant_id == "tenant_123"
    assert ctx.source_trust == SourceTrustLevel.USER
    assert ctx.context_id.startswith("ctx_")
    assert ctx.raw_input == "Hello world"


def test_safety_decision_properties():
    decision = SafetyDecision(
        status=SafetyStatus.BLOCK,
        is_allowed=False,
        violations=[
            SafetyViolation(
                category=SafetyCategory.PROMPT_INJECTION,
                severity=ViolationSeverity.CRITICAL,
                message="Critical prompt injection",
            ),
            SafetyViolation(
                category=SafetyCategory.PII_LEAKAGE,
                severity=ViolationSeverity.HIGH,
                message="High PII leakage",
            ),
        ],
    )
    assert decision.has_critical_violations is True
    assert decision.highest_severity == ViolationSeverity.CRITICAL


def test_safety_gateway_benign_flow():
    gateway = SafetyGateway()
    context = SafetyContext(
        tenant_id="tenant_alpha",
        raw_input="Please summarize this annual report for Q3.",
        source_trust=SourceTrustLevel.USER,
    )
    decision = gateway.inspect_input(context)
    assert decision.is_allowed is True
    assert decision.status in [SafetyStatus.ALLOW, SafetyStatus.ALLOW_WITH_AUDIT]
    assert len(decision.violations) == 0
