"""
Phase 3I.10: Master CLI Runner for Enterprise Observability Intelligence Governance & Operations Certification
"""
import sys
from app.platform_verification.observability_operations_governance.runtime.observability_operations_runtime import (
    ObservabilityOperationsRuntime,
)


def main():
    print("=" * 80)
    print("  PHASE 3I.10: OBSERVABILITY INTELLIGENCE GOVERNANCE & AUTONOMOUS OPERATIONS")
    print("  Reliability Automation Maturity & Enterprise SRE Certification Framework")
    print("=" * 80)
    print()

    export_dir = "observability_governance_verification"
    print(f"[*] Executing operational governance verification suite and exporting manifests to '{export_dir}'...\n")

    runtime = ObservabilityOperationsRuntime(output_dir=export_dir)
    pipeline_result = runtime.run_pipeline()
    cert = pipeline_result["certification_report"]
    exported_files = pipeline_result["exported_files"]

    print("-" * 80)
    print("  6-PILLAR ENTERPRISE OPERATIONS SCORECARD")
    print("-" * 80)
    for p in cert.pillar_scores:
        status_str = f"[{p.status:^8}]"
        print(f"  {status_str} {p.pillar_name:<30} | Weight: {p.weight_pct:4.1f}% | Raw: {p.raw_score_pct:6.2f}% | Weighted: {p.weighted_score_pct:5.2f}%")

    print("-" * 80)
    print(f"  FINAL COMPOSITE SCORE:  {cert.composite_operations_score_pct:.2f}%")
    print(f"  TARGET MATURITY LEVEL:  {cert.target_maturity_level.value}")
    print(f"  CERTIFICATION TIER:     {cert.certification_tier.value}")
    print(f"  AUTONOMOUS CERTIFIED:   {'GRANTED' if cert.autonomous_operations_certified else 'DENIED'}")
    print(f"  EVIDENCE ARTIFACTS:     {len(exported_files)} files cryptographically signed with SHA-256")
    print("=" * 80)
    print()

    if cert.autonomous_operations_certified and cert.composite_operations_score_pct >= 95.0:
        print("[+] SUCCESS: DocuTask Agent Platform is certified for Phase 3I.10 Enterprise Autonomous Operations.\n")
        return 0
    else:
        print("[-] FAILURE: Governance verification did not meet the enterprise certification threshold.\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
