"""Tests for Governance Analytics Event Canonical Schema, Normalizers, and Processors."""

import pytest
from app.governance.analytics.events.normalizers import (
    AnalyticsEventType,
    GovernanceAnalyticsEvent,
    EventNormalizer,
)
from app.governance.analytics.events.processors import EventProcessor
from app.governance.analytics.events.consumer import GovernanceEventConsumer


def test_governance_analytics_event_creation():
    ev = GovernanceAnalyticsEvent(
        tenant_id="tenant_alpha",
        event_type=AnalyticsEventType.GOVERNANCE_DECISION_CREATED,
        entity_id="doc_inv_100",
        risk_score=0.45,
        latency_ms=120.5,
        is_success=True,
    )
    assert ev.event_id.startswith("gev_")
    assert ev.tenant_id == "tenant_alpha"
    assert ev.event_type == AnalyticsEventType.GOVERNANCE_DECISION_CREATED
    assert ev.risk_score == 0.45


def test_event_normalizer_from_raw_dict():
    raw = {
        "event_type": "PolicyViolation",
        "tenant_id": "tenant_beta",
        "policy_id": "pol_pii_check",
        "risk_score": 85.0,  # 0-100 scale raw input
        "severity": "CRITICAL",
        "actor_id": "usr_john",
    }
    normalized = EventNormalizer.normalize_dict(raw)
    assert normalized.event_type == AnalyticsEventType.POLICY_VIOLATION
    assert normalized.tenant_id == "tenant_beta"
    assert normalized.policy_id == "pol_pii_check"
    assert normalized.user_id == "usr_john"
    assert normalized.severity == "CRITICAL"


def test_event_processor_risk_normalization():
    proc = EventProcessor()
    ev = GovernanceAnalyticsEvent(
        tenant_id="tenant_gamma",
        event_type=AnalyticsEventType.RISK_DETECTED,
        risk_score=85.0,  # Needs scale normalization to 0.85
    )
    processed = proc.process(ev)
    assert processed.risk_score == 0.85
    assert processed.risk_level == "CRITICAL"


def test_governance_event_consumer_ingestion():
    consumer = GovernanceEventConsumer()
    received = []
    consumer.subscribe(lambda e: received.append(e))

    ev1 = consumer.ingest({
        "event_type": "ModelInvocation",
        "tenant_id": "tenant_1",
        "model_id": "gemini-1.5-pro",
        "cost_usd": 0.005,
    })

    assert len(received) == 1
    assert received[0].model_id == "gemini-1.5-pro"
    assert len(consumer.get_events("tenant_1")) == 1
