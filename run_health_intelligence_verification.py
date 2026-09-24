"""
Master CLI Runner for Enterprise Health State Transition & Service Recovery Intelligence (Part 3H.3.3)
Executes full verification, prints a rich summary scorecard, and exports all 8 audit manifests to health_verification/.
"""
import sys
import time

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from app.platform_verification.health_transition_intelligence.runtime.health_intelligence_runtime import HealthIntelligenceRuntime
from app.platform_verification.health_transition_intelligence.domain.models import HealthTier


def print_banner():
    print("=" * 80)
    print("  DOCUTASK AGENT — PART 3H.3.3: HEALTH STATE TRANSITION & RECOVERY INTELLIGENCE")
    print("  Continuous Degradation Detection, Flapping Prevention & Automated Recovery")
    print("=" * 80)
    print()


def main():
    print_banner()
    start_time = time.time()

    print("[*] Initializing Health Intelligence Runtime & Transition Engine...")
    runtime = HealthIntelligenceRuntime(
        rules_path="health_rules.yaml",
        evidence_dir="health_verification"
    )

    print("[*] Executing Full 15-Part Health Intelligence Protocol...")
    print("    -> 3H.3.3.1: Validating 5-State Lifecycle (STARTING -> READY <-> DEGRADED <-> NOT_READY -> RECOVERING)...")
    print("    -> 3H.3.3.2: Gathering Multidimensional Telemetry & Signal Snapshot...")
    print("    -> 3H.3.3.3: Evaluating Declarative Health Transition Rules (health_rules.yaml)...")
    print("    -> 3H.3.3.4: Performing Degradation Slope & Trend Confidence Analysis...")
    print("    -> 3H.3.3.5: Logging Lifecycle Transitions in Health History Storage...")
    print("    -> 3H.3.3.6: Validating Warm-Pool Prerequisites in RECOVERING State...")
    print("    -> 3H.3.3.7: Detecting & Dampening Rapid Health Flapping (Anti-Storm)...")
    print("    -> 3H.3.3.8: Validating Cascading Failure Circuit Breaker & Fallback...")
    print("    -> 3H.3.3.9: Orchestrating Automated Service Recovery Actions...")
    print("    -> 3H.3.3.10: Auditing Kubernetes Pod Routing & Probe Code Alignment...")
    print("    -> 3H.3.3.11: Generating Multi-Severity Alerts (Critical, Warning, Recovery)...")
    print("    -> 3H.3.3.12: Synthesizing Chronological Incident Timeline Manifest...")
    print("    -> 3H.3.3.13: Running 4 Chaos & Recovery Simulation Scenarios...")
    print("    -> 3H.3.3.14: Writing 8 Structured Audit Artifacts to health_verification/...")
    print("    -> 3H.3.3.15: Computing 6-Dimension Weighted Quality Scorecard...")

    results = runtime.execute_full_verification()
    duration = time.time() - start_time

    scorecard = results["scorecard"]

    print("\n" + "=" * 80)
    print("  VERIFICATION RESULTS SUMMARY")
    print("=" * 80)
    print(f"  Overall Score:        {scorecard.overall_score:.2f}% / 100.00%")
    print(f"  Certification Tier:   {scorecard.certification_tier.value}")
    print(f"  Certification Status: {scorecard.certification_verdict}")
    print(f"  Execution Time:       {duration:.2f}s")
    print("-" * 80)
    print("  CATEGORY BREAKDOWN (Weighted):")
    print(f"    - State Accuracy (25%):              {scorecard.state_accuracy_score:>6.2f}%")
    print(f"    - Transition Logic (20%):            {scorecard.transition_logic_score:>6.2f}%")
    print(f"    - Failure Detection (20%):           {scorecard.failure_detection_score:>6.2f}%")
    print(f"    - Recovery Validation (15%):         {scorecard.recovery_validation_score:>6.2f}%")
    print(f"    - Alerting (10%):                    {scorecard.alerting_score:>6.2f}%")
    print(f"    - Evidence Quality (10%):            {scorecard.evidence_quality_score:>6.2f}%")

    print("-" * 80)
    print("  AUDIT MANIFESTS GENERATED (in health_verification/):")
    for artifact_name, file_path in results["exported_files"].items():
        print(f"    [+] {artifact_name:<30} -> {file_path}")

    print("=" * 80)

    if scorecard.passed and scorecard.certification_tier == HealthTier.ENTERPRISE_READY:
        print(">>> SUCCESS: Platform has achieved ENTERPRISE HEALTH INTELLIGENCE CERTIFICATION.")
        print("    Continuous degradation tracking and recovery automation are verified for production.")
        return 0
    else:
        print(">>> FAILURE: Platform failed to meet required certification threshold (95.0%).")
        return 1


if __name__ == "__main__":
    sys.exit(main())
