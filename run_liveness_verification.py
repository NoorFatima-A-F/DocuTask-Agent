"""
Master CLI Runner for Enterprise Liveness Verification Framework (Part 3H.2).
"""
import sys
import os

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.platform_verification.liveness.runtime.liveness_runtime import (
    LivenessVerificationRuntime,
)


def main():
    print("=" * 80)
    print(" DOCUTASK AGENT — PART 3H.2 ENTERPRISE LIVENESS VERIFICATION FRAMEWORK")
    print("=" * 80)
    print("Initializing Multi-Dimensional Liveness Runtime Verification...\n")

    runtime = LivenessVerificationRuntime(output_dir="health_verification")
    results = runtime.run_full_verification(export=True)

    scorecard = results["scorecard"]
    contract_rep = results["contract_report"]
    proc_rep = results["process_report"]
    loop_rep = results["loop_report"]
    deadlock_rep = results["deadlock_report"]
    worker_rep = results["worker_report"]
    scheduler_rep = results["scheduler_report"]
    res_rep = results["resource_report"]
    fail_rep = results["failure_report"]
    recovery_rep = results["recovery_report"]
    sec_rep = results["security_report"]
    exported = results["exported_files"]

    print("—" * 80)
    print("1. LIVENESS CONTRACT DESIGN (PART 1)")
    print("—" * 80)
    print(f"Endpoint:                     {contract_rep.endpoint}")
    print(f"Contract Schema Valid:        {'[PASS]' if contract_rep.passed else '[FAIL]'}")
    print(f"Dependency Isolation:         {'[PASS]' if contract_rep.isolated_from_dependencies else '[FAIL]'} (Zero DB, Redis, or External API calls)")

    print("\n" + "—" * 80)
    print("2. PROCESS EXISTENCE & STATE MONITORING (PART 2)")
    print("—" * 80)
    print(f"Processes Monitored:          {proc_rep.total_processes_checked} active supervised PIDs")
    print(f"Running Processes:            {proc_rep.running_processes_count} / {proc_rep.total_processes_checked}")
    print(f"Blocked / Zombies / Term:     {proc_rep.blocked_count} blocked, {proc_rep.zombies_count} zombies, {proc_rep.terminated_count} terminated")
    print(f"Process State Health:         {'[PASS]' if proc_rep.all_processes_alive else '[FAIL]'}")

    print("\n" + "—" * 80)
    print("3. EVENT LOOP RESPONSIVENESS & DEADLOCK WATCHDOG (PARTS 3 & 4)")
    print("—" * 80)
    print(f"Event Loop Avg / Max Latency: {loop_rep.average_latency_ms:.1f} ms / {loop_rep.maximum_latency_ms:.1f} ms (Threshold < {loop_rep.failure_threshold_ms:.0f} ms)")
    print(f"Watchdog Active:              {'[PASS]' if deadlock_rep.watchdog_active else '[FAIL]'}")
    print(f"Deadlock Scan Status:         {'[PASS] Clean' if not deadlock_rep.deadlock_detected else '[FAIL] Deadlock Detected'}")

    print("\n" + "—" * 80)
    print("4. WORKER & SCHEDULER RUNTIME LIVENESS (PARTS 5, 8 & 9)")
    print("—" * 80)
    print(f"Worker Nodes Tracked:         {worker_rep.total_workers_tracked} workers (Active: {worker_rep.active_workers_count}, Zombies: {worker_rep.zombie_workers_count})")
    print(f"Scheduler Ticking:            {'[PASS]' if scheduler_rep.scheduler_healthy else '[FAIL]'} (Drift: {scheduler_rep.seconds_since_last_tick:.2f}s, Missed Jobs: {scheduler_rep.missed_jobs_count})")

    print("\n" + "—" * 80)
    print("5. RESOURCE CONSUMPTION & MEMORY HEALTH (PARTS 6 & 7)")
    print("—" * 80)
    print(f"Memory RSS / Heap:            {res_rep.memory_rss_mb:.1f} MB / {res_rep.memory_heap_mb:.1f} MB")
    print(f"Memory State:                 {res_rep.memory_state} (NORMAL / WARNING / CRITICAL / UNHEALTHY)")
    print(f"CPU Utilization / Throttle:   {res_rep.cpu_usage_pct:.1f}% / {'THROTTLED' if res_rep.cpu_throttled else 'OPTIMAL'}")

    print("\n" + "—" * 80)
    print("6. FAILURE SIMULATION & RECOVERY MTTR (PARTS 10, 11 & 12)")
    print("—" * 80)
    print(f"Failure Simulations Passed:   {fail_rep.passed_simulations} / {fail_rep.total_simulations}")
    print(f"  - Test 1 Process Kill:      {'[PASS]' if fail_rep.process_kill_handled else '[FAIL]'}")
    print(f"  - Test 2 Loop Freeze:       {'[PASS]' if fail_rep.event_loop_freeze_handled else '[FAIL]'}")
    print(f"  - Test 3 Memory Exhaustion: {'[PASS]' if fail_rep.memory_exhaustion_handled else '[FAIL]'}")
    print(f"  - Test 4 Worker Deadlock:   {'[PASS]' if fail_rep.worker_deadlock_handled else '[FAIL]'}")
    print(f"Mean Time To Recovery (MTTR): {recovery_rep.mttr_seconds:.2f}s (Detection: {recovery_rep.failure_detection_time_seconds}s, Restart: {recovery_rep.restart_time_seconds}s, Init: {recovery_rep.initialization_time_seconds}s)")
    print(f"Cloud Runtimes Compatible:    {', '.join(recovery_rep.cloud_runtimes_compatible)}")

    print("\n" + "—" * 80)
    print("7. SECURITY & OBSERVABILITY (PARTS 13 & 14)")
    print("—" * 80)
    print(f"Zero Info Leaks in /live:     {'[PASS]' if sec_rep.public_endpoint_leak_free else '[FAIL]'} (No DB hosts, API keys, credentials)")
    print(f"Auth & Rate Limiting:         {'[PASS]' if sec_rep.auth_policy_enforced and sec_rep.rate_limiting_active else '[FAIL]'}")

    print("\n" + "=" * 80)
    print(" COMPREHENSIVE ENTERPRISE LIVENESS SCORECARD (PART 16)")
    print("=" * 80)
    print(f"  Runtime Detection Accuracy (25%):     {scorecard.runtime_detection_accuracy_score:>6.2f} / 100.00")
    print(f"  Event Loop Monitoring (20%):          {scorecard.event_loop_monitoring_score:>6.2f} / 100.00")
    print(f"  Deadlock Detection (15%):             {scorecard.deadlock_detection_score:>6.2f} / 100.00")
    print(f"  Resource Monitoring (15%):            {scorecard.resource_monitoring_score:>6.2f} / 100.00")
    print(f"  Recovery Integration (15%):           {scorecard.recovery_integration_score:>6.2f} / 100.00")
    print(f"  Security (10%):                       {scorecard.security_score:>6.2f} / 100.00")
    print("  " + "-" * 50)
    print(f"  OVERALL LIVENESS SCORE:               {scorecard.overall_liveness_score:>6.2f} / 100.00")
    print(f"  CERTIFICATION TIER:                   {scorecard.certification_tier.value}")
    print(f"  CERTIFICATION VERDICT:                {scorecard.certification_verdict}")
    print(f"  AUTO-RECOVERY VALIDATED:              {'YES' if scorecard.auto_recovery_validated else 'NO'}")
    print("=" * 80)

    print(f"\nAudit Evidence Manifests Exported ({len(exported)} files to health_verification/):")
    for fname, fpath in exported.items():
        print(f"  [+] {fname} -> {fpath}")

    print("\nVerification Complete.")
    if scorecard.passed:
        print("[SUCCESS] Platform Liveness Verification meets Enterprise Tier Requirements.")
        sys.exit(0)
    else:
        print("[FAILURE] Platform Liveness Verification failed minimum threshold.")
        sys.exit(1)


if __name__ == "__main__":
    main()
