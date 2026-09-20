"""
Phase 3I.5: Master CLI Runner for Enterprise Alerting & Incident Detection Verification
"""
import sys
import os
import json
from app.platform_verification.alerting_infrastructure.runtime.alerting_verification_runtime import AlertingVerificationRuntime


def main():
    print("=" * 80)
    print("  PHASE 3I.5: ENTERPRISE ALERTING & INCIDENT DETECTION VERIFICATION")
    print("  Anomaly Detection, SRE Golden Signals & Self-Healing SRE Engine")
    print("=" * 80)
    print()

    export_dir = "observability_verification/alerting"
    print(f"[*] Executing enterprise alerting verification suite and exporting manifests to '{export_dir}'...\n")

    runtime = AlertingVerificationRuntime()
    results = runtime.run_full_verification(export_dir=export_dir)
    cert = results["certification_report"]
    metadata = results["metadata"]

    print("-" * 80)
    print("  6-PILLAR INCIDENT DETECTION QUALITY SCORECARD")
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
        print("[+] SUCCESS: Platform is certified for Phase 3I.5 Enterprise Alerting & Incident Detection.\n")
        return 0
    else:
        print("[-] FAILURE: Alerting infrastructure did not meet the enterprise certification threshold.\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
