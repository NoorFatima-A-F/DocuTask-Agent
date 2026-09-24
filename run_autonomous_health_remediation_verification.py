"""Master CLI Runner for Phase 3H.4.3 - Autonomous Health Remediation & Recovery Action Framework.

Executes all 14 sub-parts of Phase 3H.4.3:
1. Remediation Architecture
2. Remediation Policy Engine
3. Action Classification (Levels 0 - 3)
4. Recovery Decision Engine
5. Safety Guard System (Preconditions, Rate Limits, Blast Radius)
6. Remediation Executor (Controlled recovery actions)
7. Recovery Verification Engine (Post-recovery health validation)
8. Rollback Mechanism (State reversion & human escalation)
9. Self-Healing Chaos Scenarios (5 Production scenarios)
10. Remediation Intelligence Metrics (MTTR, MTTD, Automation Success Rate)
11. Security Audit (RBAC, Whitelisting, Zero secret leaks)
12. Observability Integration (Logs, Metrics, Traces)
13. Evidence Generation (8 JSON manifests in health_remediation_verification/)
14. Certification Scoring (Weighted 6-dimension scorecard)
"""

import sys
import os
import io

# Enforce UTF-8 stdout for Windows terminals
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.platform_verification.autonomous_remediation.runtime.autonomous_remediation_runtime import (
    AutonomousRemediationRuntime,
)


