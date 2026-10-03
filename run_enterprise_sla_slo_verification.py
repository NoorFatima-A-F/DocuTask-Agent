"""
Master CLI Runner for Phase 3J.10: Enterprise Performance SLA, SLO & Continuous Reliability Verification.

Executes all 12 SLA/SLO verification phases, evaluates weighted scores across 6 SRE categories,
and exports JSON evidence reports with cryptographic SHA-256 integrity manifest.
"""

import os
import sys

from app.platform_verification.enterprise_sla_slo_verification.runtime.sla_slo_runtime import (
    SLASLORuntime,
)


def main() -> int:
    output_dir = "sla_slo_verification"
    print("=" * 80)
    print("  DocuTask Agent - Enterprise Performance SLA/SLO & Continuous Reliability")
    print("  Phase 3J.10 Verification Suite")
    print("=" * 80)
    print()

    runtime = SLASLORuntime(export_dir=output_dir)

    print("[*] Initializing 12 SLA/SLO & continuous reliability verification engines...")
    result = runtime.run_all()
    scorecard = result["scorecard"]
    manifest = result["manifest"]
    reports = result["reports"]

    print()
    print("-" * 80)
    print("  VERIFICATION PHASES EXECUTION SUMMARY")
    print("-" * 80)

    for report in reports:
        tag = "[PASS]" if report.status.value in ("PASSED", "passed") else "[FAIL]"
        print(
            f"  {tag} Phase {report.phase_id:<12} : {report.phase_name:<50} (Score: {report.score:.1f}%)"
        )

    print()
    print("-" * 80)
    print("  CATEGORY RELIABILITY BREAKDOWN (6 SRE DIMENSIONS)")
    print("-" * 80)

    for cat_name, cat in scorecard.categories.items():
        weight_pct = int(cat.weight * 100)
        print(
            f"  - {cat_name:<24} [Weight: {weight_pct:2d}%] Score: {cat.score:6.2f}% | Contribution: {cat.contribution:5.2f}%"
        )

    print()
    print("=" * 80)
    print(f"  OVERALL RELIABILITY SCORE   : {scorecard.overall_score:.2f}%")
    print(f"  CERTIFICATION TIER          : {scorecard.certification_tier.value}")
    print(f"  VERIFICATION STATUS         : {scorecard.status.value}")
    print(f"  EVIDENCE DIRECTORY          : {os.path.abspath(output_dir)}")
    print(f"  ARTIFACTS GENERATED         : {len(manifest.files)} files (SHA-256 verified)")
    print("=" * 80)

    return 0 if scorecard.overall_score >= 95.0 else 1


if __name__ == "__main__":
    sys.exit(main())
