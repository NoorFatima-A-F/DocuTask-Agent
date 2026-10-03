"""Master CLI Runner for Phase 3H.4.7 — Enterprise Incident Signal Verification Framework."""

import sys
import os

# Ensure app package is importable
sys.path.insert(0, os.path.abspath("."))

from app.platform_verification.incident_signal_verification.runtime.incident_signal_verification_runtime import (
    IncidentSignalVerificationRuntime,
)


def main():
    print("=" * 80)
    print("DocuTask Agent — Phase 3H.4.7: Enterprise Incident Signal Verification Framework")
    print("=" * 80)
    print("Initializing verification runtime and evaluating incident signal processing pipeline...")

    runtime = IncidentSignalVerificationRuntime(output_dir="incident_signal_verification")
    scorecard, manifests = runtime.execute_full_verification()

    print("\n" + "-" * 80)
    print("ENTERPRISE INCIDENT SIGNAL QUALITY SCORECARD")
    print("-" * 80)
    print(f"Overall Composite Score:        {scorecard.overall_score:.2f}%")
    print(f"Certification Tier:             {scorecard.certification_tier.value}")
    print(f"Certification Verdict:          {scorecard.certification_verdict}")
    print(f"Certified Enterprise Ready:     {'YES (PASSED)' if scorecard.passed else 'NO (FAILED)'}")
    print("-" * 80)
    print("CATEGORY BREAKDOWN:")
    print(f"  • Alert-to-Incident Accuracy (20%)    : {scorecard.alert_to_incident_accuracy_score:.2f}%")
    print(f"  • Context Completeness (20%)          : {scorecard.context_completeness_score:.2f}%")
    print(f"  • Impact Analysis (15%)               : {scorecard.impact_analysis_score:.2f}%")
    print(f"  • Correlation Quality (15%)           : {scorecard.correlation_quality_score:.2f}%")
    print(f"  • Timeline Accuracy (10%)             : {scorecard.timeline_accuracy_score:.2f}%")
    print(f"  • Response Guidance (10%)             : {scorecard.response_guidance_score:.2f}%")
    print(f"  • Security & PII Protection (10%)     : {scorecard.security_score:.2f}%")
    print("-" * 80)
    print(f"Evidence manifests exported to 'incident_signal_verification/' directory ({len(manifests)} files):")
    for fname in sorted(manifests.keys()):
        print(f"  - {fname}")
    print("=" * 80)

    if scorecard.passed and scorecard.overall_score >= 95.0:
        print("[SUCCESS] Phase 3H.4.7 Incident Signal Verification certified successfully.")
        sys.exit(0)
    else:
        print(f"[ERROR] Quality score ({scorecard.overall_score:.2f}%) fell below target (95.00%).")
        sys.exit(1)


if __name__ == "__main__":
    main()
