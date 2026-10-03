"""
Master CLI Runner for Phase 3L: Enterprise Backup, Disaster Recovery & Business Continuity Verification Framework.

Executes all 13 disaster recovery verification phases, evaluates weighted scores across 6 categories,
and exports JSON evidence reports with cryptographic SHA-256 integrity manifest.
"""

import os
import sys

from app.platform_verification.enterprise_disaster_recovery.runtime.disaster_recovery_runtime import (
    DisasterRecoveryRuntime,
)


def main() -> int:
    output_dir = "disaster_recovery_verification"
    print("=" * 80)
    print("  DocuTask Agent - Enterprise Backup, Disaster Recovery & Continuity")
    print("  Phase 3L Verification Suite (Enterprise Operational Survivability)")
    print("=" * 80)
    print()

    runtime = DisasterRecoveryRuntime()

    print("[*] Initializing 13 enterprise disaster recovery verifiers...")
    result = runtime.run_full_verification(export_dir=output_dir)
    scorecard = result["scorecard"]
    manifest = result["manifest"]
    reports = result["reports"]

    print()
    print("-" * 80)
    print("  DISASTER RECOVERY VERIFICATION PHASES EXECUTION SUMMARY")
    print("-" * 80)

    for report in reports:
        tag = "[PASS]" if report.status.value in ("PASSED", "passed") else "[FAIL]"
        name = getattr(report, "phase_name", "") or getattr(report, "report_title", "")
        print(
            f"  {tag} Phase {report.phase_id:<8} : {name:<55} (Score: {report.score:.1f}%)"
        )

    print()
    print("-" * 80)
    print("  CATEGORY RECOVERY BREAKDOWN (6 ENGINEERING DIMENSIONS)")
    print("-" * 80)

    for cat_name, cat in scorecard.categories.items():
        weight_pct = int(cat.weight * 100)
        print(
            f"  - {cat_name:<25} [Weight: {weight_pct:2d}%] Score: {cat.score:6.2f}% | Contribution: {cat.contribution:5.2f}%"
        )

    print()
    print("=" * 80)
    print(f"  OVERALL RECOVERY SCORE      : {scorecard.overall_score:.2f}%")
    print(f"  CERTIFICATION TIER          : {scorecard.certification_tier.value}")
    print(f"  VERIFICATION STATUS         : {scorecard.status.value}")
    print(f"  EVIDENCE DIRECTORY          : {os.path.abspath(output_dir)}")
    print(f"  ARTIFACTS GENERATED         : {len(manifest.files)} files (SHA-256 verified)")
    print("=" * 80)

    return 0 if scorecard.overall_score >= 95.0 else 1


if __name__ == "__main__":
    sys.exit(main())
