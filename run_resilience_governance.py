"""
Master CLI Runner for Part 3G.4:
Disaster Recovery Governance, Continuous Resilience Management & Operational Maturity Verification Framework.
"""
import os
import sys
import io

# Ensure UTF-8 output encoding on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from app.platform_verification.resilience_governance.runtime.governance_runtime import (
    GovernanceRuntime,
)


def run_resilience_governance_cli():
    print("=" * 80)
    print("  PART 3G.4: DISASTER RECOVERY GOVERNANCE & CONTINUOUS RESILIENCE FRAMEWORK")
    print("=" * 80)
    print("Initializing Enterprise Disaster Recovery Governance Verification Engine...")

    runtime = GovernanceRuntime(base_dir=".")
    result = runtime.execute_governance_verification(export_artifacts=True)

    print("\n" + "-" * 80)
    print(" 1. COMPONENT OWNERSHIP VALIDATION (42 Critical Assets)")
    print("-" * 80)
    print(f"Total Components Scanned:    {result.ownership_report.total_components}")
    print(f"Components Fully Owned:      {result.ownership_report.owned_components}")
    print(f"Orphaned Components:        {result.ownership_report.missing_owner}")
    print(f"Ownership Status:            {'[PASS] 100% OWNED' if result.ownership_report.passed else '[FAIL] UNOWNED ASSETS FOUND'}")

    print("\n" + "-" * 80)
    print(" 2. DISASTER RECOVERY POLICY FORMALIZATION")
    print("-" * 80)
    print(f"Policies Evaluated:          {result.policy_report.policies_evaluated}")
    print(f"Backup Policy Compliant:     {result.policy_report.backup_policy_compliant}")
    print(f"Restore Policy Compliant:    {result.policy_report.restore_policy_compliant}")
    print(f"Incident Policy Compliant:   {result.policy_report.incident_policy_compliant}")
    print(f"Testing Policy Compliant:    {result.policy_report.testing_policy_compliant}")
    print(f"All Policies Enforced:       {result.policy_report.all_policies_enforced}")

    print("\n" + "-" * 80)
    print(" 3. CHANGE IMPACT ANALYSIS & DRIFT DETECTION")
    print("-" * 80)
    print(f"Changes Evaluated:           {result.change_impact_report.total_changes_scanned}")
    print(f"Uncovered Dependencies:      {result.change_impact_report.uncovered_dependencies_count}")
    print(f"Documents / Runbooks Scanned:{result.drift_report.total_documents_scanned}")
    print(f"Drifts Detected:             {result.drift_report.drifts_detected_count}")
    print(f"Drift & Change Verdict:      {'[PASS] NO UNCOVERED RISKS' if result.drift_report.passed and result.change_impact_report.passed else '[FAIL] DRIFT DETECTED'}")

    print("\n" + "-" * 80)
    print(" 4. INCIDENT LIFECYCLE & 5-SECTION POSTMORTEMS")
    print("-" * 80)
    print(f"5-Section Completeness:      Summary: {result.postmortem_report.summary_valid} | Timeline: {result.postmortem_report.timeline_valid} | RootCause: {result.postmortem_report.root_cause_valid} | Impact: {result.postmortem_report.impact_valid} | Actions: {result.postmortem_report.action_items_valid}")
    print(f"Postmortem Quality Score:    {result.postmortem_report.postmortem_quality_score} / 100.0")
    print(f"Action Items Cataloged:      {len(result.postmortem_report.action_items)} remediation items with active SLAs")

    print("\n" + "-" * 80)
    print(" 5. CONTINUOUS RESILIENCE METRICS & 5-CATEGORY RISK POSTURE")
    print("-" * 80)
    print(f"Average RTO Measured:        {result.metrics_report.rto_average_minutes} min (SLA <= 15.0 min)")
    print(f"Average RPO Measured:        {result.metrics_report.rpo_average_minutes} min (SLA <= 5.0 min)")
    print(f"Average MTTR Measured:       {result.metrics_report.mttr_average_minutes} min (SLA <= 20.0 min)")
    print(f"Restore Verification Rate:   {result.metrics_report.restore_success_rate_pct}% (Target >= 99.0%)")
    print(f"Total Risks Assessed:        {result.risk_report.total_risks_cataloged} (Unmitigated High/Critical: {result.risk_report.high_critical_risks_unmitigated})")
    print(f"Operational Metrics Verdict: {result.metrics_report.metrics_health_verdict}")

    print("\n" + "-" * 80)
    print(" 6. 6-TIER RESILIENCE MATURITY ASSESSMENT")
    print("-" * 80)
    print(f"Achieved Maturity Tier:      {result.maturity_score.maturity_level.value} (Level {result.maturity_score.level_numeric}/5)")
    print(f"Composite Maturity Score:    {result.maturity_score.maturity_score} / 100.0")
    print("Dimensional Scores:")
    for dim, score in result.maturity_score.dimension_scores.items():
        print(f"  - {dim:<28}: {score:>5.1f} / 100.0")

    print("\n" + "-" * 80)
    print(" 7. COMPLIANCE AUDIT PACKAGE & CI/CD RESILIENCE GATE")
    print("-" * 80)
    print(f"SOC2 / ISO27001 / NIST:      {result.audit_manifest.overall_compliance_pct}% Compliant")
    print(f"CI/CD Gate Passed:           {result.cicd_gate_result.gate_passed}")
    print(f"Deployment Approved:         {result.cicd_gate_result.deployment_approved}")
    print(f"Exported Files Count:        {result.export_result.get('total_files_exported', 0)} files")

    print("\n" + "=" * 80)
    print(" MASTER GOVERNANCE SCORECARD SUMMARY")
    print("=" * 80)
    print(f"  Ownership Score (20%):     {result.scorecard.ownership_score:>6.2f} / 100.0")
    print(f"  Policy Score (15%):        {result.scorecard.policy_governance_score:>6.2f} / 100.0")
    print(f"  Change/Drift Score (20%):  {result.scorecard.change_drift_score:>6.2f} / 100.0")
    print(f"  Maturity Score (20%):      {result.scorecard.maturity_score:>6.2f} / 100.0")
    print(f"  Incident Learning (15%):   {result.scorecard.incident_learning_score:>6.2f} / 100.0")
    print(f"  Audit Readiness (10%):     {result.scorecard.audit_readiness_score:>6.2f} / 100.0")
    print("  " + "-" * 40)
    print(f"  OVERALL GOVERNANCE SCORE:  {result.scorecard.overall_governance_score:>6.2f} / 100.0")
    print(f"  CERTIFICATION STATUS:      {result.scorecard.certification_status}")
    print(f"  CI/CD PRODUCTION GATING:   {'APPROVED FOR DEPLOYMENT' if result.scorecard.ci_cd_deployment_approved else 'BLOCKED'}")
    print("=" * 80)

    return 0 if result.passed else 1


if __name__ == "__main__":
    exit_code = run_resilience_governance_cli()
    sys.exit(exit_code)
