"""
Phase 3H.4.9: Enterprise Incident Recovery Verification Master CLI Runner
"""
import sys
import os
from app.platform_verification.incident_recovery_verification.runtime.recovery_verification_runtime import (
    RecoveryVerificationRuntime,
)


def main():
    print("=" * 80)
    print("DocuTask Agent — Phase 3H.4.9: Enterprise Incident Recovery Verification")
    print("=" * 80)
    print("Initializing recovery verification runtime and testing self-healing workflows...\n")

    runtime = RecoveryVerificationRuntime()
    results = runtime.run_all_verifications(output_dir="incident_recovery_verification")
    scorecard = results["scorecard"]

    print("-" * 80)
    print("ENTERPRISE INCIDENT RECOVERY SCORECARD")
    print("-" * 80)
    print(f"Overall Composite Score:        {scorecard.composite_score:.2f}%")
    print(f"Certification Tier:             {scorecard.tier.value}")
    print(f"Certification Verdict:          {'CERTIFIED' if scorecard.certified_enterprise_ready else 'REJECTED'}")
    print(f"Certified Enterprise Ready:     {'YES (PASSED)' if scorecard.certified_enterprise_ready else 'NO (FAILED)'}")
    print("-" * 80)
    print("CATEGORY BREAKDOWN:")
    print(f"  • Recovery Success Rate (20%)   : {scorecard.recovery_success_rate_score:.2f}%")
    print(f"  • Recovery Speed (20%)          : {scorecard.recovery_speed_score:.2f}%")
    print(f"  • Data Integrity (20%)          : {scorecard.data_integrity_score:.2f}%")
    print(f"  • Automation Safety (15%)       : {scorecard.automation_safety_score:.2f}%")
    print(f"  • Validation Quality (15%)      : {scorecard.validation_quality_score:.2f}%")
    print(f"  • Improvement Process (10%)     : {scorecard.improvement_process_score:.2f}%")
    print("-" * 80)
    print(f"Evidence manifests exported to 'incident_recovery_verification/' directory ({len(results['exported_files'])} files):")
    for f in sorted(results["exported_files"]):
        print(f"  - {os.path.basename(f)}")
    print("=" * 80)

    if scorecard.certified_enterprise_ready:
        print("[SUCCESS] Phase 3H.4.9 Enterprise Incident Recovery certified successfully.\n")
        sys.exit(0)
    else:
        print("[ERROR] Phase 3H.4.9 Enterprise Incident Recovery failed certification criteria.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
