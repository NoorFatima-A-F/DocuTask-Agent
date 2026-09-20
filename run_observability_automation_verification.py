"""
Phase 3I.8: Master CLI Runner for Enterprise Observability Automation, Self-Healing Operations & Autonomous Reliability
"""
import sys
import os
import json
from app.platform_verification.observability_automation.runtime.observability_automation_runtime import ObservabilityAutomationRuntime


def main():
    print("=" * 80)
    print("  PHASE 3I.8: OBSERVABILITY AUTOMATION & AUTONOMOUS RELIABILITY")
    print("  Self-Healing Operations, Multi-Modal RCA & AIOps Certification Engine")
    print("=" * 80)
    print()

    export_dir = "observability_automation_verification"
    print(f"[*] Executing autonomous operations verification suite and exporting manifests to '{export_dir}'...\n")

    runtime = ObservabilityAutomationRuntime(output_dir=export_dir)
    results = runtime.run_full_verification()
    cert = results["certification_report"]
    metadata = results["metadata"]

    print("-" * 80)
    print("  6-PILLAR AUTONOMOUS RELIABILITY SCORECARD")
    print("-" * 80)
    for p in cert["pillar_scores"]:
        status_str = f"[     {p['status']}      ]" if p["status"] == "PASSED" else f"[   {p['status']}   ]"
        print(f"  {status_str} {p['pillar_name']:<60} | Weight: {p['weight_pct']:4.1f}% | Achieved: {p['achieved_score_pct']:6.2f}% | Weighted: {p['weighted_score_pct']:5.2f}%")

    print("-" * 80)
    print(f"  FINAL COMPOSITE SCORE: {cert['overall_score_pct']:.2f}%  (Passing Threshold: {cert['minimum_passing_threshold_pct']:.1f}%)")
    print(f"  CERTIFICATION TIER:    {cert['certification_tier']}")
    print(f"  CERTIFICATION STATUS:  {'GRANTED' if cert['certification_granted'] else 'DENIED'}")
    print(f"  EVIDENCE ARTIFACTS:    {metadata['total_reports_exported']} JSON reports + metadata cryptographically signed (SHA-256)")
    print("=" * 80)
    print()

    if cert["certification_granted"] and cert["overall_score_pct"] >= 95.0:
        print("[+] SUCCESS: Platform is certified for Phase 3I.8 Autonomous Operations & Reliability.\n")
        return 0
    else:
        print("[-] FAILURE: Autonomous operations did not meet the enterprise certification threshold.\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
