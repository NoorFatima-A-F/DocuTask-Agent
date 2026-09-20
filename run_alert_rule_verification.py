"""Master CLI Runner for Phase 3H.4.5 — Enterprise Alert Rule Verification Framework."""

import sys
import os

# Ensure app package is importable
sys.path.insert(0, os.path.abspath("."))

from app.platform_verification.alert_rule_verification.runtime.alert_rule_verification_runtime import (
    AlertRuleVerificationRuntime,
)
from app.platform_verification.alert_rule_verification.domain.models import (
    AlertCertificationTier,
)


def main():
    print("=" * 80)
    print("DocuTask Agent — Phase 3H.4.5: Enterprise Alert Rule Verification Framework")
    print("=" * 80)
    print("Initializing verification runtime and executing all 14 alert validation phases...")

    runtime = AlertRuleVerificationRuntime(output_dir="alert_verification")
    scorecard, manifests = runtime.execute_full_verification()

    print("\n" + "-" * 80)
    print("ENTERPRISE ALERT QUALITY SCORECARD")
    print("-" * 80)
    print(f"Overall Composite Score:        {scorecard.overall_score:.2f}%")
    print(f"Certification Tier:             {scorecard.certification_tier.value}")
    print(f"Certification Verdict:          {scorecard.certification_verdict}")
    print(f"Certified Enterprise Ready:     {'YES (PASSED)' if scorecard.passed else 'NO (FAILED)'}")
    print("-" * 80)
    print("CATEGORY BREAKDOWN:")
    print(f"  • Detection Accuracy (25%)            : {scorecard.detection_accuracy_score:.2f}%")
    print(f"  • Severity Correctness (20%)          : {scorecard.severity_correctness_score:.2f}%")
    print(f"  • Message Quality (15%)               : {scorecard.message_quality_score:.2f}%")
    print(f"  • Routing Correctness (15%)           : {scorecard.routing_correctness_score:.2f}%")
    print(f"  • Noise Reduction (15%)               : {scorecard.noise_reduction_score:.2f}%")
    print(f"  • Performance & Scale (10%)           : {scorecard.performance_score:.2f}%")
    print("-" * 80)
    print(f"Evidence manifests exported to 'alert_verification/' directory ({len(manifests)} files):")
    for fname in sorted(manifests.keys()):
        print(f"  - {fname}")
    print("=" * 80)

    if scorecard.passed and scorecard.overall_score >= 95.0:
        print("[SUCCESS] Phase 3H.4.5 Alert Rule Verification certified successfully.")
        sys.exit(0)
    else:
        print(f"[ERROR] Quality score ({scorecard.overall_score:.2f}%) fell below target (95.00%).")
        sys.exit(1)


if __name__ == "__main__":
    main()
