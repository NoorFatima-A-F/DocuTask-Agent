"""
Phase 3H.4.12: Enterprise Observability Evidence, Audit & Certification Master CLI Runner
"""
import sys
import os
from app.platform_verification.observability_audit_certification.runtime.observability_audit_certification_runtime import (
    ObservabilityAuditCertificationRuntime,
)
from app.platform_verification.observability_audit_certification.domain.models import CICDDecision


def main():
    print("=" * 80)
    print("DocuTask Agent — Phase 3H.4.12: Observability Evidence, Audit & Certification")
    print("=" * 80)
    print("Executing cryptographic evidence audit, PRR review, and CI/CD gate evaluation...\n")

    runtime = ObservabilityAuditCertificationRuntime()
    results = runtime.run_full_audit_and_certification(output_dir="observability_certification")
    cert = results["certification_report"]
    gate = results["cicd_gate_report"]
    prr = results["prr_report"]

    print("-" * 80)
    print("ENTERPRISE OBSERVABILITY CERTIFICATION SCORECARD")
    print("-" * 80)
    print(f"Overall Composite Score:        {cert.composite_score:.2f}%")
    print(f"Certification Tier:             {cert.certification_tier.value}")
    print(f"Production Readiness Review:    {prr.prr_status} (Score: {prr.overall_prr_score:.2f}%)")
    print(f"CI/CD Deployment Gate:          {gate.gate_decision.value} (Pipeline Exit Code: {gate.pipeline_exit_code})")
    print(f"Certified Enterprise Ready:     {'YES (PASSED)' if cert.certified else 'NO (FAILED)'}")
    print("-" * 80)
    print("WEIGHTED CATEGORY BREAKDOWN:")
    for cs in cert.category_scores:
        print(f"  • {cs.category:<25} ({cs.weight * 100:.0f}%): {cs.score:.2f}% [Weighted: {cs.weighted_score:.2f}%]")
    print("-" * 80)
    print(f"Standardized evidence repository exported to 'observability_certification/' ({len(results['exported_files'])} artifacts):")
    for f in sorted(results["exported_files"]):
        print(f"  - {os.path.relpath(f, 'observability_certification')}")
    print("=" * 80)

    if gate.gate_decision in [CICDDecision.DEPLOY, CICDDecision.DEPLOY_WITH_WARNING]:
        print("[SUCCESS] Phase 3H.4.12 Observability Audit & Certification completed successfully. Deployment Approved.\n")
        sys.exit(0)
    else:
        print("[ERROR] Phase 3H.4.12 Observability Audit & Certification rejected deployment.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
