"""
Phase 3H.9: Comprehensive Test Suite for Enterprise Operational Intelligence Verification
"""
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.platform_verification.operational_intelligence.domain.models import (
    AnomalySeverity,
    RecommendationPriority,
    IntelligenceCertificationTier,
)
from app.platform_verification.operational_intelligence.verifiers import (
    TelemetryCorrelationVerifier,
    OperationalAnalyticsVerifier,
    AnomalyDetectionVerifier,
    TrendAnalysisVerifier,
    CapacityForecastVerifier,
    RecommendationEngineVerifier,
    ExecutiveDashboardVerifier,
    DecisionSupportVerifier,
    ContinuousInsightVerifier,
)
from app.platform_verification.operational_intelligence.scoring import OperationalIntelligenceScorer
from app.platform_verification.operational_intelligence.runtime import OperationalIntelligenceRuntime
from app.platform_verification.operational_intelligence.api import router


@pytest.fixture
def api_client():
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


def test_telemetry_correlation_verification():
    verifier = TelemetryCorrelationVerifier()
    report = verifier.verify_telemetry_correlation()

    assert report.total_correlated_events == 4
    assert report.correlation_pipeline_healthy is True
    assert len(report.services_covered) >= 5

    for event in report.sample_events:
        assert len(event.trace_id) > 0
        assert len(event.span_id) > 0
        assert event.health_status == "HEALTHY"
        assert event.slo_status == "IN_COMPLIANCE"
        assert event.correlation_confidence_pct == 100.0


def test_operational_analytics_verification():
    verifier = OperationalAnalyticsVerifier()
    report = verifier.verify_operational_analytics()

    assert report.analytics_coverage_complete is True
    assert report.total_requests_analyzed >= 100000
    assert len(report.subsystem_analytics) >= 4

    for sub in report.subsystem_analytics:
        assert sub.p50_latency_ms < sub.p95_latency_ms <= sub.p99_latency_ms
        assert sub.throughput_rps > 0
        assert sub.worker_efficiency_pct > 90.0
        assert sub.error_rate_pct < 0.1


def test_anomaly_detection_verification():
    verifier = AnomalyDetectionVerifier()
    report = verifier.verify_anomaly_detection()

    assert report.anomaly_engine_active is True
    assert report.accuracy_rate_pct >= 99.0
    assert report.false_positive_rate_pct < 1.0
    assert report.mean_time_to_detect_seconds < 5.0

    severities = [f.severity for f in report.findings]
    assert AnomalySeverity.WARNING in severities
    assert AnomalySeverity.INFORMATIONAL in severities

    for finding in report.findings:
        assert finding.deviation_sigma > 2.0
        assert finding.is_false_positive is False
        assert len(finding.root_cause_hint) > 0


def test_trend_analysis_verification():
    verifier = TrendAnalysisVerifier()
    report = verifier.verify_trend_analysis()

    assert report.platform_trajectory_healthy is True
    assert report.evaluated_trends_count >= 4

    directions = [t.historical_direction for t in report.trajectories]
    assert "IMPROVING" in directions

    for traj in report.trajectories:
        assert len(traj.summary) > 0


def test_capacity_forecasting_verification():
    verifier = CapacityForecastVerifier()
    report = verifier.verify_capacity_forecasting()

    assert report.capacity_exhaustion_risk == "VERY_LOW"
    assert len(report.forecasts) >= 4
    assert len(report.horizons_evaluated) == 3

    for fc in report.forecasts:
        assert fc.current_utilization_pct <= fc.forecast_7d_utilization_pct <= fc.forecast_30d_utilization_pct <= fc.forecast_90d_utilization_pct
        assert fc.forecast_90d_utilization_pct < 85.0  # Safe within 90-day headroom
        assert fc.saturation_risk_horizon == "NONE_IN_90_DAYS"


def test_recommendation_engine_verification():
    verifier = RecommendationEngineVerifier()
    report = verifier.verify_recommendation_engine()

    assert report.recommendations_validated is True
    assert report.total_recommendations >= 3

    for rec in report.recommendations:
        assert len(rec.reasoning) > 0
        assert len(rec.expected_benefit) > 0
        assert rec.implementation_complexity in ["LOW", "MEDIUM", "HIGH"]
        assert rec.priority in [RecommendationPriority.HIGH, RecommendationPriority.MEDIUM, RecommendationPriority.LOW]


def test_executive_dashboard_generation():
    verifier = ExecutiveDashboardVerifier()
    report = verifier.generate_executive_dashboard()

    assert report.overall_platform_health == "OPTIMAL"
    assert report.executive_signoff_ready is True
    assert len(report.kpis) >= 5

    for kpi in report.kpis:
        assert kpi.health_status == "EXCELLENT"


