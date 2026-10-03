"""
Master CLI Runner for Enterprise Dependency-Aware Readiness Decision Engine Verification (Part 3H.3.2)
Executes full verification, prints a rich summary table, and exports all 8 audit manifests to health_verification/.
"""
import sys
import time

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from app.platform_verification.readiness_engine.runtime.readiness_engine_runtime import ReadinessEngineRuntime
from app.platform_verification.readiness_engine.domain.models import ReadinessTier


def print_banner():
    print("=" * 80)
    print("  DOCUTASK AGENT — PART 3H.3.2: DEPENDENCY-AWARE READINESS DECISION ENGINE")
    print("  Production Traffic Gatekeeper & Distributed Dependency Intelligence")
    print("=" * 80)
    print()


def main():
    print_banner()
    start_time = time.time()

    print("[*] Initializing Readiness Engine Runtime & Subsystem Checkers...")
    runtime = ReadinessEngineRuntime(
        policy_path="dependency_policy.yaml",
        evidence_dir="health_verification"
    )

    print("[*] Executing Full 14-Part Readiness Verification Protocol...")
    print("    -> 3H.3.2.1: Validating 6-State Operational Model (STARTING -> READY <-> DEGRADED <-> NOT_READY)...")
    print("    -> 3H.3.2.2: Evaluating Declarative Dependency Policy & Criticality Matrix...")
    print("    -> 3H.3.2.3: Checking Database Connectivity, Transactions & Connection Pool...")
    print("    -> 3H.3.2.4: Checking Redis Availability (PING/PONG) & Queue Pressure...")
    print("    -> 3H.3.2.5: Verifying Document Storage Write/Read/Integrity Lifecycle...")
    print("    -> 3H.3.2.6: Verifying Gemini AI Auth, Quota Headroom & Degraded Queuing...")
    print("    -> 3H.3.2.7: Verifying Worker Fleet Registration, Heartbeats & Capacity...")
    print("    -> 3H.3.2.8: Executing Readiness Aggregation Engine & Traffic Routing Decisions...")
    print("    -> 3H.3.2.9: Executing 4 Controlled Fault Injection Scenarios...")
    print("    -> 3H.3.2.10: Auditing Kubernetes readinessProbe Spec & Deterministic Response...")
    print("    -> 3H.3.2.11: Performing Zero-Information-Leakage Security Scan...")
    print("    -> 3H.3.2.12: Exporting Prometheus Observability Metrics...")
    print("    -> 3H.3.2.13: Writing 8 Structured Audit Artifacts to health_verification/...")
    print("    -> 3H.3.2.14: Computing 6-Dimension Weighted Quality Scorecard...")

    results = runtime.execute_full_verification()
    duration = time.time() - start_time

    scorecard = results["scorecard"]
    eval_result = results["eval_result"]

    print("\n" + "=" * 80)
    print("  VERIFICATION RESULTS SUMMARY")
    print("=" * 80)
    print(f"  Overall Score:        {scorecard.overall_readiness_score:.2f}% / 100.00%")
    print(f"  Certification Tier:   {scorecard.certification_tier.value}")
    print(f"  Certification Status: {scorecard.certification_verdict}")
    print(f"  Service State:        {eval_result.state.value}")
    print(f"  Traffic Decision:     {eval_result.traffic_action.value} ({'Allowed' if eval_result.traffic_allowed else 'Rejected'})")
    print(f"  Execution Time:       {duration:.2f}s")
    print("-" * 80)
    print("  CATEGORY BREAKDOWN (Weighted):")
    print(f"    - Dependency Detection (25%):        {scorecard.dependency_detection_score:>6.2f}%")
    print(f"    - Failure Accuracy (20%):            {scorecard.failure_accuracy_score:>6.2f}%")
    print(f"    - Policy Correctness (20%):          {scorecard.policy_correctness_score:>6.2f}%")
    print(f"    - Kubernetes Compatibility (15%):    {scorecard.kubernetes_compatibility_score:>6.2f}%")
    print(f"    - Security & Zero-Leak (10%):        {scorecard.security_score:>6.2f}%")
    print(f"    - Observability & Metrics (10%):     {scorecard.observability_score:>6.2f}%")

    print("-" * 80)
    print("  AUDIT MANIFESTS GENERATED (in health_verification/):")
    for artifact_name, file_path in results["exported_files"].items():
        print(f"    [+] {artifact_name:<30} -> {file_path}")

    print("=" * 80)

    if scorecard.passed and scorecard.certification_tier == ReadinessTier.ENTERPRISE_READY:
        print(">>> SUCCESS: Platform has achieved ENTERPRISE READINESS CERTIFICATION.")
        print("    Dependency-aware traffic admission gatekeeper is verified for production.")
        return 0
    else:
        print(">>> FAILURE: Platform failed to meet required certification threshold (95.0%).")
        return 1


if __name__ == "__main__":
    sys.exit(main())
