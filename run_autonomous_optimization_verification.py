"""
Master CLI Runner: Phase 3H.10 Autonomous Operational Intelligence & Self-Optimization Verification Framework
"""
import sys
import os

# Ensure workspace root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.platform_verification.autonomous_optimization.runtime.autonomous_optimization_runtime import (
    AutonomousOptimizationRuntime,
)


def main():
    print("=" * 80)
    print("  PHASE 3H.10: AUTONOMOUS OPERATIONAL INTELLIGENCE & SELF-OPTIMIZATION")
    print("  Verification, Predictive Reliability & Certification Framework")
    print("=" * 80)

    runtime = AutonomousOptimizationRuntime()
    output_dir = "autonomous_intelligence_verification"
    print(f"\n[*] Executing autonomous optimization verifiers and exporting to '{output_dir}'...")

    results = runtime.run_full_verification(export_dir=output_dir)
    cert = results["certification_report"]
    metadata = results["metadata"]

    print("\n" + "-" * 80)
    print("  7-PILLAR AUTONOMOUS OPERATIONS SCORECARD")
    print("-" * 80)
    for p in cert.pillar_scores:
        print(f"  [{p.status:^17}] {p.pillar_name:<38} | Weight: {p.weight_pct:>4.1f}% | Achieved: {p.achieved_score_pct:>5.2f}% | Weighted: {p.weighted_score_pct:>5.2f}%")

    print("-" * 80)
    print(f"  FINAL COMPOSITE SCORE: {cert.overall_score_pct:.2f}%  (Passing Threshold: {cert.minimum_passing_threshold_pct:.1f}%)")
    print(f"  CERTIFICATION TIER:    {cert.certification_tier.value}")
    print(f"  CERTIFICATION STATUS:  {'GRANTED' if cert.certification_granted else 'REJECTED'}")
    print(f"  EVIDENCE ARTIFACTS:    {metadata['total_artifacts']} JSON manifests cryptographically signed (SHA-256)")
    print("=" * 80)

    if not cert.certification_granted:
        print("\n[!] FAILURE: Autonomous operations certification criteria not met.")
        sys.exit(1)
    else:
        print("\n[+] SUCCESS: Platform is certified for Phase 3H.10 Autonomous Operations & Self-Optimization.")
        sys.exit(0)


if __name__ == "__main__":
    main()
