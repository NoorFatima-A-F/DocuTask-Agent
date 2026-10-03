"""Master CLI Runner for Phase 3H.4.6 — Enterprise Alert Accuracy & Intelligence Verification Framework."""

import sys
import os

# Ensure app package is importable
sys.path.insert(0, os.path.abspath("."))

from app.platform_verification.alert_accuracy_verification.runtime.alert_accuracy_verification_runtime import (
    AlertAccuracyVerificationRuntime,
)


def main():
    print("=" * 80)
    print("DocuTask Agent — Phase 3H.4.6: Enterprise Alert Accuracy Verification Framework")
    print("=" * 80)
    print("Initializing accuracy verification runtime and evaluating all statistical dimensions...")

    runtime = AlertAccuracyVerificationRuntime(output_dir="alert_accuracy_verification")
    scorecard, manifests = runtime.execute_full_verification()

    print("\n" + "-" * 80)
    print("ENTERPRISE ALERT ACCURACY & INTELLIGENCE SCORECARD")
    print("-" * 80)
    print(f"Overall Composite Score:        {scorecard.overall_score:.2f}%")
    print(f"Certification Tier:             {scorecard.certification_tier.value}")
    print(f"Certification Verdict:          {scorecard.certification_verdict}")
    print(f"Certified Enterprise Ready:     {'YES (PASSED)' if scorecard.passed else 'NO (FAILED)'}")
    print("-" * 80)
    print("CATEGORY BREAKDOWN:")
    print(f"  • True Positive Detection (25%)       : {scorecard.true_positive_score:.2f}%")
    print(f"  • False Positive Control (20%)        : {scorecard.false_positive_score:.2f}%")
    print(f"  • False Negative Prevention (20%)     : {scorecard.false_negative_score:.2f}%")
    print(f"  • Severity Accuracy (15%)             : {scorecard.severity_accuracy_score:.2f}%")
    print(f"  • Detection Speed (10%)               : {scorecard.detection_speed_score:.2f}%")
    print(f"  • Correlation Quality (10%)           : {scorecard.correlation_quality_score:.2f}%")
    print("-" * 80)
    print(f"Evidence manifests exported to 'alert_accuracy_verification/' directory ({len(manifests)} files):")
    for fname in sorted(manifests.keys()):
        print(f"  - {fname}")
    print("=" * 80)

    if scorecard.passed and scorecard.overall_score >= 95.0:
        print("[SUCCESS] Phase 3H.4.6 Alert Accuracy & Intelligence Verification certified successfully.")
        sys.exit(0)
    else:
        print(f"[ERROR] Quality score ({scorecard.overall_score:.2f}%) fell below target (95.00%).")
        sys.exit(1)


if __name__ == "__main__":
    main()
