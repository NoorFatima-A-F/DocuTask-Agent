"""
Phase 3I.7: Master CLI Runner for Enterprise Observability Security, Privacy & Compliance Verification
"""
import sys
from app.platform_verification.observability_security.runtime.observability_security_runtime import ObservabilitySecurityRuntime


def main():
    print("=" * 80)
    print("  PHASE 3I.7: ENTERPRISE OBSERVABILITY SECURITY, PRIVACY & COMPLIANCE")
    print("  Zero-Leakage Telemetry, Least-Privilege RBAC & Compliance Certification Engine")
    print("=" * 80)
    print()

    export_dir = "observability_security_verification"
    print(f"[*] Executing observability security verification suite and exporting manifests to '{export_dir}'...\n")

    runtime = ObservabilitySecurityRuntime(output_dir=export_dir)
    results = runtime.run_full_verification()
    cert = results["certification_report"]
    metadata = results["metadata"]

    print("-" * 80)
    print("  6-PILLAR OBSERVABILITY SECURITY & PRIVACY SCORECARD")
    print("-" * 80)
    for p in cert["pillar_scores"]:
        status_str = f"[     {p['status']}      ]" if p["status"] == "PASSED" else f"[   {p['status']}   ]"
        print(f"  {status_str} {p['pillar_name']:<58} | Weight: {p['weight_pct']:4.1f}% | Achieved: {p['achieved_score_pct']:6.2f}% | Weighted: {p['weighted_score_pct']:5.2f}%")

    print("-" * 80)
    print(f"  FINAL COMPOSITE SCORE: {cert['overall_score_pct']:.2f}%  (Passing Threshold: {cert['minimum_passing_threshold_pct']:.1f}%)")
    print(f"  CERTIFICATION TIER:    {cert['certification_tier']}")
    print(f"  CERTIFICATION STATUS:  {'GRANTED' if cert['certification_granted'] else 'DENIED'}")
    print(f"  EVIDENCE ARTIFACTS:    {metadata['total_reports_exported']} JSON reports + metadata cryptographically signed (SHA-256)")
    print("=" * 80)
    print()

    if cert["certification_granted"] and cert["overall_score_pct"] >= 95.0:
        print("[+] SUCCESS: Platform is certified for Phase 3I.7 Enterprise Observability Security, Privacy & Compliance.\n")
        return 0
    else:
        print("[-] FAILURE: Observability security did not meet the enterprise certification threshold.\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
