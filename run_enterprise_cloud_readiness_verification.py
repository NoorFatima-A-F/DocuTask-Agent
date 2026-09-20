"""
Master CLI Runner for Phase 3M: Enterprise Cloud Readiness Verification Framework.

Executes all 15 cloud readiness verification phases, evaluates weighted scores across 7 categories,
and exports JSON evidence reports with cryptographic SHA-256 integrity manifest.
"""

import json
import os
import sys
from pathlib import Path

from app.platform_verification.enterprise_cloud_readiness.runtime.cloud_readiness_runtime import (
    CloudReadinessRuntime,
)


def main() -> int:
    output_dir = "cloud_readiness_verification"
    print("=" * 80)
    print("  DocuTask Agent - Enterprise Cloud Readiness Verification Framework")
    print("  Phase 3M Verification Suite (Multi-Cloud Architecture & Portability)")
    print("=" * 80)
    print()

    runtime = CloudReadinessRuntime()

    print("[*] Initializing 15 enterprise cloud readiness verifiers...")
    result = runtime.run_full_verification(export_dir=output_dir)
    scorecard = result["scorecard"]
    manifest = result["manifest"]
    reports = result["reports"]

    print()
    print("-" * 80)
    print("  CLOUD READINESS VERIFICATION PHASES EXECUTION SUMMARY")
    print("-" * 80)

    for report in reports:
        tag = "[PASS]" if report.status.value in ("PASSED", "passed") else "[FAIL]"
        name = getattr(report, "phase_name", "") or getattr(report, "report_title", "")
        print(
            f"  {tag} Phase {report.phase_id:<8} : {name:<55} (Score: {report.score:.1f}%)"
        )

    print()
    print("-" * 80)
    print("  CATEGORY CLOUD READINESS BREAKDOWN (7 ENGINEERING PILLARS)")
    print("-" * 80)

    for cat_name, cat in scorecard.categories.items():
        weight_pct = int(cat.weight * 100)
        print(
            f"  - {cat_name:<30} [Weight: {weight_pct:2d}%] Score: {cat.score:6.2f}% | Contribution: {cat.contribution:5.2f}%"
        )

    print()
    print("=" * 80)
    print(f"  OVERALL CLOUD READINESS SCORE : {scorecard.overall_score:.2f}%")
    print(f"  CERTIFICATION TIER            : {scorecard.certification_tier.value}")
    print(f"  VERIFICATION STATUS           : {scorecard.status.value}")
    print(f"  CLOUD TARGETS SUPPORTED       : {', '.join(manifest.cloud_targets)}")
    print(f"  EVIDENCE DIRECTORY            : {os.path.abspath(output_dir)}")
    print(f"  ARTIFACTS GENERATED           : {len(manifest.files)} files (SHA-256 verified)")
    print("=" * 80)

    return 0 if scorecard.overall_score >= 95.0 else 1


if __name__ == "__main__":
    sys.exit(main())
