"""
Phase 3I.6: Master CLI Runner for Observability Governance, SLO Engineering & Reliability Certification
"""
import sys
import os
import json
from app.platform_verification.reliability_governance.runtime.reliability_governance_runtime import ReliabilityGovernanceRuntime


def main():
    print("=" * 80)
    print("  PHASE 3I.6: OBSERVABILITY GOVERNANCE, SLO ENGINEERING & RELIABILITY")
    print("  Enterprise SRE Quantitative Reliability Certification Engine")
    print("=" * 80)
    print()

    export_dir = "observability_verification/reliability"
    print(f"[*] Executing reliability governance verification suite and exporting manifests to '{export_dir}'...\n")

    runtime = ReliabilityGovernanceRuntime(output_dir=export_dir)
    results = runtime.run_full_verification()
    cert = results["certification_report"]
    metadata = results["metadata"]

    print("-" * 80)
    print("  6-PILLAR RELIABILITY GOVERNANCE SCORECARD")
    print("-" * 80)
    for p in cert["pillar_scores"]:
        status_str = f"[     {p['status']}      ]" if p["status"] == "PASSED" else f"[   {p['status']}   ]"
        print(f"  {status_str} {p['pillar_name']:<55} | Weight: {p['weight_pct']:4.1f}% | Achieved: {p['achieved_score_pct']:6.2f}% | Weighted: {p['weighted_score_pct']:5.2f}%")

    print("-" * 80)
    print(f"  FINAL COMPOSITE SCORE: {cert['overall_score_pct']:.2f}%  (Passing Threshold: {cert['minimum_passing_threshold_pct']:.1f}%)")
    print(f"  CERTIFICATION TIER:    {cert['certification_tier']}")
    print(f"  CERTIFICATION STATUS:  {'GRANTED' if cert['certification_granted'] else 'DENIED'}")
    print(f"  EVIDENCE ARTIFACTS:    {metadata['total_reports_exported']} JSON reports + metadata cryptographically signed (SHA-256)")
    print("=" * 80)
    print()

    if cert["certification_granted"] and cert["overall_score_pct"] >= 95.0:
        print("[+] SUCCESS: Platform is certified for Phase 3I.6 Enterprise Observability Governance & Reliability.\n")
        return 0
    else:
        print("[-] FAILURE: Reliability governance did not meet the enterprise certification threshold.\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