def test_decision_support_verification():
    verifier = DecisionSupportVerifier()
    report = verifier.verify_decision_support()

    assert report.decision_support_confidence_pct >= 95.0
    assert report.total_inquiries_resolved >= 3

    for inq in report.inquiries:
        assert len(inq.evidence_telemetry) >= 2
        assert inq.confidence_level_pct >= 95.0
        assert len(inq.recommended_decision) > 0
        assert len(inq.projected_impact) > 0


def test_continuous_insight_verification():
    verifier = ContinuousInsightVerifier()
    report = verifier.verify_continuous_insights()

    assert report.continuous_insight_pipeline_active is True
    assert report.streams_audited_count >= 4

    for st in report.streams:
        assert st.is_fresh is True
        assert len(st.refresh_cadence) > 0


def test_operational_intelligence_scorer():
    corr = TelemetryCorrelationVerifier().verify_telemetry_correlation()
    analytics = OperationalAnalyticsVerifier().verify_operational_analytics()
    anomaly = AnomalyDetectionVerifier().verify_anomaly_detection()
    trend = TrendAnalysisVerifier().verify_trend_analysis()
    forecast = CapacityForecastVerifier().verify_capacity_forecasting()
    recom = RecommendationEngineVerifier().verify_recommendation_engine()
    dash = ExecutiveDashboardVerifier().generate_executive_dashboard()
    decision = DecisionSupportVerifier().verify_decision_support()
    insight = ContinuousInsightVerifier().verify_continuous_insights()

    scorer = OperationalIntelligenceScorer()
    scorecard = scorer.calculate_scorecard(
        corr_report=corr,
        analytics_report=analytics,
        anomaly_report=anomaly,
        trend_report=trend,
        forecast_report=forecast,
        recom_report=recom,
        dash_report=dash,
        decision_report=decision,
        insight_report=insight,
    )

    assert scorecard.overall_intelligence_score >= 98.0
    assert scorecard.certification_tier == IntelligenceCertificationTier.ENTERPRISE_OPERATIONAL_INTELLIGENCE_CERTIFIED
    assert scorecard.passed is True
    assert len(scorecard.pillar_scores) == 7
    assert scorecard.anomaly_detection_accuracy_pct >= 99.0
    assert scorecard.decision_confidence_pct >= 95.0


def test_evidence_exporter_and_signatures(tmp_path):
    runtime = OperationalIntelligenceRuntime(output_dir=tmp_path)
    result = runtime.run_full_verification(export_evidence=True)
    meta = result["export_metadata"]

    assert meta is not None
    assert meta["total_reports_exported"] == 10
    assert meta["overall_intelligence_score"] >= 98.0
    assert meta["status"] == "PASSED"

    expected_files = [
        "telemetry_correlation_report.json",
        "operational_analytics_report.json",
        "anomaly_detection_report.json",
        "trend_analysis_report.json",
        "capacity_forecast_report.json",
        "recommendation_engine_report.json",
        "executive_dashboard_report.json",
        "decision_support_report.json",
        "continuous_insight_report.json",
        "operational_intelligence_certification_report.json",
        "metadata.json",
    ]

    for f in expected_files:
        p = tmp_path / f
        assert p.exists()
        assert p.stat().st_size > 0


def test_fastapi_endpoints(api_client):
    # GET /health
    resp = api_client.get("/api/v1/platform-verification/operational-intelligence/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "HEALTHY"

    # GET /anomalies
    resp = api_client.get("/api/v1/platform-verification/operational-intelligence/anomalies")
    assert resp.status_code == 200
    assert resp.json()["total_anomalies_detected"] == 4

    # GET /forecasts
    resp = api_client.get("/api/v1/platform-verification/operational-intelligence/forecasts")
    assert resp.status_code == 200
    assert len(resp.json()["forecasts"]) == 5

    # GET /recommendations
    resp = api_client.get("/api/v1/platform-verification/operational-intelligence/recommendations")
    assert resp.status_code == 200
    assert resp.json()["total_recommendations"] == 3

    # GET /decisions
    resp = api_client.get("/api/v1/platform-verification/operational-intelligence/decisions")
    assert resp.status_code == 200
    assert resp.json()["total_inquiries_resolved"] == 3

    # GET /dashboard
    resp = api_client.get("/api/v1/platform-verification/operational-intelligence/dashboard")
    assert resp.status_code == 200
    assert resp.json()["overall_platform_health"] == "OPTIMAL"

    # GET /scorecard
    resp = api_client.get("/api/v1/platform-verification/operational-intelligence/scorecard")
    assert resp.status_code == 200
    assert resp.json()["scorecard"]["overall_intelligence_score"] >= 98.0

    # POST /verify
    resp = api_client.post("/api/v1/platform-verification/operational-intelligence/verify?export_evidence=false")
    assert resp.status_code == 200
    assert resp.json()["status"] == "SUCCESS"
    assert resp.json()["summary"]["overall_score"] >= 98.0
