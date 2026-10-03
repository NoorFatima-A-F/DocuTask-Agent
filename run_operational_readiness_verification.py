"""
Phase 3H.4.11: Enterprise Operational Readiness Scoring Master CLI Runner
"""
import sys
import os
from app.platform_verification.operational_readiness_verification.runtime.operational_readiness_runtime import (
    OperationalReadinessRuntime,
)


def main():
    print("=" * 80)
    print("DocuTask Agent — Phase 3H.4.11: Operational Readiness Scoring & Certification")
    print("=" * 80)
    print("Initializing readiness scoring engine and aggregating operational evidence...\n")

    runtime = OperationalReadinessRuntime()
    results = runtime.evaluate_operational_readiness(output_dir="operational_readiness_verification")
    scorecard = results["scorecard"]

    print("-" * 80)
    print("ENTERPRISE OPERATIONAL READINESS SCORECARD")
    print("-" * 80)
    print(f"Overall Composite Score:        {scorecard.composite_score:.2f}%")
    print(f"Maturity Classification:        {scorecard.maturity_report.level.value} (Level {scorecard.maturity_report.level_numeric})")
    print(f"Risk Assessment:                {scorecard.risk_report.overall_risk.value} Risk ({scorecard.risk_report.blocking_risks_count} Blocking Issues)")
    print(f"Certification Status:           {scorecard.certification_result.certification.value}")
    print(f"Production Release Status:      {'APPROVED (PASSED)' if scorecard.certification_result.release_approved else 'BLOCKED (FAILED)'}")
    print("-" * 80)
    print("WEIGHTED CATEGORY BREAKDOWN:")
    print(f"  • Metrics Completeness (20%)   : {scorecard.metrics_completeness.score:.2f}%")
    print(f"  • Monitoring Accuracy (20%)    : {scorecard.monitoring_accuracy.score:.2f}% (MTTD: {scorecard.monitoring_accuracy.mean_time_to_detect_seconds}s)")
    print(f"  • Alert Reliability (20%)      : {scorecard.alert_reliability.score:.2f}% (FP Rate: {scorecard.alert_reliability.false_positive_rate}%)")
    print(f"  • Incident Quality (15%)       : {scorecard.incident_quality.score:.2f}%")
    print(f"  • Dashboard Usability (15%)    : {scorecard.dashboard_usability.score:.2f}%")
    print(f"  • Security Readiness (10%)     : {scorecard.security_readiness.score:.2f}%")
    print("-" * 80)
    print(f"Evidence manifests exported to 'operational_readiness_verification/' directory ({len(results['exported_files'])} files):")
    for f in sorted(results["exported_files"]):
        print(f"  - {os.path.basename(f)}")
    print("=" * 80)

    if scorecard.certification_result.release_approved:
        print("[SUCCESS] Phase 3H.4.11 Operational Readiness certified for Enterprise Production.\n")
        sys.exit(0)
    else:
        print("[ERROR] Phase 3H.4.11 Operational Readiness failed certification criteria.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
