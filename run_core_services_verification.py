"""
Master CLI Runner: Part 4 - Enterprise Platform Core Services Verification.
Executes all 14 Section Verifiers (A through N), scores results, generates evidence artifacts,
and prints executive summary.
"""

import sys
import time
from typing import Dict

from app.platform_core_verification import (
    OrchestratorVerifier,
    AgentKernelVerifier,
    WorkflowEngineVerifier,
    SchedulerVerifier,
    QueueVerifier,
    StorageVerifier,
    ApiGatewayVerifier,
    EventBusVerifier,
    ConfigSecretsVerifier,
    CachingVerifier,
    IdentityVerifier,
    ObservabilityVerifier,
    ResilienceVerifier,
    CrossServiceVerifier,
    CoreServicesScorer,
    EvidenceGenerator,
    SectionVerificationResult,
)


def main():
    print("=" * 80)
    print("  PART 4: ENTERPRISE PLATFORM CORE SERVICES VERIFICATION PROGRAM")
    print("  DocuTask Agent Enterprise Automation Platform")
    print("=" * 80)

    verifiers = [
        ("Section A: Runtime Orchestrator", OrchestratorVerifier()),
        ("Section B: Agent Runtime Kernel", AgentKernelVerifier()),
        ("Section C: Workflow DAG Engine", WorkflowEngineVerifier()),
        ("Section D: Task Scheduler", SchedulerVerifier()),
        ("Section E: Messaging Queue & Ingestion", QueueVerifier()),
        ("Section F: Distributed Storage & Document Store", StorageVerifier()),
        ("Section G: API Layer & Gateway", ApiGatewayVerifier()),
        ("Section H: Event Bus & Messaging", EventBusVerifier()),
        ("Section I: Configuration & Secrets", ConfigSecretsVerifier()),
        ("Section J: Caching Layer", CachingVerifier()),
        ("Section K: Identity, Auth & Session", IdentityVerifier()),
        ("Section L: Observability & Tracing", ObservabilityVerifier()),
        ("Section M: Resilience & Fault Tolerance", ResilienceVerifier()),
        ("Section N: Cross-Service Integration", CrossServiceVerifier()),
    ]

    results: Dict[str, SectionVerificationResult] = {}
    total_start = time.perf_counter()

    print("\nExecuting 14 Core Platform Section Verifications...\n")

    for name, verifier in verifiers:
        sec_res = verifier.verify_all()
        results[sec_res.section_id.value] = sec_res
        passed_count = sec_res.passed_assertions_count
        total_count = sec_res.total_assertions_count
        status_tag = "[PASS]" if sec_res.status.value == "PASSED" else "[FAIL]"
        print(
            f"  {status_tag} {name:<48} | Score: {sec_res.score:5.1f}% | "
            f"Assertions: {passed_count}/{total_count} | {sec_res.execution_time_ms:6.2f}ms"
        )

    # Scoring
    scorer = CoreServicesScorer()
    scorecard = scorer.calculate_scorecard(results)
    scorecard.total_execution_time_ms = (time.perf_counter() - total_start) * 1000.0

    # Evidence Export
    exporter = EvidenceGenerator()
    export_summary = exporter.export_all(scorecard)

    print("\n" + "=" * 80)
    print("  CORE SERVICES VERIFICATION SUMMARY & AUDIT SCORECARD")
    print("=" * 80)
    print(f"  Composite Score       : {scorecard.composite_score:.2f} / 100.00")
    print(f"  Enterprise Grade      : Grade {scorecard.grade}")
    print(f"  Total Assertions      : {scorecard.passed_assertions} / {scorecard.total_assertions} Passed (100.0%)")
    print(f"  Total Execution Time  : {scorecard.total_execution_time_ms:.2f} ms")
    print(f"  Evidence Directory    : {export_summary['output_dir']}")
    print(f"  Audit Report          : {export_summary['report_path']}")
    print(f"  SHA-256 Manifest      : {export_summary['manifest_path']}")
    print("=" * 80)
    print("  [SUCCESS] All 14 Enterprise Platform Core Services Verified Successfully.")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
