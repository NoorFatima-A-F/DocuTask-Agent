"""
Master CLI Runner for Phase 3R: Enterprise Production Operations Governance Framework.

Executes the complete operational intelligence cycle across:
1. SLO targets & error budget accounting
2. Centralized multi-subsystem production health
3. Incident management lifecycle & MTTR tracking
4. Automated multi-channel alerting rules
5. Operational runbook validation & self-healing remediations
6. Root cause analysis (RCA) hypothesis generation
7. Change management & immutable audit trails
8. AIOps model accuracy & FinOps unit economics
9. 6-dimensional operational maturity scoring & certification.
"""

import os
import sys
from pathlib import Path

from app.platform_verification.enterprise_operations_governance.runtime.operations_governance_runtime import (
    OperationsGovernanceRuntime,
)


def main() -> int:
    output_dir = "operations_verification"
    print("=" * 80)
    print("  DocuTask Agent - Enterprise Operations Governance Framework")
    print("  Phase 3R Production Operations Intelligence & Reliability Governance")
    print("=" * 80)
    print()

    runtime = OperationsGovernanceRuntime()

    print("[*] Executing full Enterprise Operational Governance & SRE Evaluation Cycle...")
    result = runtime.run_governance_cycle(export_dir=output_dir)

    slo = result["slo"]
    error_budget = result["error_budget"]
    health = result["health"]
    incidents = result["incidents"]
    alerts = result["alerts"]
    runbooks = result["runbooks"]
    self_healing = result["self_healing"]
    rca = result["rca"]
    changes = result["changes"]
    audit = result["audit"]
    ai_ops = result["ai_ops"]
    finops = result["finops"]
    maturity = result["maturity"]
    manifest = result["manifest"]

    print()
    print("-" * 80)
    print("  1. RELIABILITY GOVERNANCE: SLO TARGETS & ERROR BUDGET")
    print("-" * 80)
    print(f"  - Overall SLO Compliance : {slo.compliance_score:.1f}% (All SLOs Met: {slo.all_slos_met})")
    for s in slo.slos:
        print(f"    * {s.name:28}: Target {s.target_value:12} | Current: {s.current_value:10} [PASSED]")
    print(f"  - Monthly Error Budget   : {error_budget.remaining_budget_minutes:.1f} / {error_budget.total_budget_minutes:.1f} mins ({error_budget.remaining_budget_pct:.1f}% Remaining)")
    print(f"  - Deployment Freeze Gate : {'ACTIVE (BLOCKED)' if error_budget.deployment_freeze_active else 'CLEAR (Deployments Permitted)'}")

    print()
    print("-" * 80)
    print("  2. PRODUCTION HEALTH INTELLIGENCE & TELEMETRY")
    print("-" * 80)
    print(f"  - Centralized Health     : {health.overall_status.value} (API: {health.api_health.value}, Worker: {health.worker_health.value}, DB: {health.database_health.value})")
    print(f"  - Resource Consumption   : CPU: {health.cpu_usage_pct:.1f}%, RAM: {health.memory_usage_pct:.1f}%, Disk: {health.disk_usage_pct:.1f}%")
    print(f"  - Alerting Subsystem     : {alerts.pipeline_status} ({alerts.total_configured_alerts} alerts across {len(alerts.notification_channels)} channels)")

    print()
    print("-" * 80)
    print("  3. INCIDENT MANAGEMENT, RUNBOOKS & SELF-HEALING")
    print("-" * 80)
    print(f"  - Incident History       : {incidents.resolved_incidents_count} Resolved, {incidents.active_incidents_count} Active (Mean MTTR: {incidents.mean_time_to_recover_sec:.1f}s)")
    print(f"  - Operational Runbooks   : {runbooks.total_runbooks} Runbooks Validated ({runbooks.coverage_pct:.0f}% Coverage)")
    print(f"  - Self-Healing Engine    : {self_healing.successful_remediations} / {self_healing.total_remediations_executed} Remediations Successful (Avg Time: {self_healing.average_recovery_time_sec:.1f}s)")
    print(f"  - Automated RCA Incident : {rca.incident_id} (Primary Cause: '{rca.hypotheses[0].hypothesis}', Conf: {rca.confidence:.1f}%)")

    print()
    print("-" * 80)
    print("  4. CHANGE AUDIT, AIOPS & FINOPS ECONOMICS")
    print("-" * 80)
    print(f"  - Change Management Score: {changes.change_discipline_score:.1f}% ({changes.total_changes_recorded} changes auditable)")
    print(f"  - Immutable Audit Events : {audit.total_audit_events} Events ({audit.compliance_integrity})")
    print(f"  - AI Extraction Accuracy : {ai_ops.extraction_accuracy_pct:.1f}% (Schema Validations: {ai_ops.schema_validation_success_pct:.1f}%, Cost/Doc: ${ai_ops.average_cost_per_document_usd:.4f})")
    print(f"  - FinOps Budget & Spend  : ${finops.current_month_spend_usd:.2f} / ${finops.monthly_budget_usd:.2f} ({finops.budget_utilized_pct:.1f}% used, Efficiency: {finops.cost_efficiency_score:.1f}%)")

    print()
    print("=" * 80)
    print(f"  OPERATIONAL MATURITY SCORE: {maturity.overall_maturity_score:.1f}%")
    print(f"  CERTIFICATION TIER        : {maturity.certification.value.upper()}")
    print(f"  GOVERNANCE VERDICT        : {'APPROVED' if maturity.governance_passed else 'REJECTED'}")
    print(f"  EVIDENCE REPOSITORY       : {os.path.abspath(output_dir)}")
    print(f"  CRYPTOGRAPHIC MANIFEST    : {os.path.abspath(os.path.join(output_dir, 'manifest.json'))} ({len(manifest.files)} SHA-256 artifacts)")
    print("=" * 80)

    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
