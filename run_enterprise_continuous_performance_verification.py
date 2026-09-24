"""
Master CLI Runner for Phase 3J.12: Continuous Performance Engineering & Regression Intelligence.

Executes all 12 continuous performance verification phases, evaluates weighted scores across 6 categories,
and exports JSON evidence reports with cryptographic SHA-256 integrity manifest.
"""

import os
import sys

from app.platform_verification.continuous_performance_engineering.runtime.continuous_performance_runtime import (
    ContinuousPerformanceRuntime,
)


def main() -> int:
    output_dir = "continuous_performance_verification"
    print("=" * 80)
    print("  DocuTask Agent - Continuous Performance Engineering & Regression Intelligence")
    print("  Phase 3J.12 Verification Suite (Final Maturity Layer of Part 3J)")
    print("=" * 80)
    print()

    runtime = ContinuousPerformanceRuntime(export_dir=output_dir)

    print("[*] Initializing 12 continuous performance engineering & regression engines...")
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
    print("  CATEGORY RELIABILITY BREAKDOWN (6 ENGINEERING DIMENSIONS)")
    print("-" * 80)

    for cat_name, cat in scorecard.categories.items():
        weight_pct = int(cat.weight * 100)
        print(
            f"  - {cat_name:<30} [Weight: {weight_pct:2d}%] Score: {cat.score:6.2f}% | Contribution: {cat.contribution:5.2f}%"
        )

    print()
    print("=" * 80)
    print(f"  OVERALL ENGINEERING SCORE   : {scorecard.overall_score:.2f}%")
    print(f"  CERTIFICATION TIER          : {scorecard.certification_tier.value}")
    print(f"  VERIFICATION STATUS         : {scorecard.status.value}")
    print(f"  EVIDENCE DIRECTORY          : {os.path.abspath(output_dir)}")
    print(f"  ARTIFACTS GENERATED         : {len(manifest.files)} files (SHA-256 verified)")
    print("=" * 80)

    return 0 if scorecard.overall_score >= 95.0 else 1


if __name__ == "__main__":
    sys.exit(main())
