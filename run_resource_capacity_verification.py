"""
Master CLI Runner for Phase 3J.4: Resource Utilization & Capacity Engineering Verification Framework.

Executes all 11 verifiers (covering sub-phases 3J.4.1 through 3J.4.13),
computes 6-category weighted resource quality scoring,
exports all JSON reports and metadata manifest to `performance_verification/`,
and displays formatted SRE-grade terminal outputs.
"""

import sys
from datetime import datetime, timezone

from app.platform_verification.resource_capacity_engineering.runtime.resource_capacity_runtime import (
    ResourceCapacityRuntime,
)


def print_banner():
    print("=" * 80)
    print("  DOCUTASK AGENT -- RESOURCE UTILIZATION & CAPACITY ENGINEERING")
    print("  Phase 3J.4 Enterprise Verification Framework")
    print("=" * 80)
    print(f"  Execution Time: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("  Environment:    Dedicated Performance Staging Sandbox")
    print("=" * 80)
    print()


def main():
    print_banner()

    runtime = ResourceCapacityRuntime()
    print("[*] Starting full resource utilization & capacity engineering verification suite...")
    result = runtime.run_full_verification()

    reports = result["reports"]
    certification = result["certification"]
    exported_files = result["exported_files"]

    print("\n" + "-" * 80)
    print("  SUB-PHASE VERIFICATION RESULTS")
    print("-" * 80)

    for key, report in reports.items():
        status_symbol = "[PASS]" if report.status.value == "PASSED" else "[FAIL]"
        score_str = f"{report.score:5.1f}%"
        print(f"  {status_symbol}  |  {score_str}  |  {report.verifier_id:<36}  |  {len(report.checks)} checks")
        for check in report.checks:
            check_mark = "  * " if check.passed else "  X "
            print(f"    {check_mark} {check.name:<52} : {check.details}")

    print("\n" + "-" * 80)
    print("  6-CATEGORY RESOURCE QUALITY SCORING")
    print("-" * 80)
    for cat in certification.category_scores:
        bar_len = int(cat.score / 5)
        bar = "#" * bar_len + "-" * (20 - bar_len)
        print(f"  {cat.category:<25} [{bar}] {cat.score:5.1f}%  (Weight: {cat.weight*100:2.0f}%, Weighted: {cat.weighted_score:5.2f}%)")

    print("-" * 80)
    print(f"  COMPOSITE RESOURCE QUALITY SCORE:    {certification.overall_score:5.2f}%")
    print(f"  CERTIFICATION TIER:                  {certification.certification_tier.value}")
    print(f"  STATUS:                              {'PASSED' if certification.passed else 'FAILED'}")
    print("-" * 80)

    print("\n" + "-" * 80)
    print("  EXPORTED EVIDENCE MANIFESTS (performance_verification/)")
    print("-" * 80)
    for file_path in exported_files:
        print(f"  --> {file_path}")

    print("\n" + "=" * 80)
    if certification.passed:
        print("  >>> ENTERPRISE CAPACITY CERTIFICATION: GRANTED (Enterprise Capacity Ready) <<<")
        print("=" * 80 + "\n")
        return 0
    else:
        print("  >>> ENTERPRISE CAPACITY CERTIFICATION: REJECTED <<<")
        print("=" * 80 + "\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
