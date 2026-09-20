"""
CLI Runner for Enterprise Backup Certification Framework.
Part 3G.2G — Backup Readiness Certification System for DocuTask Agent.
"""
import sys
import os
import json
import logging

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from app.platform_verification.backup_certification.runtime.backup_certification_runtime import (
    BackupCertificationRuntime,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("BackupCertificationCLI")


def main():
    print("=" * 80)
    print("   DOCUTASK AGENT -- ENTERPRISE BACKUP CERTIFICATION FRAMEWORK (PART 3G.2G)")
    print("=" * 80)
    print("Initiating automated multi-source evidence collection, weighted readiness scoring,")
    print("RTO/RPO SLA certification, risk register analysis, and CI/CD quality gate check...\n")

    runtime = BackupCertificationRuntime()
    results = runtime.execute_full_certification(output_dir="backup_certification")

    scorecard = results["scorecard"]
    rto_rpo = results["rto_rpo"]
    risks = results["risks"]
    manifests = results["manifests"]

    print("\n" + "=" * 80)
    print("                     BACKUP CERTIFICATION RESULTS")
    print("=" * 80)
    print(f"Overall Certification Score:     {scorecard.overall_score:.2f} / 100.0")
    print(f"Certification Tier:              {scorecard.certification_level.value}")
    print(f"Readiness Status:                {'PASSED' if scorecard.passed else 'FAILED'}")
    print(f"CI/CD Deployment Gate:           {'APPROVED' if scorecard.ci_cd_deployment_approved else 'BLOCKED'}")
    print("-" * 80)
    print("WEIGHTED CATEGORY BREAKDOWN:")
    categories = [
        ("Backup Completeness", scorecard.backup_completeness, 0.20),
        ("Restore Success & Speed", scorecard.restore_success, 0.25),
        ("Data Integrity & Hashing", scorecard.integrity, 0.15),
        ("Security & Immutability", scorecard.security, 0.15),
        ("Automation Cadence", scorecard.automation, 0.10),
        ("Monitoring & Alerting", scorecard.monitoring, 0.10),
        ("Documentation & Runbooks", scorecard.documentation, 0.05),
    ]
    for cat_name, cat_score, weight in categories:
        weighted = cat_score * weight
        print(f"  * {cat_name:<32} : {cat_score:6.2f} / 100 (Weight: {weight * 100:4.1f}% -> {weighted:5.2f} pts)")
    
    print("-" * 80)
    print("RECOVERY OBJECTIVES (RTO / RPO):")
    print(f"  * Measured RTO : {rto_rpo.measured_rto_minutes:.1f} mins (Target: <= {rto_rpo.target_rto_minutes:.1f} mins) [{rto_rpo.rto_status}]")
    print(f"  * Measured RPO : {rto_rpo.measured_rpo_minutes:.1f} mins (Target: <= {rto_rpo.target_rpo_minutes:.1f} mins) [{rto_rpo.rpo_status}]")

    print("-" * 80)
    print(f"RISK REGISTER SUMMARY ({risks.total_risks_identified} Total Monitored Risks):")
    print(f"  * Critical: {risks.critical_risks_count} | High: {risks.high_risks_count} | Medium: {risks.medium_risks_count} | Low/Mitigated: {risks.low_risks_count}")
    print(f"  * Status: {risks.summary}")

    print("-" * 80)
    print(f"CERTIFICATION ARTIFACTS EXPORTED ({len(manifests)}/14):")
    for name, path in manifests.items():
        print(f"  * {name:<38} -> {path}")

    print("=" * 80)

    if scorecard.ci_cd_deployment_approved and scorecard.overall_score >= 90.0:
        print("\n>>> SUCCESS: ENTERPRISE BACKUP READINESS CERTIFIED (DEPLOYMENT APPROVED) <<<")
        return 0
    else:
        print("\n>>> FAILURE: BACKUP CERTIFICATION THRESHOLD NOT MET (DEPLOYMENT BLOCKED) <<<")
        return 1


if __name__ == "__main__":
    sys.exit(main())
