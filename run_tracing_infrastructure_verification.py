"""
Phase 3I.4: Master CLI Runner for Enterprise Distributed Tracing Verification
"""
import sys
from app.platform_verification.tracing_infrastructure.runtime.tracing_verification_runtime import TracingVerificationRuntime


def main():
    print("=" * 80)
    print("  PHASE 3I.4: ENTERPRISE DISTRIBUTED TRACING VERIFICATION")
    print("  End-to-End Causal Telemetry, Bottleneck Analysis & SRE Certification Engine")
    print("=" * 80)
    print()

    export_dir = "observability_verification/tracing"
    print(f"[*] Executing enterprise distributed tracing verification suite and exporting manifests to '{export_dir}'...\n")

    runtime = TracingVerificationRuntime()
    results = runtime.run_full_verification(export_dir=export_dir)
    cert = results["certification_report"]
    metadata = results["metadata"]

    print("-" * 80)
    print("  6-PILLAR DISTRIBUTED TRACING QUALITY SCORECARD")
    print("-" * 80)
    for p in cert.pillar_scores:
        status_str = f"[     {p.status}      ]" if p.status == "PASSED" else f"[   {p.status}   ]"
        print(f"  {status_str} {p.pillar_name:<52} | Weight: {p.weight_pct:4.1f}% | Achieved: {p.achieved_score_pct:6.2f}% | Weighted: {p.weighted_score_pct:5.2f}%")

    print("-" * 80)
    print(f"  FINAL COMPOSITE SCORE: {cert.overall_score_pct:.2f}%  (Passing Threshold: {cert.minimum_passing_threshold_pct:.1f}%)")
    print(f"  CERTIFICATION TIER:    {cert.certification_tier.value}")
    print(f"  CERTIFICATION STATUS:  {'GRANTED' if cert.certification_granted else 'DENIED'}")
    print(f"  EVIDENCE ARTIFACTS:    {metadata['total_artifacts']} JSON manifests cryptographically signed (SHA-256)")
    print("=" * 80)
    print()

    if cert.certification_granted and cert.overall_score_pct >= 95.0:
        print("[+] SUCCESS: Platform is certified for Phase 3I.4 Enterprise Distributed Tracing Infrastructure.\n")
        return 0
    else:
        print("[-] FAILURE: Distributed tracing infrastructure did not meet the enterprise certification threshold.\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
