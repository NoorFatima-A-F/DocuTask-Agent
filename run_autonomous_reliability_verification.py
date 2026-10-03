"""
Phase 3I.12: Master CLI Runner for Autonomous Reliability Engineering & Continuous Optimization
"""
import sys
from app.platform_verification.autonomous_reliability_engineering.runtime.autonomous_reliability_runtime import (
    AutonomousReliabilityRuntime,
)


def main():
    print("=" * 80)
    print("  PHASE 3I.12: AUTONOMOUS RELIABILITY ENGINEERING & CONTINUOUS OPTIMIZATION")
    print("  Operational Intelligence, Self-Optimization & Knowledge Graph Framework")
    print("=" * 80)
    print()

    export_dir = "autonomous_reliability_verification"
    print(f"[*] Executing autonomous reliability verification suite and exporting manifests to '{export_dir}'...\n")

    runtime = AutonomousReliabilityRuntime(output_dir=export_dir)
    pipeline_result = runtime.run_pipeline()
    cert = pipeline_result["certification_report"]
    exported_files = pipeline_result["exported_files"]

    print("-" * 80)
    print("  7-CATEGORY AUTONOMOUS RELIABILITY SCORECARD")
    print("-" * 80)
    for c in cert.category_scores:
        status_str = f"[{c.status:^8}]"
        print(f"  {status_str} {c.category_name:<34} | Weight: {c.weight_pct:4.1f}% | Raw: {c.raw_score_pct:6.2f}% | Weighted: {c.weighted_score_pct:5.2f}%")

    print("-" * 80)
    print(f"  FINAL COMPOSITE SCORE:  {cert.composite_reliability_score_pct:.2f}%")
    print(f"  CERTIFICATION TIER:     {cert.certification_tier.value}")
    print(f"  AUTONOMOUS CERTIFIED:   {'GRANTED' if cert.certification_granted else 'DENIED'}")
    print(f"  EVIDENCE ARTIFACTS:     {len(exported_files)} files cryptographically signed with SHA-256")
    print("=" * 80)
    print()

    if cert.certification_granted and cert.composite_reliability_score_pct >= 95.0:
        print("[+] SUCCESS: DocuTask Agent Platform is certified as Autonomous Reliability Certified.\n")
        return 0
    else:
        print("[-] FAILURE: Platform verification did not meet the autonomous certification threshold.\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
