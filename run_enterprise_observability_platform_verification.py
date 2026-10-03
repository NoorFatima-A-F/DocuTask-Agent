"""
Phase 3I.11: Master CLI Runner for Enterprise Observability Platform Integration & Global Reliability Control
"""
import sys
from app.platform_verification.enterprise_observability_platform.runtime.enterprise_observability_runtime import (
    EnterpriseObservabilityRuntime,
)


def main():
    print("=" * 80)
    print("  PHASE 3I.11: ENTERPRISE OBSERVABILITY PLATFORM INTEGRATION")
    print("  Multi-Environment Operations & Global Reliability Control Framework")
    print("=" * 80)
    print()

    export_dir = "enterprise_observability_platform_verification"
    print(f"[*] Executing global platform verification suite and exporting manifests to '{export_dir}'...\n")

    runtime = EnterpriseObservabilityRuntime(output_dir=export_dir)
    pipeline_result = runtime.run_pipeline()
    cert = pipeline_result["certification_report"]
    exported_files = pipeline_result["exported_files"]

    print("-" * 80)
    print("  7-CATEGORY ENTERPRISE GLOBAL OPERATIONS SCORECARD")
    print("-" * 80)
    for c in cert.category_scores:
        status_str = f"[{c.status:^8}]"
        print(f"  {status_str} {c.category_name:<34} | Weight: {c.weight_pct:4.1f}% | Raw: {c.raw_score_pct:6.2f}% | Weighted: {c.weighted_score_pct:5.2f}%")

    print("-" * 80)
    print(f"  FINAL COMPOSITE SCORE:  {cert.composite_global_score_pct:.2f}%")
    print(f"  CERTIFICATION TIER:     {cert.certification_tier.value}")
    print(f"  GLOBAL CERTIFICATION:   {'GRANTED' if cert.certification_granted else 'DENIED'}")
    print(f"  EVIDENCE ARTIFACTS:     {len(exported_files)} files cryptographically signed with SHA-256")
    print("=" * 80)
    print()

    if cert.certification_granted and cert.composite_global_score_pct >= 95.0:
        print("[+] SUCCESS: DocuTask Agent Platform is certified as Enterprise Global Operations Ready.\n")
        return 0
    else:
        print("[-] FAILURE: Platform verification did not meet the enterprise certification threshold.\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
