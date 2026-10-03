"""
Master CLI Runner: Phase 3I.2 Enterprise Logging Infrastructure Verification Framework
"""
import sys
import os

# Ensure workspace root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.platform_verification.logging_infrastructure.runtime.logging_verification_runtime import (
    LoggingVerificationRuntime,
)


def main():
    print("=" * 80)
    print("  PHASE 3I.2: ENTERPRISE LOGGING INFRASTRUCTURE VERIFICATION")
    print("  Structured Telemetry, Distributed Correlation & SRE Compliance Engine")
    print("=" * 80)

    runtime = LoggingVerificationRuntime()
    output_dir = "observability_verification/logging"
    print(f"\n[*] Executing enterprise logging verification suite and exporting manifests to '{output_dir}'...")

    results = runtime.run_full_verification(export_dir=output_dir)
    cert = results["certification_report"]
    metadata = results["metadata"]

    print("\n" + "-" * 80)
    print("  6-PILLAR LOGGING QUALITY SCORECARD")
    print("-" * 80)
    for p in cert.pillar_scores:
        print(f"  [{p.status:^17}] {p.pillar_name:<46} | Weight: {p.weight_pct:>4.1f}% | Achieved: {p.achieved_score_pct:>5.2f}% | Weighted: {p.weighted_score_pct:>5.2f}%")

    print("-" * 80)
    print(f"  FINAL COMPOSITE SCORE: {cert.overall_score_pct:.2f}%  (Passing Threshold: {cert.minimum_passing_threshold_pct:.1f}%)")
    print(f"  CERTIFICATION TIER:    {cert.certification_tier.value}")
    print(f"  CERTIFICATION STATUS:  {'GRANTED' if cert.certification_granted else 'REJECTED'}")
    print(f"  EVIDENCE ARTIFACTS:    {metadata['total_artifacts']} JSON manifests cryptographically signed (SHA-256)")
    print("=" * 80)

    if not cert.certification_granted:
        print("\n[!] FAILURE: Logging infrastructure certification criteria not met.")
        sys.exit(1)
    else:
        print("\n[+] SUCCESS: Platform is certified for Phase 3I.2 Enterprise Logging Infrastructure.")
        sys.exit(0)


if __name__ == "__main__":
    main()
