"""
Master CLI Runner for Phase 3N: Enterprise Infrastructure Security Verification Framework.

Executes all 16 infrastructure security verification phases, evaluates weighted scores across 8 security pillars,
and exports JSON evidence reports with cryptographic SHA-256 integrity manifest.
"""

import os
import sys

from app.platform_verification.enterprise_infrastructure_security.runtime.infrastructure_security_runtime import (
    InfrastructureSecurityRuntime,
)


def main() -> int:
    output_dir = "security_verification"
    print("=" * 80)
    print("  DocuTask Agent - Enterprise Infrastructure Security Verification Framework")
    print("  Phase 3N Verification Suite (Zero-Trust, DevSecOps & AI Hardening)")
    print("=" * 80)
    print()

    runtime = InfrastructureSecurityRuntime()

    print("[*] Initializing 16 enterprise infrastructure security verifiers...")
    result = runtime.run_full_verification(export_dir=output_dir)
    scorecard = result["scorecard"]
    manifest = result["manifest"]
    reports = result["reports"]

    print()
    print("-" * 80)
    print("  INFRASTRUCTURE SECURITY VERIFICATION PHASES EXECUTION SUMMARY")
    print("-" * 80)

    for report in reports:
        tag = "[PASS]" if report.status.value in ("PASSED", "passed") else "[FAIL]"
        name = getattr(report, "phase_name", "") or getattr(report, "report_title", "")
        print(
            f"  {tag} Phase {report.phase_id:<8} : {name:<55} (Score: {report.score:.1f}%)"
        )

    print()
    print("-" * 80)
    print("  CATEGORY SECURITY BREAKDOWN (8 ENGINEERING PILLARS)")
    print("-" * 80)

    for cat_name, cat in scorecard.categories.items():
        weight_pct = int(cat.weight * 100)
        print(
            f"  - {cat_name:<30} [Weight: {weight_pct:2d}%] Score: {cat.score:6.2f}% | Contribution: {cat.contribution:5.2f}%"
        )

    print()
    print("=" * 80)
    print(f"  OVERALL SECURITY SCORE        : {scorecard.overall_score:.2f}%")
    print(f"  CERTIFICATION TIER            : {scorecard.certification_tier.value}")
    print(f"  VERIFICATION STATUS           : {scorecard.status.value}")
    print(f"  SECURITY FRAMEWORK            : {manifest.security_framework}")
    print(f"  EVIDENCE DIRECTORY            : {os.path.abspath(output_dir)}")
    print(f"  ARTIFACTS GENERATED           : {len(manifest.files)} files (SHA-256 verified)")
    print("=" * 80)

    return 0 if scorecard.overall_score >= 95.0 else 1


if __name__ == "__main__":
    sys.exit(main())
