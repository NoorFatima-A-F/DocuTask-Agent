"""
Phase 3H.5.9: Predictive Health Intelligence & Proactive Failure Prevention Master CLI Runner
"""
import sys
import os
from app.platform_verification.predictive_failure_prevention.runtime.predictive_health_runtime import (
    PredictiveHealthRuntime,
)


def main():
    print("=" * 80)
    print("DocuTask Agent — Phase 3H.5.9: Predictive Health Intelligence & Failure Prevention")
    print("=" * 80)
    print("Executing predictive analytics, anomaly detection, failure forecasting, and chaos validation...\n")

    runtime = PredictiveHealthRuntime()
    results = runtime.run_full_verification(output_dir="predictive_failure_prevention_verification")
    scorecard = results["scorecard"]
    arch_report = results["arch_report"]
    feature_report = results["feature_report"]
    anomaly_report = results["anomaly_report"]
    prediction_report = results["prediction_report"]
    capacity_report = results["capacity_report"]
    remediation_report = results["remediation_report"]
    accuracy_report = results["accuracy_report"]
    incident_report = results["incident_report"]
    twin_report = results["twin_report"]
    chaos_report = results["chaos_report"]
    dashboard_report = results["dashboard_report"]

    print("-" * 80)
    print("PREDICTIVE HEALTH INTELLIGENCE & FAILURE PREVENTION SCORECARD")
    print("-" * 80)
    print(f"Overall Composite Score:        {scorecard.composite_score:.2f}%")
    print(f"Predictive Maturity Tier:       {scorecard.tier.value}")
    print(f"Certified Predictive Ready:     {'YES (CERTIFIED)' if scorecard.certified_predictive_ready else 'NO (FAILED)'}")
    print("-" * 80)
    print("PREDICTIVE INTELLIGENCE SUMMARY:")
    print(f"  • Architecture Pipeline:       {len(arch_report.pipeline_stages)} stages, {arch_report.total_signal_sources} signal sources")
    print(f"  • Feature Engineering:         {feature_report.total_features_extracted} features ({feature_report.resource_features_count}R/{feature_report.performance_features_count}P/{feature_report.reliability_features_count}L/{feature_report.ai_features_count}AI)")
    print(f"  • Anomaly Detection:           {anomaly_report.total_anomalies_detected} anomalies (stat={anomaly_report.statistical_detection_active}, trend={anomaly_report.trend_detection_active}, behavioral={anomaly_report.behavioral_detection_active})")
    print(f"  • Failure Predictions:         {prediction_report.total_predictions} predictions ({prediction_report.high_risk_predictions} high/critical risk)")
    print(f"  • Capacity Forecasts:          {capacity_report.total_capacity_predictions} forecasts ({capacity_report.critical_resources} critical)")
    print(f"  • Preventive Actions:          {remediation_report.total_preventive_actions} actions ({remediation_report.automatic_actions_count} auto, {remediation_report.approval_required_count} approval-required)")
    print(f"  • Prediction Accuracy:         precision={accuracy_report.metrics.precision:.2%}, recall={accuracy_report.metrics.recall:.2%}, false_alarm={accuracy_report.false_alarm_rate_pct:.2f}%")
    print(f"  • Predictive Incidents:        {incident_report.total_predictive_incidents} pre-failure incidents created")
    print(f"  • Reliability Twin:            {twin_report.total_components_modeled} components ({twin_report.healthy_components} healthy, {twin_report.degraded_components} degraded)")
    print(f"  • Chaos Prediction:            {'PASSED' if chaos_report.all_chaos_predictions_passed else 'FAILED'} ({len(chaos_report.scenarios)}/{chaos_report.total_chaos_scenarios} scenarios, mean lead={chaos_report.mean_prediction_lead_time_seconds:.1f}s)")
    print(f"  • Dashboards:                  {dashboard_report.total_dashboards} active")
    print("-" * 80)
    print("WEIGHTED SCORECARD PILLARS:")
    print(f"  • Prediction Accuracy    (25%): {scorecard.prediction_accuracy_score:.2f}%")
    print(f"  • Anomaly Detection      (20%): {scorecard.anomaly_detection_score:.2f}%")
    print(f"  • Preventive Actions     (20%): {scorecard.preventive_actions_score:.2f}%")
    print(f"  • False Alarm Control    (15%): {scorecard.false_alarm_control_score:.2f}%")
    print(f"  • Reliability Improvement(10%): {scorecard.reliability_improvement_score:.2f}%")
    print(f"  • Security               (10%): {scorecard.security_score:.2f}%")
    print("-" * 80)
    print(f"Standardized evidence repository exported to 'predictive_failure_prevention_verification/' ({len(results['exported_files'])} artifacts):")
    for f in sorted(results["exported_files"]):
        print(f"  - {os.path.relpath(f, 'predictive_failure_prevention_verification')}")
    print("=" * 80)

    if scorecard.certified_predictive_ready and scorecard.composite_score >= 90.0:
        print("[SUCCESS] Phase 3H.5.9 Predictive Health Intelligence & Failure Prevention Verification PASSED.\n")
        sys.exit(0)
    else:
        print("[ERROR] Phase 3H.5.9 Verification FAILED to meet predictive readiness thresholds.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
