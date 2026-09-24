"""
Master CLI Runner for Part 3G.5:
Enterprise Operational Resilience & Recovery Automation Verification Framework.
"""
import sys

# Ensure UTF-8 output encoding on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from app.platform_verification.operational_resilience.runtime.resilience_runtime import (
    ResilienceRuntime,
)


def run_operational_resilience_cli():
    print("=" * 80)
    print("  PART 3G.5: OPERATIONAL RESILIENCE & RECOVERY AUTOMATION VERIFICATION")
    print("=" * 80)
    print("Initializing Enterprise Operational Resilience Verification Engine...")

    runtime = ResilienceRuntime(base_dir=".")
    result = runtime.execute_resilience_verification(export_artifacts=True)

    print("\n" + "-" * 80)
    print(" 1. FAILURE INJECTION EXPERIMENTS (Part 3G.5C - 7 Experiments)")
    print("-" * 80)
    for exp in result.experiments:
        print(f"  [{exp.status}] {exp.experiment_id:<16} | {exp.category.value:<14} | {exp.target_component:<26} (MTTD: {exp.detection_time_seconds:>4.1f}s, MTTR: {exp.recovery_duration_seconds:>4.1f}s, Loss: {exp.data_loss})")

    print("\n" + "-" * 80)
    print(" 2. SELF-HEALING SYSTEM VERIFICATION (Part 3G.5B)")
    print("-" * 80)
    print(f"Container Self-Healing:      {'[PASS]' if result.self_healing.container_healing_passed else '[FAIL]'} (Restart: {result.self_healing.container_restart_time_sec}s)")
    print(f"Queue Self-Healing:          {'[PASS]' if result.self_healing.queue_healing_passed else '[FAIL]'} ({result.self_healing.queue_messages_preserved_pct}% messages durable)")
    print(f"DB Connection Recovery:      {'[PASS]' if result.self_healing.db_connection_recovery_passed else '[FAIL]'} (Reconnect: {result.self_healing.db_reconnect_time_sec}s)")
    print(f"Measured MTTD:               {result.self_healing.mttd_seconds}s (Target < 30s)")
    print(f"Measured MTTR:               {result.self_healing.mttr_seconds}s (Target < 300s)")
    print(f"Recovery Success Rate:       {result.self_healing.recovery_success_rate_pct}% (Target > 99%)")

    print("\n" + "-" * 80)
    print(" 3. RECOVERY ORCHESTRATION & INCIDENT AUTOMATION (Part 3G.5A/D)")
    print("-" * 80)
    print(f"Recovery Workflows Passed:   {result.orchestrator_report.get('all_workflows_passed', False)}")
    print(f"Incidents Auto-Created:      {result.incidents.tickets_auto_created} / {result.incidents.total_incidents_simulated}")
    print(f"On-Call Paging Verified:     {result.incidents.paged_oncall_verified}")
    print(f"Average Incident MTTD / MTTR:{result.incidents.average_mttd_seconds}s / {result.incidents.average_mttr_seconds}s")

    print("\n" + "-" * 80)
    print(" 4. EXECUTABLE RUNBOOK AUTOMATION (Part 3G.5E - 6 Runbooks)")
    print("-" * 80)
    print(f"Total Runbooks Validated:    {result.runbooks.total_runbooks}")
    print(f"Automated CLI Supported:     {result.runbooks.automated_runbooks_count} / {result.runbooks.total_runbooks} (100% Automated)")
    for rb in result.runbooks.runbooks:
        print(f"  - [{rb.validation_status}] {rb.runbook_id}: {rb.title}")

    print("\n" + "-" * 80)
    print(" 5. DEPENDENCY RESILIENCE & STATE CONSISTENCY (Part 3G.5F/G)")
    print("-" * 80)
    print(f"AI Provider Fallback:        {'[PASS]' if result.dependencies.ai_provider_fallback_passed else '[FAIL]'}")
    print(f"Storage Upload Buffer:       {'[PASS]' if result.dependencies.storage_degradation_handled else '[FAIL]'}")
    print(f"Queue Task Preservation:     {result.dependencies.queue_preservation_pct}%")
    print(f"State Invariant Violations:  {result.consistency.corrupted_states_detected}")
    print(f"Duplicate Ingestions:        {result.consistency.duplicate_executions_detected}")
    print(f"Transaction Rollbacks:       {'[VERIFIED]' if result.consistency.transaction_rollback_verified else '[FAILED]'}")

    print("\n" + "-" * 80)
    print(" 6. AUTOMATED DR DRILL RESULT (Part 3G.5H)")
    print("-" * 80)
    print(f"Drill Name:                  {result.drill.drill_name}")
    print(f"Failure Injected:            {result.drill.injected_failure}")
    print(f"Measured RTO / Data Loss:    {result.drill.rto_seconds}s / {result.drill.data_loss_bytes} bytes")
    print(f"Drill Score:                 {result.drill.drill_score} / 100.0")

    print("\n" + "=" * 80)
    print(" OPERATIONAL RESILIENCE SCORECARD SUMMARY (Part 3G.5I)")
    print("=" * 80)
    print(f"  Detection Score (20%):            {result.scorecard.detection_score:>6.2f} / 100.0")
    print(f"  Recovery Automation (25%):        {result.scorecard.recovery_automation_score:>6.2f} / 100.0")
    print(f"  Data Integrity (20%):             {result.scorecard.data_integrity_score:>6.2f} / 100.0")
    print(f"  Failure Containment (15%):        {result.scorecard.failure_containment_score:>6.2f} / 100.0")
    print(f"  Operational Visibility (10%):     {result.scorecard.operational_visibility_score:>6.2f} / 100.0")
    print(f"  Documentation (10%):              {result.scorecard.documentation_score:>6.2f} / 100.0")
    print("  " + "-" * 40)
    print(f"  OVERALL RESILIENCE SCORE:         {result.scorecard.overall_resilience_score:>6.2f} / 100.0")
    print(f"  RESILIENCE TIER:                  {result.scorecard.resilience_tier.value}")
    print(f"  CERTIFICATION VERDICT:            {result.scorecard.certification_verdict}")
    print(f"  CI/CD PRODUCTION GATING:          {'APPROVED FOR DEPLOYMENT' if result.scorecard.ci_cd_deployment_approved else 'BLOCKED'}")
    print(f"  Exported Evidence Files:          {result.export_result.get('total_files_exported', 0)} files in resilience_verification/")
    print("=" * 80)

    return 0 if result.passed else 1


if __name__ == "__main__":
    exit_code = run_operational_resilience_cli()
    sys.exit(exit_code)
