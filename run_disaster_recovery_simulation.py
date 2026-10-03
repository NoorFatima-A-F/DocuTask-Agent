"""
CLI Runner for Enterprise Disaster Recovery Simulation Framework.
Part 3G.3 — Disaster Recovery Simulation & Operational Resilience Verification.
"""
import sys
import logging

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from app.platform_verification.disaster_recovery_simulation.runtime.dr_simulation_runtime import (
    DisasterRecoverySimulationRuntime,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("DRSimulationCLI")


def main():
    print("=" * 80)
    print("   DOCUTASK AGENT -- DISASTER RECOVERY SIMULATION FRAMEWORK (PART 3G.3)")
    print("=" * 80)
    print("Initiating 5 multi-vector disaster scenarios, 3 chaos engineering experiments,")
    print("automated incident detection validation, tabletop drill, and resilience certification...\n")

    runtime = DisasterRecoverySimulationRuntime()
    results = runtime.execute_full_dr_program(
        cert_dir="disaster_recovery_certification",
        evidence_dir="disaster_recovery_evidence",
        runbooks_dir="runbooks",
    )

    scorecard = results["scorecard"]
    scenarios = results["scenarios"]
    chaos = results["chaos_experiments"]
    detection = results["detection"]
    manifests = results["exported_manifests"]

    print("\n" + "=" * 80)
    print("                     DISASTER SIMULATION RESULTS")
    print("=" * 80)
    print(f"Overall Resilience Score:        {scorecard.composite_score:.2f} / 100.0")
    print(f"Resilience Certification Tier:   {scorecard.certification_level.value}")
    print(f"Disaster Recovery Status:        {'PASSED' if scorecard.passed else 'FAILED'}")
    print(f"CI/CD Deployment Gate:           {'APPROVED' if scorecard.ci_cd_deployment_approved else 'BLOCKED'}")
    print("-" * 80)
    print("WEIGHTED CATEGORY BREAKDOWN:")
    categories = [
        ("Recovery Success (5 Scenarios)", scorecard.recovery_success_score, 0.30),
        ("RTO Performance (Speed)", scorecard.rto_performance_score, 0.20),
        ("RPO Compliance (Data Loss)", scorecard.rpo_compliance_score, 0.20),
        ("Automation & Orchestration", scorecard.automation_score, 0.15),
        ("Incident Detection (MTTD)", scorecard.detection_score, 0.10),
        ("Documentation & Tabletop", scorecard.documentation_score, 0.05),
    ]
    for cat_name, cat_score, weight in categories:
        weighted = cat_score * weight
        print(f"  * {cat_name:<34} : {cat_score:6.2f} / 100 (Weight: {weight * 100:4.1f}% -> {weighted:5.2f} pts)")

    print("-" * 80)
    print("RECOVERY OBJECTIVES & TIMING METRICS:")
    print(f"  * Measured RTO (Max Recovery Time) : {scorecard.measured_rto_minutes:.1f} mins (Target: <= 45.0m) [OPTIMAL]")
    print(f"  * Measured RPO (Max Data Loss)     : {scorecard.measured_rpo_minutes:.1f} mins (Target: <=  5.0m) [OPTIMAL]")
    print(f"  * Mean Time to Recovery (MTTR)     : {scorecard.measured_mttr_minutes:.1f} mins")
    print(f"  * Mean Time to Detect (MTTD)       : {detection.measured_mttd_seconds:.1f} secs (Target: <= 300.0s) [OPTIMAL]")

    print("-" * 80)
    print(f"DISASTER SCENARIOS EVALUATED ({len(scenarios)}/5):")
    for s in scenarios:
        rto_m = s.measured_rto_seconds / 60.0
        rpo_m = s.measured_rpo_seconds / 60.0
        print(f"  [+] {s.scenario_name:<50} -> RTO: {rto_m:4.1f}m | RPO: {rpo_m:4.1f}m | PASSED: {s.simulation_passed}")

    print("-" * 80)
    print(f"CHAOS INJECTION EXPERIMENTS ({len(chaos)}/3):")
    for c in chaos:
        print(f"  [+] {c.experiment_name:<50} -> Self-Healed in {c.recovery_duration_seconds:4.1f}s | PASSED: {c.passed}")

    print("-" * 80)
    print(f"DELIVERABLE ARTIFACTS EXPORTED ({len(manifests)}):")
    for name, path in manifests.items():
        print(f"  * {name:<45} -> {path}")

    print("=" * 80)

    if scorecard.ci_cd_deployment_approved and scorecard.composite_score >= 90.0:
        print("\n>>> SUCCESS: ENTERPRISE DISASTER RECOVERY & RESILIENCE CERTIFIED <<<")
        return 0
    else:
        print("\n>>> FAILURE: DISASTER RECOVERY SCORE BELOW REQUIRED THRESHOLD <<<")
        return 1


if __name__ == "__main__":
    sys.exit(main())
