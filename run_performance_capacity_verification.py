"""
Phase 3J.1: Master CLI Runner for Performance Infrastructure Verification & Baseline Capacity Engineering
"""
import sys
from app.platform_verification.performance_capacity_engineering.runtime.performance_verification_runtime import (
    PerformanceVerificationRuntime,
)


def main():
    print("=" * 80)
    print("  PHASE 3J.1: PERFORMANCE INFRASTRUCTURE VERIFICATION")
    print("  Enterprise Load Testing & Baseline Capacity Engineering Framework")
    print("=" * 80)
    print()

    export_dir = "performance_verification"
    print(f"[*] Executing performance verification suite and exporting manifests to '{export_dir}'...\n")

    runtime = PerformanceVerificationRuntime(output_dir=export_dir)
    pipeline_result = runtime.run_pipeline()
    cert = pipeline_result["certification_report"]
    exported_files = pipeline_result["exported_files"]

    print("-" * 80)
    print("  6-CATEGORY ENTERPRISE PERFORMANCE SCORECARD")
    print("-" * 80)
    for c in cert.category_scores:
        status_str = f"[{c.status:^8}]"
        print(f"  {status_str} {c.category_name:<44} | Weight: {c.weight_pct:4.1f}% | Raw: {c.raw_score_pct:6.2f}% | Weighted: {c.weighted_score_pct:5.2f}%")

    print("-" * 80)
    print(f"  FINAL COMPOSITE SCORE:  {cert.composite_performance_score_pct:.2f}%")
    print(f"  CERTIFICATION TIER:     {cert.certification_tier.value}")
    print(f"  PERFORMANCE CERTIFIED:  {'GRANTED' if cert.certification_granted else 'DENIED'}")
    print(f"  EVIDENCE ARTIFACTS:     {len(exported_files)} files cryptographically signed with SHA-256")
    print("=" * 80)
    print()

    if cert.certification_granted and cert.composite_performance_score_pct >= 95.0:
        print("[+] SUCCESS: DocuTask Agent Platform is certified as Enterprise Performance Ready.\n")
        return 0
    else:
        print("[-] FAILURE: Platform verification did not meet the enterprise performance threshold.\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
