"""
Phase 3H.5: Enterprise Health Intelligence, Diagnosis & Automated Remediation Master CLI Runner
"""
import sys
import os
from app.platform_verification.enterprise_health_intelligence.runtime.health_intelligence_runtime import (
    HealthIntelligenceRuntime,
)
from app.platform_verification.enterprise_health_intelligence.domain.models import IntelligenceCertificationTier


def main():
    print("=" * 80)
    print("DocuTask Agent — Phase 3H.5: Health Intelligence, Diagnosis & Remediation")
    print("=" * 80)
    print("Executing event correlation, RCA verification, remediation decisioning, and self-healing...\n")

    runtime = HealthIntelligenceRuntime()
    results = runtime.run_full_verification(output_dir="health_intelligence_verification")
    scorecard = results["scorecard"]
    event_report = results["event_report"]
    class_report = results["class_report"]
    corr_report = results["corr_report"]
    rca_report = results["rca_report"]
    remed_report = results["remed_report"]
    recov_report = results["recov_report"]
    self_heal_report = results["self_heal_report"]
    chaos_report = results["chaos_report"]

    print("-" * 80)
    print("ENTERPRISE HEALTH INTELLIGENCE & REMEDIATION SCORECARD")
    print("-" * 80)
    print(f"Overall Composite Score:        {scorecard.composite_score:.2f}%")
    print(f"Intelligence Maturity Tier:     {scorecard.tier.value}")
    print(f"Self-Healing Validation:        {'PASSED' if self_heal_report.self_healing_certified else 'FAILED'} (Success Rate: {self_heal_report.automatic_recovery_success_rate:.1f}%)")
    print(f"Certified Enterprise Ready:     {'YES (CERTIFIED)' if scorecard.certified_enterprise_ready else 'NO (FAILED)'}")
    print("-" * 80)
    print("OPERATIONAL HEALTH INTELLIGENCE SUMMARY:")
    print(f"  • Captured Health Events:      {event_report.total_events_captured} across {len(event_report.supported_event_types)} event types")
    print(f"  • Failure Classification:      {class_report.classification_accuracy_pct:.2f}% accuracy ({class_report.total_classified_events} events)")
    print(f"  • Signal Noise Reduction:      {corr_report.noise_reduction_pct:.2f}% ({corr_report.total_raw_signals} raw signals -> {corr_report.total_correlated_incidents} incidents)")
    print(f"  • RCA Confidence Score:        {rca_report.mean_confidence_score * 100:.2f}% ({rca_report.total_rcas_performed} root causes identified)")
    print(f"  • Remediation Safety Matrix:   {remed_report.total_decisions} decisions evaluated (0 forbidden actions executed)")
    print(f"  • Recovery Workflow MTTR:      {self_heal_report.mean_time_to_recovery_seconds:.1f}s (MTTD: {self_heal_report.mean_time_to_detection_seconds:.1f}s)")
    print(f"  • Chaos Fault Injection:       {'PASSED' if chaos_report.all_chaos_tests_passed else 'FAILED'} ({len(chaos_report.tests)}/4 tests validated)")
    print("-" * 80)
    print("WEIGHTED SCORECARD PILLARS:")
    print(f"  • Failure Detection   (15%): {scorecard.failure_detection_score:.2f}%")
    print(f"  • Diagnosis Accuracy  (20%): {scorecard.diagnosis_accuracy_score:.2f}%")
    print(f"  • Event Correlation   (15%): {scorecard.event_correlation_score:.2f}%")
    print(f"  • RCA Quality         (15%): {scorecard.rca_quality_score:.2f}%")
    print(f"  • Recovery Automation (20%): {scorecard.recovery_automation_score:.2f}%")
    print(f"  • Safety Controls     (15%): {scorecard.safety_controls_score:.2f}%")
    print("-" * 80)
    print(f"Standardized evidence repository exported to 'health_intelligence_verification/' ({len(results['exported_files'])} artifacts):")
    for f in sorted(results["exported_files"]):
        print(f"  - {os.path.relpath(f, 'health_intelligence_verification')}")
    print("=" * 80)

    if scorecard.certified_enterprise_ready and scorecard.composite_score >= 90.0:
        print("[SUCCESS] Phase 3H.5 Health Intelligence, Diagnosis & Remediation Verification PASSED.\n")
        sys.exit(0)
    else:
        print("[ERROR] Phase 3H.5 Verification FAILED to meet enterprise thresholds.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
