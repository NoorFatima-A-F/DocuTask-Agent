"""
Master CLI Runner for Phase 3O: Enterprise Infrastructure Quality Scoring, Certification & Readiness Assessment.

Orchestrates automated evidence collection, 6-pillar SRE quality scoring, risk evaluation,
operational maturity assessment, regression detection, and signed artifact export.
"""

import os
import sys
from pathlib import Path

from app.platform_verification.enterprise_infrastructure_certification.runtime.infrastructure_certification_runtime import (
    InfrastructureCertificationRuntime,
)


def main() -> int:
    output_dir = "infrastructure_certification"
    print("=" * 80)
    print("  DocuTask Agent - Enterprise Infrastructure Certification & Quality Scoring")
    print("  Phase 3O Quality, Risk & Production Readiness Assessment Framework")
    print("=" * 80)
    print()

    runtime = InfrastructureCertificationRuntime()

    print("[*] Collecting and normalizing multi-phase infrastructure verification evidence...")
    result = runtime.run_full_certification(export_dir=output_dir)
    scorecard = result["scorecard"]
    decision = result["decision"]
    risk_report = result["risk_report"]
    maturity = result["maturity"]
    regression = result["regression"]
    manifest = result["manifest"]

    print()
    print("-" * 80)
    print("  INFRASTRUCTURE QUALITY PILLARS BREAKDOWN (6 CORE SRE DOMAINS)")
    print("-" * 80)

    for cat_name, cat in scorecard.categories.items():
        weight_pct = int(cat.weight * 100)
        tag = "[PASS]" if cat.status.value == "PASSED" else "[FAIL]"
        print(
            f"  {tag} {cat_name:<25} [Weight: {weight_pct:2d}%] Score: {cat.score:6.2f}% | Contribution: {cat.contribution:5.2f}%"
        )

    print()
    print("-" * 80)
    print("  OPERATIONAL MATURITY & RISK SUMMARY")
    print("-" * 80)
    print(f"  - Maturity Level           : {maturity.maturity_level.value}")
    print(f"  - Highest Detected Risk    : {risk_report.highest_risk.value}")
    print(f"  - Critical / High Risks    : {risk_report.critical_risks_count} Critical, {risk_report.high_risks_count} High")
    print(f"  - Production Blocker       : {'YES' if risk_report.production_blocker_present else 'NO (Zero Blockers)'}")
    print(f"  - Regression Delta         : {'+' if regression.score_delta >= 0 else ''}{regression.score_delta:.2f}% (Status: {'REGRESSION' if regression.regression_detected else 'CLEAN'})")

    print()
    print("=" * 80)
    print(f"  OVERALL INFRASTRUCTURE SCORE  : {scorecard.overall_score:.2f} / 100.0")
    print(f"  CERTIFICATION LEVEL           : {decision.certification.value}")
    print(f"  PRODUCTION DEPLOYMENT GATE    : {'APPROVED' if decision.deployment_approved else 'BLOCKED'}")
    print(f"  EVIDENCE REPOSITORY           : {os.path.abspath(output_dir)}")
    print(f"  ARTIFACTS GENERATED           : {len(manifest.files)} files (Cryptographic SHA-256 verified)")
    print(f"  READINESS REPORT (MARKDOWN)   : {os.path.abspath(os.path.join(output_dir, 'Infrastructure_Readiness_Report.md'))}")
    print("=" * 80)

    return 0 if decision.deployment_approved else 1


if __name__ == "__main__":
    sys.exit(main())
