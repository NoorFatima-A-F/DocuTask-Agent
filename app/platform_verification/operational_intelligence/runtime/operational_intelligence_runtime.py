"""
Phase 3H.9: Enterprise Operational Intelligence Verification Runtime Orchestrator
"""
import logging
from typing import Dict, Any, Optional
from pathlib import Path

from app.platform_verification.operational_intelligence.verifiers.telemetry_correlation_verifier import TelemetryCorrelationVerifier
from app.platform_verification.operational_intelligence.verifiers.operational_analytics_verifier import OperationalAnalyticsVerifier
from app.platform_verification.operational_intelligence.verifiers.anomaly_detection_verifier import AnomalyDetectionVerifier
from app.platform_verification.operational_intelligence.verifiers.trend_analysis_verifier import TrendAnalysisVerifier
from app.platform_verification.operational_intelligence.verifiers.capacity_forecast_verifier import CapacityForecastVerifier
from app.platform_verification.operational_intelligence.verifiers.recommendation_engine_verifier import RecommendationEngineVerifier
from app.platform_verification.operational_intelligence.verifiers.executive_dashboard_verifier import ExecutiveDashboardVerifier
from app.platform_verification.operational_intelligence.verifiers.decision_support_verifier import DecisionSupportVerifier
from app.platform_verification.operational_intelligence.verifiers.continuous_insight_verifier import ContinuousInsightVerifier
from app.platform_verification.operational_intelligence.scoring.operational_intelligence_scorer import OperationalIntelligenceScorer
from app.platform_verification.operational_intelligence.exporter.operational_intelligence_exporter import OperationalIntelligenceExporter

logger = logging.getLogger("operational_intelligence.runtime")


class OperationalIntelligenceRuntime:
    """
    Main runtime orchestrator for Phase 3H.9 Operational Intelligence Verification Framework.
    """

    def __init__(self, output_dir: Optional[Path] = None):
        self.corr_verifier = TelemetryCorrelationVerifier()
        self.analytics_verifier = OperationalAnalyticsVerifier()
        self.anomaly_verifier = AnomalyDetectionVerifier()
        self.trend_verifier = TrendAnalysisVerifier()
        self.forecast_verifier = CapacityForecastVerifier()
        self.recom_verifier = RecommendationEngineVerifier()
        self.dash_verifier = ExecutiveDashboardVerifier()
        self.decision_verifier = DecisionSupportVerifier()
        self.insight_verifier = ContinuousInsightVerifier()
        self.scorer = OperationalIntelligenceScorer()
        self.exporter = OperationalIntelligenceExporter(output_dir=output_dir)

    def run_full_verification(self, export_evidence: bool = True) -> Dict[str, Any]:
        logger.info("Starting Phase 3H.9 Enterprise Operational Intelligence Verification Suite...")

        # 1. Execute all 9 Verifiers
        corr_report = self.corr_verifier.verify_telemetry_correlation()
        analytics_report = self.analytics_verifier.verify_operational_analytics()
        anomaly_report = self.anomaly_verifier.verify_anomaly_detection()
        trend_report = self.trend_verifier.verify_trend_analysis()
        forecast_report = self.forecast_verifier.verify_capacity_forecasting()
        recom_report = self.recom_verifier.verify_recommendation_engine()
        dash_report = self.dash_verifier.generate_executive_dashboard()
        decision_report = self.decision_verifier.verify_decision_support()
        insight_report = self.insight_verifier.verify_continuous_insights()

        # 2. Scorecard Calculation
        scorecard = self.scorer.calculate_scorecard(
            corr_report=corr_report,
            analytics_report=analytics_report,
            anomaly_report=anomaly_report,
            trend_report=trend_report,
            forecast_report=forecast_report,
            recom_report=recom_report,
            dash_report=dash_report,
            decision_report=decision_report,
            insight_report=insight_report,
        )

        export_metadata = None
        if export_evidence:
            export_metadata = self.exporter.export_all(
                corr_report=corr_report,
                analytics_report=analytics_report,
                anomaly_report=anomaly_report,
                trend_report=trend_report,
                forecast_report=forecast_report,
                recom_report=recom_report,
                dash_report=dash_report,
                decision_report=decision_report,
                insight_report=insight_report,
                scorecard=scorecard,
            )

        logger.info(
            f"Phase 3H.9 Verification Complete. Score: {scorecard.overall_intelligence_score}% "
            f"({scorecard.certification_tier.value}). Passed: {scorecard.passed}"
        )

        return {
            "scorecard": scorecard,
            "telemetry_correlation_report": corr_report,
            "operational_analytics_report": analytics_report,
            "anomaly_detection_report": anomaly_report,
            "trend_analysis_report": trend_report,
            "capacity_forecast_report": forecast_report,
            "recommendation_engine_report": recom_report,
            "executive_dashboard_report": dash_report,
            "decision_support_report": decision_report,
            "continuous_insight_report": insight_report,
            "export_metadata": export_metadata,
        }
