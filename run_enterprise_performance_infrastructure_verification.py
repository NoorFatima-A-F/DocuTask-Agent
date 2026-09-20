"""Master CLI Runner for Phase 3J.6 Enterprise Performance Infrastructure Verification.

Executes all 13 verification phases, calculates weighted scores across 5 quality categories,
and exports JSON reports with cryptographic SHA-256 integrity manifest to performance_verification/.
"""

import asyncio
import os
import sys

from app.platform_verification.enterprise_performance_infrastructure.domain.models import (
    PerformanceVerificationStatus,
)
from app.platform_verification.enterprise_performance_infrastructure.runtime.performance_infrastructure_runtime import (
    PerformanceInfrastructureRuntime,
)


async def main() -> int:
    output_dir = "performance_verification"
    print("=" * 80)
    print("  DocuTask Agent - Enterprise Performance Infrastructure Verification")
    print("  Phase 3J.6 Verification & SRE Engineering Suite")
    print("=" * 80)
    print()

    runtime = PerformanceInfrastructureRuntime()

    print("[*] Initializing 13 verification phases...")
    manifest = await runtime.run_all(output_dir=output_dir)

    print()
    print("-" * 80)
    print("  VERIFICATION PHASES EXECUTION SUMMARY")
    print("-" * 80)

    import json

    for filename in sorted(manifest.reports_generated):
        if filename.endswith(".json") and filename not in ("metadata.json", "certification_report.json"):
            filepath = os.path.join(output_dir, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                phase_id = data.get("phase_id", "N/A")
                title = data.get("phase_name") or data.get("report_title", filename)
                score = data.get("score", 100.0)
                status = data.get("status", "PASSED")
                tag = "[PASS]" if status in ("PASSED", "passed") else "[FAIL]"
                print(f"  {tag} Phase {phase_id:<8} : {title:<55} (Score: {score:.1f}%)")
            except Exception:
                pass

    print()
    print("-" * 80)
    print("  CATEGORY QUALITY BREAKDOWN (5 DIMENSIONS)")
    print("-" * 80)

    cert_path = os.path.join(output_dir, "certification_report.json")
    if os.path.exists(cert_path):
        with open(cert_path, "r", encoding="utf-8") as f:
            cert_data = json.load(f)
        for cat in cert_data.get("category_scores", []):
            name = cat.get("category", "")
            weight = cat.get("weight", 0.0) * 100
            score = cat.get("score", 0.0)
            weighted = cat.get("weighted_score", 0.0)
            print(f"  - {name:<26} [Weight: {weight:>2.0f}%] Score: {score:>6.2f}% | Contribution: {weighted:>5.2f}%")

    print()
    print("=" * 80)
    print(f"  OVERALL PERFORMANCE SCORE : {manifest.overall_score:.2f}%")
    print(f"  CERTIFICATION TIER        : {manifest.certification_tier}")
    print(f"  VERIFICATION STATUS       : {'PASSED' if manifest.passed else 'FAILED'}")
    print(f"  ARTIFACTS DIRECTORY       : {os.path.abspath(output_dir)}")
    print(f"  REPORTS GENERATED         : {len(manifest.reports_generated)} files (SHA-256 verified)")
    print("=" * 80)

    return 0 if manifest.passed else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
