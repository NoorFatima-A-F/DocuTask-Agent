"""Tests for Risk Scoring, Category Breakdown, and Trend Detection."""

import pytest
from app.governance.analytics.risk.scoring import RiskCategory, RiskScoringModel
from app.governance.analytics.risk.analyzer import RiskAnalyzer
from app.governance.analytics.risk.trends import RiskTrendAnalyzer
from app.governance.analytics.warehouse.repositories import GovernanceDataWarehouseRepository
from app.governance.analytics.events.normalizers import GovernanceAnalyticsEvent, AnalyticsEventType


def test_risk_scoring_model():
    breakdown = RiskScoringModel.calculate_score(
        category=RiskCategory.SECURITY_RISK,
        impact=0.8,
        probability=0.7,
        exposure=1.0,
    )
    assert breakdown.calculated_score > 0.6
    assert breakdown.severity_level in {"HIGH", "CRITICAL"}


def test_risk_posture_and_trend_analyzer():
    repo = GovernanceDataWarehouseRepository()
    analyzer = RiskAnalyzer(repo)
    trend_analyzer = RiskTrendAnalyzer(repo)

    # Ingest repeated policy violations
    for _ in range(4):
        repo.insert_event(
            GovernanceAnalyticsEvent(
                tenant_id="tenant_risk",
                event_type=AnalyticsEventType.POLICY_VIOLATION,
                user_id="usr_risky",
                policy_id="pol_jailbreak",
                risk_score=0.85,
            )
        )

    summary = analyzer.analyze_risk_posture("tenant_risk")
    assert summary.tenant_id == "tenant_risk"
    assert summary.overall_risk_score >= 0.0

    signals = trend_analyzer.detect_trend_signals("tenant_risk")
    assert len(signals) >= 1
    assert any(s.signal_type == "REPEATED_VIOLATIONS" for s in signals)
