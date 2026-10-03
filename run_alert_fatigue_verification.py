"""Master CLI Runner for Phase 3H.4.8 — Enterprise Alert Fatigue Prevention & Signal Optimization Framework."""

import sys
import os

# Ensure app package is importable
sys.path.insert(0, os.path.abspath("."))

from app.platform_verification.alert_fatigue_verification.runtime.alert_fatigue_verification_runtime import (
    AlertFatigueVerificationRuntime,
)


def main():
    print("=" * 80)
    print("DocuTask Agent — Phase 3H.4.8: Alert Fatigue Prevention & Signal Optimization")
    print("=" * 80)
    print("Initializing verification runtime and evaluating signal reduction pipeline under storm...")

    runtime = AlertFatigueVerificationRuntime(output_dir="alert_fatigue_verification")
    scorecard, manifests = runtime.execute_full_verification()

    print("\n" + "-" * 80)
    print("ENTERPRISE ALERT FATIGUE & SIGNAL OPTIMIZATION SCORECARD")
    print("-" * 80)
    print(f"Overall Composite Score:        {scorecard.overall_score:.2f}%")
    print(f"Certification Tier:             {scorecard.certification_tier.value}")
    print(f"Certification Verdict:          {scorecard.certification_verdict}")
    print(f"Certified Enterprise Ready:     {'YES (PASSED)' if scorecard.passed else 'NO (FAILED)'}")
    print("-" * 80)
    print("CATEGORY BREAKDOWN:")
    print(f"  • Deduplication Accuracy (20%)        : {scorecard.deduplication_accuracy_score:.2f}%")
    print(f"  • Correlation Quality (20%)           : {scorecard.correlation_quality_score:.2f}%")
    print(f"  • Severity Accuracy (15%)             : {scorecard.severity_accuracy_score:.2f}%")
    print(f"  • Noise Reduction (15%)               : {scorecard.noise_reduction_score:.2f}%")
    print(f"  • Routing Correctness (15%)           : {scorecard.routing_correctness_score:.2f}%")
    print(f"  • Safety Controls & Bypass (15%)      : {scorecard.safety_controls_score:.2f}%")
    print("-" * 80)
    print(f"Evidence manifests exported to 'alert_fatigue_verification/' directory ({len(manifests)} files):")
    for fname in sorted(manifests.keys()):
        print(f"  - {fname}")
    print("=" * 80)

    if scorecard.passed and scorecard.overall_score >= 95.0:
        print("[SUCCESS] Phase 3H.4.8 Alert Fatigue Prevention & Signal Optimization certified successfully.")
        sys.exit(0)
    else:
        print(f"[ERROR] Quality score ({scorecard.overall_score:.2f}%) fell below target (95.00%).")
        sys.exit(1)


if __name__ == "__main__":
    main()
