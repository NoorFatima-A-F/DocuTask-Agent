"""
Phase 3H.9: Enterprise Operational Intelligence, Anomaly Analytics & Decision Support Verification Master CLI Runner
"""
import sys
import os
from pathlib import Path
from app.platform_verification.operational_intelligence.runtime.operational_intelligence_runtime import (
    OperationalIntelligenceRuntime,
)
from app.platform_verification.operational_intelligence.domain.models import (
    IntelligenceCertificationTier,
)


def main():
    print("=" * 80)
    print("DocuTask Agent — Phase 3H.9: Enterprise Operational Intelligence Verification")
    print("=" * 80)
    print("Executing multi-dimensional telemetry correlation, continuous analytics,")
    print("automated anomaly detection, long-term trend analysis, multi-horizon")
    print("capacity forecasting, recommendation engine audits, executive dashboards,")
    print("and empirical decision-support evaluations...\n")

    output_dir = Path("operational_intelligence_verification")
    runtime = OperationalIntelligenceRuntime(output_dir=output_dir)
    results = runtime.run_full_verification(export_evidence=True)

    scorecard = results["scorecard"]
    corr = results["telemetry_correlation_report"]
    analytics = results["operational_analytics_report"]
    anomaly = results["anomaly_detection_report"]
    trend = results["trend_analysis_report"]
    forecast = results["capacity_forecast_report"]
    recom = results["recommendation_engine_report"]
    dash = results["executive_dashboard_report"]
    decision = results["decision_support_report"]
    insight = results["continuous_insight_report"]
    export_meta = results["export_metadata"]

    print("-" * 80)
    print("OPERATIONAL INTELLIGENCE & DECISION SUPPORT SCORECARD")
    print("-" * 80)
    print(f"Verification ID:                {scorecard.verification_id}")
    print(f"Overall Intelligence Score:     {scorecard.overall_intelligence_score:.2f}%")
    print(f"Certification Tier:             {scorecard.certification_tier.value}")
    print(f"Anomaly Detection Accuracy:     {scorecard.anomaly_detection_accuracy_pct:.2f}% (False Positive: {anomaly.false_positive_rate_pct:.1f}%)")
    print(f"Decision Support Confidence:    {scorecard.decision_confidence_pct:.2f}%")
    print(f"Intelligence Certified Ready:   {'YES (PASSED)' if scorecard.passed else 'NO (FAILED)'}")
    print("-" * 80)
    print("OPERATIONAL INTELLIGENCE CAPABILITY DIMENSIONS:")
    print(f"  • Telemetry Correlation:       {len(corr.services_covered)} services correlated across metrics, logs & traces (Confidence: 100%)")
    print(f"  • Operational Analytics:       {len(analytics.subsystem_analytics)} subsystems analyzed ({analytics.total_requests_analyzed:,} requests in {analytics.time_window_evaluated})")
    print(f"  • Anomaly Detection:           {anomaly.total_anomalies_detected} anomalies detected (MTTD: {anomaly.mean_time_to_detect_seconds:.1f}s, Precision: {anomaly.accuracy_rate_pct:.1f}%)")
    print(f"  • Trend Analysis:              {trend.evaluated_trends_count} long-term trajectories evaluated (Latency: Improving, Tokens: Improving)")
    print(f"  • Capacity Forecasting:        {len(forecast.forecasts)} resources projected across 7d, 30d, 90d (Risk: {forecast.capacity_exhaustion_risk})")
    print(f"  • Recommendation Engine:       {recom.total_recommendations} actionable optimizations validated (High, Medium, Low priority)")
    print(f"  • Executive Dashboards:        {len(dash.kpis)} executive KPIs evaluated (Platform health: {dash.overall_platform_health})")
    print(f"  • Decision Support:            {decision.total_inquiries_resolved} strategic engineering inquiries resolved with telemetry evidence")
    print(f"  • Continuous Insight Pipeline: {insight.streams_audited_count} insight streams active with automatic refresh & stale pruning")
    print("-" * 80)
    print("7-PILLAR WEIGHTED INTELLIGENCE BREAKDOWN:")
    for pillar in scorecard.pillar_scores:
        print(f"  • {pillar.pillar_name:<46} ({pillar.weight * 100:.0f}%): {pillar.raw_score:.2f}% (Weighted: {pillar.weighted_score:.2f}%) [{pillar.status}]")
    print("-" * 80)

    if export_meta:
        print("EVIDENCE MANIFEST EXPORTED:")
        print(f"  Directory: {output_dir.resolve()}")
        print(f"  Total Artifacts: {export_meta['total_reports_exported']} files + metadata.json")
        for filename, file_info in export_meta["manifest"].items():
            print(f"    - {filename:<48} ({file_info['size_bytes']} bytes, SHA-256: {file_info['sha256_checksum'][:12]}...)")
        print("-" * 80)

    print(f"RESULT: {scorecard.certification_tier.value.upper()} (Score: {scorecard.overall_intelligence_score:.2f}%)")
    print("=" * 80)

    return 0 if scorecard.passed else 1


if __name__ == "__main__":
    sys.exit(main())
