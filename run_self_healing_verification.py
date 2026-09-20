"""
Phase 3H.5.5: Enterprise Health Self-Healing & Automated Recovery Verification Master CLI Runner
"""
import sys
import os
from app.platform_verification.self_healing_verification.runtime.self_healing_runtime import (
    SelfHealingRuntime,
)
from app.platform_verification.self_healing_verification.domain.models import SelfHealingTier


def main():
    print("=" * 80)
    print("DocuTask Agent — Phase 3H.5.5: Enterprise Self-Healing & Automated Recovery")
    print("=" * 80)
    print("Executing 5-layer automated recovery validation, policy verification, and scorecard...\n")

    runtime = SelfHealingRuntime()
    results = runtime.run_full_self_healing_verification(output_dir="self_healing_verification")
    scorecard = results["scorecard"]
    val_report = results["validation_report"]
    exec_report = results["execution_report"]

    print("-" * 80)
    print("ENTERPRISE SELF-HEALING & RECOVERY SCORECARD")
    print("-" * 80)
    print(f"Overall Composite Score:        {scorecard.composite_score:.2f}%")
    print(f"Self-Healing Maturity Tier:     {scorecard.tier.value}")
    print(f"5-Layer Recovery Accepted:      {'YES (PASSED)' if val_report.recovery_accepted else 'NO (FAILED)'}")
    print(f"Certified Enterprise Ready:     {'YES (CERTIFIED)' if scorecard.certified_enterprise_ready else 'NO (FAILED)'}")
    print("-" * 80)
    print("RECOVERY VALIDATION (5 LAYERS):")
    print(f"  • Layer 1 (Service Health):   {'PASSED' if val_report.layer1_health.all_health_passed else 'FAILED'}")
    print(f"  • Layer 2 (Dependencies):     {'PASSED' if val_report.layer2_dependency.all_restored else 'FAILED'} ({len(val_report.layer2_dependency.dependencies)}/5 healthy)")
    print(f"  • Layer 3 (Workflow E2E):     {'PASSED' if val_report.layer3_workflow.business_workflow_passed else 'FAILED'} (Doc ID: {val_report.layer3_workflow.document_id})")
    print(f"  • Layer 4 (Performance):      {'PASSED' if val_report.layer4_performance.performance_restored else 'FAILED'} (Ratio: {val_report.layer4_performance.recovery_performance_ratio:.2f}x <= 1.20x)")
    print(f"  • Layer 5 (Stability Window): {'PASSED' if val_report.layer5_stability.overall_stability_passed else 'FAILED'} (5m/30m/1h horizons)")
    print("-" * 80)
    print("SCORECARD PILLARS:")
    print(f"  • Detection & Classification (20%): {scorecard.recovery_detection_score:.2f}%")
    print(f"  • Execution & Orchestration  (20%): {scorecard.recovery_execution_score:.2f}%")
    print(f"  • Validation Accuracy        (25%): {scorecard.validation_accuracy_score:.2f}%")
    print(f"  • Workflow Recovery          (20%): {scorecard.business_workflow_recovery_score:.2f}%")
    print(f"  • Evidence Quality           (10%): {scorecard.evidence_quality_score:.2f}%")
    print(f"  • Security & Isolation        (5%): {scorecard.security_controls_score:.2f}%")
    print("-" * 80)
    print(f"Standardized evidence repository exported to 'self_healing_verification/' ({len(results['exported_files'])} artifacts):")
    for f in sorted(results["exported_files"]):
        print(f"  - {os.path.relpath(f, 'self_healing_verification')}")
    print("=" * 80)

    if scorecard.certified_enterprise_ready and scorecard.composite_score >= 90.0:
        print("[SUCCESS] Phase 3H.5.5 Self-Healing & Automated Recovery Verification PASSED.\n")
        sys.exit(0)
    else:
        print("[ERROR] Phase 3H.5.5 Self-Healing Verification FAILED to meet enterprise thresholds.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
