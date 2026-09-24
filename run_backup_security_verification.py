"""
CLI Runner for Enterprise Backup Security Verification Framework.
Part 3G.2F — Backup Security, Encryption, Integrity, Access Control & Compliance.
"""
import sys
import logging

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from app.platform_verification.backup_security_verification.runtime.backup_security_runtime import (
    BackupSecurityVerificationRuntime,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("BackupSecurityCLI")


def main():
    print("=" * 80)
    print("   DOCUTASK AGENT -- ENTERPRISE BACKUP SECURITY VERIFICATION (PART 3G.2F)")
    print("=" * 80)
    print("Initiating comprehensive backup security, cryptographic tamper-resistance,")
    print("IAM penetration testing, WORM immutability, and compliance audits...\n")

    runtime = BackupSecurityVerificationRuntime()
    results = runtime.execute_full_security_verification(output_dir="evidence/backup_security_verification")

    scorecard = results["scorecard"]

    print("\n" + "=" * 80)
    print("                     SECURITY VERIFICATION RESULTS")
    print("=" * 80)
    print(f"Overall Security Quality Score:   {scorecard.composite_score:.2f} / 100.0")
    print(f"Certification Tier:               {scorecard.certification_tier.value}")
    print(f"Passed Certification:             {scorecard.passed}")
    print(f"Execution Duration:               {scorecard.execution_duration_ms:.2f} ms")
    print("-" * 80)
    print("CATEGORY BREAKDOWN:")
    categories = [
        ("Encryption Standards", scorecard.encryption_score, 0.25),
        ("Access Control & IAM", scorecard.access_control_score, 0.20),
        ("Integrity & Tamper Protection", scorecard.integrity_protection_score, 0.20),
        ("Key Management & KMS", scorecard.key_management_score, 0.15),
        ("Forensic Auditability", scorecard.auditability_score, 0.10),
        ("Regulatory Compliance", scorecard.compliance_score, 0.10),
    ]
    for cat_name, cat_score, weight in categories:
        print(f"  * {cat_name:<32} : {cat_score:6.2f} / 100 (Weight: {weight * 100:4.1f}%)")
    
    print("-" * 80)
    print("SUMMARY AUDIT INSIGHTS:")
    for key, val in scorecard.audit_metadata.items():
        print(f"  [+] {key:<28}: {val}")

    print("-" * 80)
    print(f"EVIDENCE ARTIFACTS GENERATED ({len(results['exported_manifest_paths'])}/14):")
    for name, path in results["exported_manifest_paths"].items():
        print(f"  * {name:<35} -> {path}")

    print("=" * 80)

    if scorecard.passed and scorecard.composite_score >= 95.0:
        print("\n>>> SUCCESS: ENTERPRISE BACKUP SECURITY CERTIFIED (TIER 1) <<<")
        return 0
    else:
        print("\n>>> FAILURE: BACKUP SECURITY REQUIREMENTS NOT MET <<<")
        return 1


if __name__ == "__main__":
    sys.exit(main())
