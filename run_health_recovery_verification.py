"""
Phase 3H.5.12: Automated Health Recovery Verification Framework Master CLI Runner
"""
import sys
import os
from app.platform_verification.health_recovery.runtime.health_recovery_runtime import (
    HealthRecoveryRuntime,
)
from app.platform_verification.health_recovery.domain.models import (
    RecoveryCertificationTier,
)


def main():
    print("=" * 80)
    print("DocuTask Agent — Phase 3H.5.12: Automated Health Recovery Verification Framework")
    print("=" * 80)
    print("Executing self-healing pipelines, chaos tests, safety verifications, and recovery audits...\n")

    runtime = HealthRecoveryRuntime(output_dir="health_recovery_verification")
    results = runtime.run_full_recovery_verification()
    scorecard = results["scorecard"]
    transitions = results["transition_report"]
    detection = results["detection_report"]
    policy = results["policy_report"]
    components = results["component_report"]
    safety = results["safety_report"]
    self_healing = results["self_healing_report"]
    chaos = results["chaos_report"]
    validation = results["validation_report"]
    observability = results["observability_report"]
    security = results["security_report"]

    print("-" * 80)
    print("HEALTH RECOVERY & SELF-HEALING SCORECARD")
    print("-" * 80)
    print(f"Verification ID:                {scorecard.verification_id}")
    print(f"Overall Recovery Score:         {scorecard.overall_recovery_score:.2f}%")
    print(f"Certification Tier:             {scorecard.certification_tier.value}")
    print(f"Mean Time To Detect (MTTD):     {scorecard.mttd_seconds:.2f}s")
    print(f"Mean Time To Recover (MTTR):    {scorecard.mttr_seconds:.2f}s")
    print(f"Recovery Success Rate:          {scorecard.recovery_success_rate:.2f}%")
    print(f"Certified Recovery Ready:       {'YES (PASSED)' if scorecard.passed else 'NO (FAILED)'}")
    print("-" * 80)
    print("RECOVERY CAPABILITY SUMMARY:")
    print(f"  • State Transitions:           {transitions.valid_transitions_count}/{transitions.total_transitions_evaluated} valid ({transitions.invalid_transitions_rejected} invalid rejected)")
    print(f"  • Automated Failure Detection: {detection.detected_scenarios_count}/{detection.total_scenarios_tested} scenarios detected (MTTD: {detection.mean_time_to_detect_seconds:.2f}s)")
    print(f"  • Recovery Policies:           {len(policy.active_policies)} active policies with validated rollback strategies")
    print(f"  • Component Recovery:          {components.successful_recoveries_count}/{components.total_components_verified} components restored (API, DB, Redis, Worker, Gemini AI)")
    print(f"  • Recovery Safety:             {len(safety.safety_checks)} rules enforced (Infinite loop protection, backoff, blast-radius isolation)")
    print(f"  • Autonomous Self-Healing:     {self_healing.successful_self_heals}/{self_healing.total_workflows_tested} workflows restored with zero manual intervention")
    print(f"  • Recovery Chaos Testing:      {chaos.passed_experiments_count}/{chaos.total_chaos_experiments} experiments passed (DB drop, worker SIGKILL, queue partitions)")
    print(f"  • Post-Recovery Validation:    {validation.passed_probes_count}/{validation.total_probes_executed} functional probes confirmed health restoration")
    print(f"  • Observability Telemetry:     {len(observability.metrics)} Prometheus metrics active; recovery dashboard operational")
    print(f"  • Recovery Security:           {security.authorized_actions_count} authorized actions logged; {security.unauthorized_actions_blocked} unauthorized attempts blocked")
    print("-" * 80)
    print("6-PILLAR WEIGHTED OPERATIONAL READINESS:")
    for pillar in scorecard.pillar_scores:
        print(f"  • {pillar.pillar_name:<28} ({pillar.weight * 100:.0f}%): {pillar.raw_score:.2f}% (Weighted: {pillar.weighted_score:.2f}%) [{pillar.status}]")
    print("-" * 80)
    print(f"Standardized evidence repository exported to 'health_recovery_verification/' ({len(results['exported_files'])} artifacts):")
    for filename in sorted(results["exported_files"].keys()):
        print(f"  - {filename}")
    print("=" * 80)

    if scorecard.passed and scorecard.overall_recovery_score >= 90.0:
        print("[SUCCESS] Phase 3H.5.12 Automated Health Recovery Verification PASSED.\n")
        sys.exit(0)
    else:
        print("[ERROR] Phase 3H.5.12 Verification FAILED to meet required recovery thresholds.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