def main() -> int:
    print("=" * 100)
    print(" DOCUTASK AGENT - ENTERPRISE AUTONOMOUS HEALTH REMEDIATION & RECOVERY FRAMEWORK")
    print(" PHASE 3H.4.3: SELF-HEALING RELIABILITY, ACTION PLANNING, SAFETY GUARDS & CHAOS VALIDATION")
    print("=" * 100)

    runtime = AutonomousRemediationRuntime()
    print("\n[*] Initializing Phase 3H.4.3 Autonomous Remediation verification engine...")
    results = runtime.run_full_verification()

    policy_rep = results["policy_report"]
    exec_rep = results["execution_report"]
    val_rep = results["validation_report"]
    roll_rep = results["rollback_report"]
    scen_rep = results["scenarios_report"]
    metrics_rep = results["metrics_report"]
    sec_rep = results["security_report"]
    scorecard = results["scorecard"]
    manifests = results["exported_manifests"]

    # 1. Remediation Policies Table
    print("\n" + "-" * 100)
    print(" 1. REMEDIATION POLICY INVENTORY & ACTION CLASSIFICATIONS")
    print("-" * 100)
    print(f" {'CONDITION':<34} | {'ACTION':<28} | {'LEVEL':<20} | {'RISK':<8} | {'COOLDOWN':<8}")
    print("-" * 100)
    for p in policy_rep.policies:
        print(f" {p.condition:<34} | {p.action:<28} | {p.action_level.value[:18]:<20} | {p.risk.value:<8} | {p.cooldown_seconds:>6}s")

    # 2. Action Executions Table
    print("\n" + "-" * 100)
    print(" 2. REMEDIATION EXECUTIONS & STATE TRANSITIONS")
    print("-" * 100)
    print(f" {'EXECUTION ID':<16} | {'ACTION':<26} | {'TARGET':<20} | {'BEFORE -> AFTER':<22} | {'DURATION':<10}")
    print("-" * 100)
    for e in exec_rep.executions:
        transition = f"{e.before_state} -> {e.after_state}"
        print(f" {e.execution_id:<16} | {e.action:<26} | {e.target:<20} | {transition:<22} | {e.duration_ms:>7.1f}ms")

    # 3. Post-Recovery Validations Table
    print("\n" + "-" * 100)
    print(" 3. POST-RECOVERY HEALTH RESTORATION VALIDATION")
    print("-" * 100)
    print(f" Total Validations:          {val_rep.total_validations}")
    print(f" Successful Recoveries:      {val_rep.successful_recoveries}")
    print(f" Recovery Success Rate:      {val_rep.recovery_success_rate_pct:.2f}%")
    print(f" Validation Engine Status:   {val_rep.status}")

    # 4. Rollback & Human Escalation Table
    print("\n" + "-" * 100)
    print(" 4. ROLLBACK OPERATIONS & FAILURE ESCALATIONS")
    print("-" * 100)
    print(f" Total Rollbacks Triggered:  {roll_rep.total_rollbacks_triggered}")
    print(f" Successful Rollbacks:       {roll_rep.successful_rollbacks}")
    print(f" Escalations to Human SRE:   {roll_rep.escalated_incidents_count}")
    print(f" Rollback Success Rate:      {roll_rep.rollback_success_rate_pct:.2f}%")

    # 5. Self-Healing Chaos Scenarios Table
    print("\n" + "-" * 100)
    print(" 5. 5 PRODUCTION SELF-HEALING CHAOS SCENARIOS")
    print("-" * 100)
    for s in scen_rep.scenarios:
        print(f" [✓] {s.scenario_id:<24} | {s.name}")
        print(f"     Failure:    {s.injected_failure}")
        print(f"     Action:     {s.executed_action} ({s.action_level.value})")
        print(f"     Transition: {s.health_transition} | Duration: {s.duration_seconds}s | Passed: {s.passed}")

    # 6. Reliability Intelligence Metrics Table
    print("\n" + "-" * 100)
    print(" 6. REMEDIATION INTELLIGENCE & RELIABILITY METRICS")
    print("-" * 100)
    print(f" Total Detected Incidents:       {metrics_rep.total_incidents_detected}")
    print(f" Successful Auto-Remediations:   {metrics_rep.successful_remediations}")
    print(f" Mean Time to Detect (MTTD):     {metrics_rep.mttd_seconds:.2f}s")
    print(f" Mean Time to Recover (MTTR):    {metrics_rep.mttr_seconds:.2f}s")
    print(f" Automation Success Rate:        {metrics_rep.automation_success_rate_pct:.2f}%")
    print(f" Human Intervention Rate:        {metrics_rep.human_intervention_rate_pct:.2f}%")

    # 7. Security & Permissions Audit Table
    print("\n" + "-" * 100)
    print(" 7. REMEDIATION SECURITY & RBAC PERMISSION AUDIT")
    print("-" * 100)
    print(f" Total Evaluated Security Checks:     {sec_rep.total_checks}")
    print(f" Unauthorized / Destructive Blocked:  {sec_rep.unauthorized_commands_blocked} (Target: >= 3)")
    print(f" Secret / Token Leaks Detected:       {int(sec_rep.secret_leaks_found)} (Target: 0)")
    print(f" RBAC Role Enforcement:               {sec_rep.rbac_enforced}")
    print(f" Audit Compliance Status:             {sec_rep.status}")

    # 8. Composite Quality Scorecard
    print("\n" + "=" * 100)
    print(" ENTERPRISE AUTONOMOUS HEALTH REMEDIATION SCORECARD")
    print("=" * 100)
    print(f" 1. Recovery Accuracy (Weight 25%):          {scorecard.recovery_accuracy_score:>6.2f} / 100")
    print(f" 2. Safety Controls (Weight 20%):            {scorecard.safety_controls_score:>6.2f} / 100")
    print(f" 3. Validation Correctness (Weight 20%):     {scorecard.validation_correctness_score:>6.2f} / 100")
    print(f" 4. Rollback Capability (Weight 15%):        {scorecard.rollback_capability_score:>6.2f} / 100")
    print(f" 5. Observability (Weight 10%):              {scorecard.observability_score:>6.2f} / 100")
    print(f" 6. Security & RBAC (Weight 10%):            {scorecard.security_score:>6.2f} / 100")
    print("-" * 100)
    print(f" OVERALL WEIGHTED SELF-HEALING SCORE:        {scorecard.overall_score:>6.2f}%")
    print(f" CERTIFICATION TIER:                         {scorecard.certification_tier.value}")
    print(f" VERDICT:                                    {scorecard.certification_verdict}")
    print("=" * 100)

    # 9. Manifests Export List
    print("\n[+] Exported 8 Structured Audit Evidence Manifests (health_remediation_verification/):")
    for fname, path in manifests.items():
        print(f"    - {fname:<34} -> {path}")

    if scorecard.passed and scorecard.overall_score >= 95.0:
        print("\n[SUCCESS] Phase 3H.4.3 Autonomous Health Remediation Verification PASSED with Tier 'Enterprise Self-Healing Ready' (>= 95.00%).")
        return 0
    else:
        print(f"\n[FAILURE] Phase 3H.4.3 Verification did not meet target (Score: {scorecard.overall_score}%).")
        return 1


if __name__ == "__main__":
    sys.exit(main())
