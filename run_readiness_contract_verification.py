"""
Master CLI Runner for Enterprise Readiness Contract Architecture Verification (Part 3H.3.1)
Executes end-to-end certification, prints a rich summary table, and exports all 8 audit manifests.
"""
import sys
import time

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from app.platform_verification.readiness_contract.runtime.readiness_runtime import ReadinessRuntime
from app.platform_verification.readiness_contract.domain.models import ReadinessTier


def print_banner():
    print("=" * 80)
    print("  DOCUTASK AGENT — PART 3H.3.1: ENTERPRISE READINESS CONTRACT VERIFICATION")
    print("  Production Traffic Gatekeeper & Dependency Lifecycle Certification")
    print("=" * 80)
    print()


def main():
    print_banner()
    start_time = time.time()

    print("[*] Initializing Readiness Runtime & Subsystem Engines...")
    runtime = ReadinessRuntime(
        policy_path="readiness_policy.yaml",
        evidence_dir="readiness_verification"
    )

    print("[*] Executing Full Readiness Verification Protocol...")
    print("    -> Validating 6-State Readiness State Machine...")
    print("    -> Checking Standardized GET /ready Contract Schema...")
    print("    -> Evaluating Declarative Dependency Policy (Critical vs Degraded)...")
    print("    -> Testing 7-Step Startup Validation Sequence...")
    print("    -> Executing 4 Failure & Degradation Transition Scenarios...")
    print("    -> Verifying Kubernetes & Multi-Cloud Probe Orchestration...")
    print("    -> Auditing Sensitive Information Leak Controls...")
    print("    -> Exporting Prometheus Metrics & State Latencies...")
    print("    -> Generating Quality Scorecard & 8 Structured Audit Evidence Files...")

    results = runtime.execute_full_verification()
    duration = time.time() - start_time

    scorecard = results["scorecard"]

    print("\n" + "=" * 80)
    print("  VERIFICATION RESULTS SUMMARY")
    print("=" * 80)
    print(f"  Overall Score:        {scorecard.overall_readiness_score:.2f}% / 100.00%")
    print(f"  Certification Tier:   {scorecard.certification_tier.value}")
    print(f"  Certification Status: {scorecard.certification_verdict}")
    print(f"  Traffic Safe:         {'YES (Admitted)' if scorecard.traffic_admission_safe else 'NO (Withheld)'}")
    print(f"  Execution Time:       {duration:.2f}s")
    print("-" * 80)
    print("  CATEGORY BREAKDOWN (Weighted):")
    print(f"    - Contract Correctness (25%):        {scorecard.contract_correctness_score:>6.2f}%")
    print(f"    - State Model Quality (20%):         {scorecard.state_model_quality_score:>6.2f}%")
    print(f"    - Dependency Modeling (20%):         {scorecard.dependency_modeling_score:>6.2f}%")
    print(f"    - Failure Handling (15%):            {scorecard.failure_handling_score:>6.2f}%")
    print(f"    - Security & Zero-Leak (10%):        {scorecard.security_score:>6.2f}%")
    print(f"    - Observability & Metrics (10%):     {scorecard.observability_score:>6.2f}%")

    print("-" * 80)
    print("  AUDIT MANIFESTS GENERATED (in readiness_verification/):")
    for artifact_name, file_path in results["exported_files"].items():
        print(f"    [+] {artifact_name:<35} -> {file_path}")

    print("=" * 80)

    if scorecard.passed and scorecard.certification_tier == ReadinessTier.ENTERPRISE_READY:
        print(">>> SUCCESS: Platform has achieved ENTERPRISE READINESS CONTRACT CERTIFICATION.")
        print("    Traffic admission and isolation contracts are verified for production.")
        return 0
    else:
        print(">>> FAILURE: Platform failed to meet required certification threshold (95.0%).")
        return 1


if __name__ == "__main__":
    sys.exit(main())
